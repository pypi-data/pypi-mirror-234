import concurrent
import os
import datetime
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from typing import List
import shutil

from cropnet.utils import download_USDA
from cropnet.utils.download_sentinel import get_county_images_seasonal, get_state_name, get_county_name

from cropnet.utils.download_wrf import DownloadWrfGrib2
from cropnet.utils.extract_wrf_data import PreprocessWRF


class DataDownloader(object):

    def __init__(self, target_dir="./data", num_workers=8, usda_base_url=None, client_id=None, client_secret=None):
        """
        Initialize the CropData object.
        :param target_dir: the directory where the data will be downloaded
        :param num_workers: the number of workers to use for downloading and processing the data
        :param client_id: sentinel hub client ID
        :param client_secret: sentinel hub client secret
        :return:
        """

        self.target_dir = target_dir
        self.num_workers = num_workers
        self.executor = ThreadPoolExecutor(max_workers=num_workers)

        if usda_base_url is None:
            usda_base_url = 'https://quickstats.nass.usda.gov/grid/grid_data'

        # Sentinel Hub credentials
        if client_id is None:
            # science 01
            # client_id = "d61ac631-ca3b-4290-9ef5-b15b1cd4c82b"
            # science 02
            # client_id = "d2577ff5-cd0e-4f53-b65a-211bc1c0bde9"
            # science 03
            client_id = "37457d21-715f-49ea-b9b9-0b0acc84b29f"
        if client_secret is None:
            # science 01
            # client_secret = "%gLPf03F(K3;)NT5g~>:oH@(lot^|]g,J5NR8b%%"
            # science 02
            # client_secret = "wznFGW3HZanBLRmms>7z6AivvJJ4_YBkhP^[Hh12"
            # science 03
            client_secret = "8;EJJ.Q4F0wHL[fY2j4w9eX*&M(:a7lThgH7P-dK"


        self.usda_base_url = usda_base_url
        self.client_id = client_id
        self.client_secret = client_secret

    def download_USDA(self, crop_type: str, fips_codes: List[str], years: List[str]):
        """
        Download USDA data for the specified FIPS codes and years.
        :param crop_type: specify the crop type, e.g., "Corn", "Cotton", "WinterWheat", "Soybean", or "Barley"
        :param fips_codes: specify a list of FIPS codes, e.g., ["10001", "10003"].
            If None, then download all U.S. counties.
        :param years: specify a list of years, e.g., ["2021", "2022"]
        :return:
        """

        assert crop_type in ["Corn", "Cotton", "WinterWheat", "Soybean", "Barley"], \
            "Please specify a valid crop type: Corn, Cotton, WinterWheat, or Soybean"
        assert self.target_dir is not None, "Please specify a target directory"
        assert self.usda_base_url is not None, "Please specify a USDA base URL"

        # download the data
        for i, year in enumerate(years):
            print("Progress: [ {}/{} ], Downloading USDA Data, Year: {}, Crop: {}".format(i + 1, len(years), year,
                                                                                          crop_type))
            download_USDA.download(crop_type, year, year, self.usda_base_url, self.target_dir, fips_codes=fips_codes)

    def download_Sentinel2(self, fips_codes: List[str], years: List[str], image_type: str = "AG"):
        """
        Download Sentinel-2 data for the specified FIPS codes and years.
        :param fips_codes: a list of FIPS codes, e.g., ["10001", "10003"]
        :param years: a list of years, e.g., ["2021", "2022"]
        :param image_type: a list of image types, i.e., "AG" OR "NDVI".
            "AG" is the Agricultural Image, and "NDVI" is the Normalized Difference Vegetation Index.
        :return:
        """

        # Check if all required parameters are set
        assert self.target_dir is not None, "Please specify a target directory"
        assert self.client_id is not None, "Please specify a client ID"
        assert self.client_secret is not None, "Please specify a client secret"
        assert image_type in ["AG", "NDVI"], "Please specify a valid image type: AG or NDVI"

        # get state and county fips codes
        states = list(map(lambda x: x[:2], fips_codes))
        counties = list(map(lambda x: x[2:], fips_codes))

        for i in range(len(states)):
            print(" Downloading Sentinel-2 Imagery ({}), Progress: [{} / {}], FIPS: {}, State Name: {}, County Name: {}"
                  .format(image_type, i + 1, len(states), fips_codes[i], get_state_name(states[i]),
                          get_county_name(states[i], counties[i])))

            get_county_images_seasonal(self.client_id, self.client_secret, self.target_dir, self.num_workers,
                                       [fips_codes[i]], years, image_type)

    def download_HRRR(self, fips_codes: List[str], years: List[str]):
        """
        Download HRRR data for the specified FIPS codes and years.
        :param fips_codes: specify a list of FIPS codes, e.g., ["10001", "10003"]
        :param years: specify a list of years, e.g., ["2021", "2022"]
        :return:
        """

        # Check if all required parameters are set
        assert self.target_dir is not None, "Please specify a target directory"

        all_months = [str(month).zfill(2) for month in range(1, 13)]
        for year in years:
            months = [year + month for month in all_months]

            print("Start to download {} WRF-HRRR data for counties: {}".format(year, fips_codes))

            # call the download script by submitting it to the executor
            futures = [self.executor.submit(self.download_HRRR_month, fips_codes, months)]
            # wait for the download script to finish
            concurrent.futures.wait(futures)

            print("Successfully download {} WRF-HRRR data for counties: {}".format(year, fips_codes))

    def download_HRRR_month(self, fips_codes: List[str], months: List[str]):
        """
        Download HRRR data for the specified FIPS codes and months.
        :param fips_codes: specify a list of FIPS codes, e.g., ["10001", "10003"]
        :param months: specify a list of months, e.g., ["202201", "202202"]
        :return:
        """

        # Check if all required parameters are set
        assert self.target_dir is not None, "Please specify a target directory"
        # TODO: make sure pased fips codes are correctly formatted

        current_date = datetime.datetime.now()
        current_month = current_date.strftime("%Y%m")

        orig_months = set(months)

        months = [month for month in months if month < current_month]

        # check which months are not available
        not_downloaded = orig_months - set(months)
        print("Warning: The HRRR data for the following months is not yet available: {}".format(not_downloaded))

        # for each passed month, call the download script and then the formatting script
        for yyyymm in months:
            # get the begin date and end date ready to be passed to script
            year = int(yyyymm[:4])
            month = int(yyyymm[4:])
            start_date = datetime.date(year, month, 1)

            # calculate the end of the month
            if month == 12:
                next_month = 1
                next_year = year + 1
            else:
                next_month = month + 1
                next_year = year
            # end_date is not inclusive, needs to be the first day of the next month
            end_date = datetime.date(next_year, next_month, 1) # - datetime.timedelta(days=1)

            start_date_str = start_date.strftime("%Y%m%d")
            end_date_str = end_date.strftime("%Y%m%d")

            # call the download script
            downloader = DownloadWrfGrib2()
            downloader.download_path = os.path.join(self.target_dir, "HRRR")
            downloader.begin_date = start_date_str
            downloader.end_date = end_date_str
            downloader.start_hour = "00:00"
            downloader.end_hour = "23:00"
            downloader.download_flag = "both"

            print(f"Downloading HRRR data for {yyyymm}...")
            downloader.main()

            # get the core count to see how much to thread
            num_cores_to_use = int(multiprocessing.cpu_count() * 0.6)

            # call the formatter script
            extractor = PreprocessWRF()
            extractor.grib_path = os.path.join(self.target_dir, "HRRR/realtime_wrf/")
            extractor.precipitation_path = os.path.join(self.target_dir, "HRRR/precip_wrf/")
            extractor.write_path = os.path.join(self.target_dir, "HRRR/")
            extractor.begin_date = start_date_str
            extractor.end_date = end_date_str
            extractor.begin_hour = "00:00"
            extractor.end_hour = "23:00"
            extractor.max_workers = num_cores_to_use
            extractor.passedFips = fips_codes
            extractor.main()

        # remove the hourly data and the log files
        path = os.path.join(self.target_dir, "HRRR/daily_data")
        try:
            for root, dirs, files, in os.walk(path, topdown=False):
                for file in files: 
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                for d in dirs: 
                    dir_path = os.path.join(root, d)
                    os.rmdir(dir_path)
            os.rmdir(path)
        except Exception as e:
            pass

        # remove the empty directories created from downloading
        path = os.path.join(self.target_dir, "HRRR/hrrr")
        try:
            for root, dirs, files, in os.walk(path, topdown=False):
                for file in files: 
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                for d in dirs: 
                    dir_path = os.path.join(root, d)
                    os.rmdir(dir_path)
            os.rmdir(path)
        except Exception as e:
            pass

        # remove all the other WRF files (realtime and precip)
        path = os.path.join(self.target_dir, "HRRR/realtime_wrf/")
        try:
            for root, dirs, files, in os.walk(path, topdown=False):
                for file in files: 
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                for d in dirs: 
                    dir_path = os.path.join(root, d)
                    os.rmdir(dir_path)
            os.rmdir(path)
        except Exception as e:
            pass

        path = os.path.join(self.target_dir, "HRRR/precip_wrf/")
        try:
            for root, dirs, files, in os.walk(path, topdown=False):
                for file in files: 
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                for d in dirs: 
                    dir_path = os.path.join(root, d)
                    os.rmdir(dir_path)
            os.rmdir(path)
        except Exception as e:
            pass


if __name__ == '__main__':
    obj = DataDownloader(target_dir="./data")
    # obj.download_Sentinel2(fips_codes=["10003"], years=["2022"], image_type="NDVI")
    # obj.download_Sentinel2(image_type="NDVI")

    obj.download_USDA("Corn", fips_codes=["10003"], years=["2022"])
    # obj.download_HRRR(fips_codes=["10003"], years=["2022"])
    # obj.download_HRRR_month(fips_codes=["10003"], months=["202301"])


