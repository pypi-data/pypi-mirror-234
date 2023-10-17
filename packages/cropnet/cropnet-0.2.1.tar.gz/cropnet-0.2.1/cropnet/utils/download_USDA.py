import os
import warnings
import json
import argparse

import numpy as np
import requests as req
import pandas as pd

from cropnet.utils import path_utils

warnings.filterwarnings('ignore')

# parser = argparse.ArgumentParser(description='Python Preprocessing Cotton Data')
# parser.add_argument('-bu', '--base_url', type=str, default='https://quickstats.nass.usda.gov/grid/grid_data')
# parser.add_argument('-op', '--output_path', type=str, default='~/Documents')
#
# args = parser.parse_args()
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
}

# breakdown of what each parameter means in the outputted csv
# year                  -> year the data was taken for
# Id                    -> number of item in the list
# published_cv          -> this might deal with the coefficient of variability, but it doesn't seem useful
# short_desc            -> short description of the data
# source_desc           -> description of where the data was sourced (all SURVEY)
# asd_desc              -> description of agricultural area
# domain_desc           -> how much area was covered (typically TOTAL)
# state_name            -> name of the state
# domaincat_desc        -> description of domain category (typically unspecified)
# published_estimate    -> number of crops
# county_ansi           -> county part of FIPS
# commodity_desc        -> product
# watershed_code        -> watershed address to find water info (only has 00000000)
# reference_period_desc -> period of time
# county_name           -> name of the county
# state_ansi            -> state part of FIPS
# agg_level_desc        -> agricultural district code


