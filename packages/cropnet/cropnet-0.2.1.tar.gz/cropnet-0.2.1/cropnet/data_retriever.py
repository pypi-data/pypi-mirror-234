import concurrent
import os
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from typing import List

import h5py
import pandas as pd

from cropnet.utils.path_utils import get_state_abbr
import numpy as np


class DataRetriever(object):

    def __init__(self, base_dir, num_workers=4):
        self.base_dir = base_dir
        self.num_workers = num_workers
        self.executor = ThreadPoolExecutor(max_workers=num_workers)

    def retrieve_USDA(self, crop_type: str, fips_codes: List[str], years: List[str]):
        """
        Retrieve USDA data for the specified FIPS codes and years.
        :param crop_type: specify the crop type, e.g., "Corn", "Cotton", "WinterWheat", or "Soybean"
        :param fips_codes: specify a list of FIPS codes, e.g., ["10001", "10003"]. If None, then retrieve all U.S. counties.
        :param years: specify a list of years, e.g., ["2021", "2022"]
        :return:
        """

        assert crop_type in ["Corn", "Cotton", "WinterWheat",
                             "Soybean"], "Please specify a valid crop type: Corn, Cotton, WinterWheat, or Soybean"
        assert self.base_dir is not None, "Please specify a base directory"

        file_paths = set()
        for year in years:
            root_dir = "{}/USDA/data/{}/{}".format(self.base_dir, crop_type, year)
            file_name = "USDA_{}_County_{}.csv".format(crop_type, year)

            file_path = os.path.join(root_dir, file_name)

            if not os.path.exists(file_path):
                print("USDA data is not available: {}".format(file_path))
                continue

            file_paths.add(file_path)

        # read the USDA data
        dfs = []
        for file_path in file_paths:
            df = self.read_csv_file(file_path)
            dfs.append(df)
        df = pd.concat(dfs, ignore_index=True)

        # convert state_ansi and county_ansi to string with leading zeros
        df['state_ansi'] = df['state_ansi'].astype(str).str.zfill(2)
        df['county_ansi'] = df['county_ansi'].astype(str).str.zfill(3)

        # filter the USDA data by FIPS codes
        if fips_codes:
            states = list(map(lambda x: x[:2], fips_codes))
            counties = list(map(lambda x: x[2:], fips_codes))
            df = df[(df["state_ansi"].isin(states)) & (df["county_ansi"].isin(counties))]

        return df

    def retrieve_Sentinel2(self, fips_codes: List[str], years: List[str], image_type="AG"):
        """
        Retrieve Sentinel-2 data for the specified FIPS codes and years.
        :param fips_codes: specify a list of FIPS codes, e.g., ["10001", "10003"]
        :param years: specify a list of years, e.g., ["2021", "2022"]
        :param image_type: specify a list of image types, i.e., "AG" OR "NDVI".
            "AG" is the Agricultural Image, and "NDVI" is the Normalized Difference Vegetation Index.

        :return: a dictionary of FIPS codes and Sentinel-2 images, e.g., {"22007": x}.
                Here x is a 5D tensor of size (T, G, H, W, C), e.g., (24, 11, 224, 224, 3),
                where T is the number of temporal data,
                G is the number of grids for the county,
                and (H, W, C) represents a satellite image.
        """

        assert self.base_dir is not None, "Please specify a root directory"
        assert image_type in ["AG", "NDVI"], "Please specify a valid image type: AG or NDVI"

        file_prefix = "Agriculture" if image_type == "AG" else "NDVI"
        # sort the years by ascending order
        years = sorted(years)

        fips_paths_map = {}
        for fips_code in fips_codes:
            file_paths = set()
            for year in years:
                state_code, county_code = fips_code[:2], fips_code[2:]
                state_abbr = get_state_abbr(state_code)
                # iterate file paths for each quarter
                for start, end in [("01-01", "03-31"), ("04-01", "06-30"), ("07-01", "09-30"), ("10-01", "12-31")]:
                    start_day = year + "-" + start
                    end_day = year + "-" + end
                    root_dir = "{}/Sentinel/data/{}/{}/{}".format(self.base_dir, image_type, year, state_abbr)
                    file_name = "{}_{}_{}_{}_{}.h5".format(file_prefix, state_code, state_abbr, start_day, end_day)
                    file_path = os.path.join(root_dir, file_name)

                    if not os.path.exists(file_path):
                        print("Sentinel-2 data for FIPS Code {} at {} is not available: {}".format(fips_code, year, file_path))
                        continue

                    file_paths.add(file_path)

            if file_paths: fips_paths_map[fips_code] = file_paths

        fips_image_map = {}
        for fips, file_paths in fips_paths_map.items():
            temporal_list = []
            for file_path in file_paths:
                with h5py.File(file_path, 'r') as hf:
                    if fips not in hf.keys(): continue

                    groups = hf[fips]
                    for i, d in enumerate(groups.keys()):
                        grids = groups[d]["data"]
                        grids = np.asarray(grids)
                        temporal_list.append(grids)
                    hf.close()

            if temporal_list: fips_image_map[fips] = np.stack(temporal_list)

        return fips_image_map

    def retrieve_HRRR(self, fips_codes: List[str], years: List[str]):
        """
        Retrieve HRRR data for the specified FIPS codes and months.
        :param fips_codes: specify a list of FIPS codes, e.g., ["10001", "10003"]
        :param years: specify a list of months, e.g., ["202201", "202202"]
        :return:
        """

        assert self.base_dir is not None, "Please specify a root directory"
        assert fips_codes, "The list of FIPS codes cannot be empty."

        states = list(map(lambda x: x[:2], fips_codes))
        counties = list(map(lambda x: x[2:], fips_codes))

        file_paths = set()
        for year in years:
            for i in range(len(states)):
                state_code, county_code = states[i], counties[i]
                state_abbr = get_state_abbr(state_code)
                root_dir = "{}/HRRR/data/{}/{}".format(self.base_dir, year, state_abbr)
                # iterate over 12 months
                for month in range(1, 13):
                    # format month to 2 digits
                    month = str(month).zfill(2)
                    file_name = "HRRR_{}_{}_{}-{}.csv".format(state_code, state_abbr, year, month)

                    file_path = os.path.join(root_dir, file_name)
                    # check if the file exists
                    if not os.path.exists(file_path):
                        print("HRRR data is not available: {}".format(file_path))
                        continue

                    # if the file exists, then add it to the file path set
                    file_paths.add(file_path)

        # Submit read_csv_file function for each file path
        futures = [self.executor.submit(self.read_csv_file, file_path) for file_path in file_paths]
        # Wait for all tasks (reading files) to complete
        concurrent.futures.wait(futures)
        # Get the results (DataFrames) from the completed tasks
        dfs = [future.result() for future in futures]

        df = pd.concat(dfs, ignore_index=True)
        # read FIPS code as string
        df["FIPS Code"] = df["FIPS Code"].astype(str)
        # filter the HRRR data by FIPS codes
        df = df[df["FIPS Code"].isin(fips_codes)]

        return df

    @lru_cache(maxsize=128)
    def read_csv_file(self, file_path: str):
        return pd.read_csv(file_path)


if __name__ == '__main__':
    obj = DataRetriever(base_dir="/mnt/data/CropNet")
    usda_data = obj.retrieve_USDA(crop_type="Soybean", fips_codes=[], years=["2021", "2022"])
    hrrr_data = obj.retrieve_HRRR(fips_codes=["22007"], years=["2021", "2022"])
    sentinel_data = obj.retrieve_Sentinel2(fips_codes=["22007", "22107", "22005"], years=["2021", "2022"], image_type="AG")

    print(usda_data)
    print(hrrr_data)

    for fips, data in sentinel_data.items():
        print(fips)
        print(data.shape)