# function to download data based on major crop and year
def download(crop_type, start, end, base_url, output_path, fips_codes=None):
    """
    Download data based on given crop and range of years
    :param: crop: desired crop
    :param: start: start year
    :param: end: end year
    :param: base_url: base url for USDA website
    :param: output_path: path to save the data
    :param: fips_codes: list of fips codes. If empty, then download all U.S. counties.
    """

    # dictionaries for each major crop
    # corn production measured in BU and yield measured in BU/Acre
    corn_url_dic = {
        "2016": "/7B610A32-020E-3F2B-8021-D8DB785F6F0D",
        "2017": "/F40BC7B4-260F-3EB8-8B3B-BFB5791338C5",
        "2018": "/59A4E969-8A42-3CE5-B847-45F6222546E5",
        "2019": "/5101C24D-152D-36BE-9AD8-FFC83107914C",
        "2020": "/0C0144CA-CD19-3263-939C-60D1C33D6BE5",
        "2021": "/6E0B4388-C733-37A6-B2C1-5ADBD5AA940C",
        "2022": "/6633348E-B2AA-3F83-8E72-5D270512DD23"
    }

    # upland cotton production measured in 480 lb bales and yield measured in lb/acre
    cotton_url_dic = {
        "2016": "/661C3A23-DEEC-37FE-ACBD-B0A97CF7CD7F",
        "2017": "/9E5390A6-057E-393F-9AB0-33278B856DED",
        "2018": "/C70A0999-E77A-33CE-9D75-9B5C887455DA",
        "2019": "/D376CB50-6B28-3834-81D5-C28F00C27CB9",
        "2020": "/A2F89CA2-ED06-33FA-BEA7-7C954E74D9C8",
        "2021": "/2270D733-1CFD-3F33-B041-222D18D3084C",
        "2022": "/E2A4226D-3B82-3A93-913B-F8933591C0B1",
    }

    # winter wheat production measured in bu and yield measured in bu/acre
    wheat_url_dic = {
        "2016": "/5ABCCABF-C72E-3CD5-9BA8-C666E02E8CF6",
        "2017": "/DB144B23-51A9-303A-ABC0-E791850329DC",
        "2018": "/2FF1F5C3-6AB9-3837-8F17-E58E44F083CF",
        "2019": "/88757047-C063-3543-8348-DD5F95277398",
        "2020": "/30703A37-47CB-3583-8E49-158F1969583A",
        "2021": "/50880CB2-68F7-3F94-AFF5-C4658CB9B121",
        "2022": "/75DB97AB-2241-31F4-B821-41E9162EA375"
    }

    # soybean production measured in bu and yield measured in bu/acre
    soybean_url_dic = {
        "2016": "/7C723A4D-CE64-3B71-BC36-50DFABE63EDA",
        "2017": "/29A25C45-FFB2-3549-8794-648E01F5F497",
        "2018": "/CED79362-BE74-32B5-A35E-6AD882FEC9E7",
        "2019": "/0038926C-B93A-3E56-AAB4-1CCD3E3C71EB",
        "2020": "/BA641CAB-9F94-31ED-9942-833294ECA18E",
        "2021": "/4CD58194-52DA-38E8-9842-903F5F43CFAC",
        "2022": "/734F6EE6-30A2-3057-98A1-8C4B7FF6C467"
    }

    barley_url_dic = {
        "2016": "/767A7AF7-5A82-3583-B302-E0919FDFEBD0",
        "2017": "/1CF42E6F-2737-3C72-BE80-BBE2563B08F8",
        "2018": "/D44E43DD-2C03-3524-873E-F91AAEA322D9",
        "2019": "/3B9D89F6-A90D-3838-A8E3-BB5FA25C1855",
        "2020": "/31B852A6-CEB0-3598-9D6C-98675D450E84",
        "2021": "/B8F43699-0111-3B4D-A13E-8DDF6A8A9078",
        "2022": "/5FE9C6EB-EE06-31B4-B2B6-7FD805C77F1E",
    }

    # getting correct dictionary
    dic = {}
    values = []
    if crop_type == "Corn":
        dic = dict(corn_url_dic)
    elif crop_type == "Cotton":
        dic = dict(cotton_url_dic)
    elif crop_type == "WinterWheat":
        dic = dict(wheat_url_dic)
    elif crop_type == "Soybean":
        dic = dict(soybean_url_dic)
    elif crop_type == "Barley":
        dic = dict(barley_url_dic)
    else:
        print("crop not in dataset")

    # pulling data
    total_df = pd.DataFrame()
    for year in range(int(start), int(end) + 1):
        # 2017 Barley data is not available
        if dic.get(str(year)) == "/1CF42E6F-2737-3C72-BE80-BBE2563B08F8":
            print("2017 Barley data is not available!")
            continue

        url = base_url + dic.get(str(year)) + "?start=0&count=30"

        # get the total number of rows
        res = req.get(url, headers=header)
        content = json.loads(res.text)
        num_rows = content["numRows"]

        # get the whole year data
        url = base_url + dic.get(str(year)) + "?start=0&count={}".format(num_rows)
        res = req.get(url, headers=header)
        content = json.loads(res.text)
        crop_yield = json.dumps(content["items"])
        df = pd.read_json(crop_yield)

        # drop rows containing (D) in published_estimate
        df = df.drop(df[df["published_estimate"].str.contains("(D)")].index)
        df = df.reset_index(drop=True)

        # convert string to number
        df["published_estimate"] = df["published_estimate"].str.replace(',', '').astype(np.float64)

        values = [[desc for desc in df.short_desc.unique() if "PRODUCTION, MEASURED IN" in desc],
                  [desc for desc in df.short_desc.unique() if "YIELD, MEASURED IN" in desc]]

        # flatten the values array
        values_arr = []
        for array in values:
            for item in array:
                values_arr.append(item)
        values = values_arr

        # filter specific values
        df = df[df["short_desc"].isin(values)]

        # convert rows to columns
        df = df.pivot_table(
            index=['commodity_desc', 'reference_period_desc', 'year', 'state_ansi', 'state_name', 'county_ansi',
                   'county_name', 'asd_code', 'asd_desc', 'domain_desc', 'source_desc', 'agg_level_desc'],
            columns=["short_desc"], values="published_estimate", aggfunc='first').reset_index()

        # rename columns, removing the commodity name
        new_name = ""
        for col in df.columns:
            if "PRODUCTION, MEASURED IN" in col:
                new_name = col.split(' - ')[1]
                df = df.rename({col: new_name}, axis='columns')
            elif "YIELD, MEASURED IN" in col:
                new_name = col.split(' - ')[1]
                df = df.rename({col: new_name}, axis='columns')

        # covert the state-ansi and county-ansi to string with leading zeros
        df['state_ansi'] = df['state_ansi'].astype(str).str.zfill(2)
        df['county_ansi'] = df['county_ansi'].astype(int).astype(str).str.zfill(3)

        df['state_ansi'] = df['state_ansi'].values.astype(str)
        df['county_ansi'] = df['county_ansi'].values.astype(str)

        total_df = pd.concat([total_df, df], ignore_index=True)

    # filter by fips codes
    if fips_codes:
        states = list(map(lambda x: x[:2], fips_codes))
        counties = list(map(lambda x: x[2:], fips_codes))
        total_df = total_df[total_df['state_ansi'].isin(states) & total_df['county_ansi'].isin(counties)]

    # save data
    if start != end:
        path = output_path + "/USDA/data/" + crop_type + "/" + end + "/USDA_{}_County_{}-{}.csv".format(crop_type, start, end)
    else:
        path = output_path + "/USDA/data/" + crop_type + "/" + end + "/USDA_{}_County_{}.csv".format(crop_type, start)

    path_utils.create_directories_if_not_exist(path)
    total_df.to_csv(path, index=False)


if __name__ == '__main__':
    pass
    # enter the desired crop, start year, and end year
    # download("Soybean", "2022", "2022")