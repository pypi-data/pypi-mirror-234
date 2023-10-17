import argparse
import datetime
import os

import PIL
import pandas
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from PIL import Image
import io
import matplotlib.pyplot as plt
from datetime import date, timedelta
import numpy as np

import geopandas as gpd
import json
import h5py

from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from tqdm import tqdm

from cropnet.utils import geo_utils
from cropnet.utils.path_utils import create_directories_if_not_exist, get_state_abbr, is_before_end_of_current_quarter


def get_token(client_id, client_secret):
    """
    Request token from sentinel hub
    :param: client_id: client id for sentinel hub
    :param: client_secret: client secret for sentinel hub
    :return: token
    """

    # set up credentials
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)

    # get an authentication token
    token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/oauth/token',
                              client_id=client_id, client_secret=client_secret)
    return oauth, token


def build_evalscript(img_type):
    """
    Return evalscript for the input image type
    :param img_type: ["Moisture Index", "Vegetation Index", "Agriculture"]
    :return: evalscript
    """

    valid_input = ["Moisture Index", "Vegetation Index", "Agriculture"]
    assert img_type in valid_input, 'Invalid image type for building evalscript'

    if img_type == "Moisture Index":
        # moisture index evalscript
        evalscript = """
        //VERSION=3
        let index = (B8A - B11)/(B8A + B11);

        let val = colorBlend(index, [-0.8, -0.24, -0.032, 0.032, 0.24, 0.8], [[0.5,0,0], [1,0,0], [1,1,0], [0,1,1], [0,0,1], [0,0,0.5]]);
        val.push(dataMask);
        return val;

        """
    elif img_type == "Vegetation Index":
        # vegetation index evalscript
        evalscript = """
        //VERSION=3

        let viz = ColorMapVisualizer.createDefaultColorMap();

        function evaluatePixel(samples) {
            let val = index(samples.B08, samples.B04);
            val = viz.process(val);
            val.push(samples.dataMask);
            return val;
        }

        function setup() {
          return {
            input: [{
              bands: [
                "B04",
                "B08",
                "dataMask"
              ]
            }],
            output: {
              bands: 4
            }
          }
        }

        """
    else:
        # agriculture evalscript
        evalscript = """
        //VERSION=3
        let minVal = 0.0;
        let maxVal = 0.4;

        let viz = new HighlightCompressVisualizer(minVal, maxVal);

        function setup() {
          return {
            input: ["B02", "B08", "B11", "dataMask"],
            output: { bands: 4 }
          };
        }

        function evaluatePixel(samples) {
            let val = [samples.B11, samples.B08, samples.B02, samples.dataMask];
            return viz.processList(val);
        }

        """

    return evalscript


def build_request_json(evalscript, geometry, end, width=224, height=224):
    """
    Return the json request for a particular image based on specifications
    :param evalscript: script for getting a certain image type
    :param geometry: boundaries of the location
    :param end: end date
    :param width: width of the output image
    :param height: height of the output image
    :return: json request
    """

    start = get_previous_day(end, delta=180)

    json_request = {
        "input": {
            "bounds": {
                "geometry": geometry
            },
            "data": [
                {
                    "dataFilter": {
                        "timeRange": {
                            "from": str(start + "T00:00:00Z"),
                            "to": str(end + "T23:59:59Z")
                        },
                        "mosaickingOrder": "mostRecent",
                        "previewMode": "EXTENDED_PREVIEW",
                        "maxCloudCoverage": 20
                    },
                    "processing": {},
                    "type": "sentinel-2-l1c"
                }
            ]
        },
        "output": {
            "width": width,
            "height": height,
            "responses": [
                {
                    "identifier": "default",
                    "format": {
                        "type": "image/png"
                    }
                }
            ],
            "delivery": {
                "s3": {}
            }
        },
        "evalscript": evalscript
    }

    return json_request


def build_geometry_grids(state_id, county_id):
    """
    Return boundaries of grids in a county
    :param state_id: FIPS code for the state
    :param county_id: FIPS code for the county
    :return: boundaries of the grids
    """

    # Load geometry information for US counties
    # cur_dir = os.path.dirname(os.path.abspath(__file__))
    # csv_path = os.path.join(cur_dir, 'input/US-counties.geojson')

    csv_path = "https://github.com/fudonglin/PyPI_resources/blob/main/cropnet/US-counties.geojson?raw=true"
    geoData = gpd.read_file(csv_path)

    # geoData = gpd.read_file('https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/US-counties.geojson')


    # Make sure the "id" column is an integer
    geoData.id = geoData.id.astype(str).astype(int)

    # Remove Alaska, Hawaii and Puerto Rico.
    stateToRemove = ['02', '15', '72']
    geoData = geoData[~geoData.STATE.isin(stateToRemove)]

    county_data = geoData[(geoData.STATE == state_id) & (geoData.COUNTY == county_id)]

    # partition a county into 10km * 10km grid
    geom = county_data.geometry.iloc[0]
    grid = geo_utils.partition(geom, 0.08)

    geometry = gpd.GeoSeries(grid)
    geometry_json = geometry.to_json()
    geometry_json = json.loads(geometry_json)

    geometry_grids = geometry_json["features"]

    return geometry_grids


def get_grid_boundaries(state_id, county_id):
    """
    Return boundaries of grids in a county as an array with lat/lon info
    :param state_id: FIPS code for the state
    :param county_id: FIPS code for the county
    :return: boundaries of the grids with lat/lon info
    """

    # Load geometry information for US counties
    csv_path = "https://github.com/fudonglin/PyPI_resources/blob/main/cropnet/US-counties.geojson?raw=true"
    geoData = gpd.read_file(csv_path)

    # Make sure the "id" column is an integer
    geoData.id = geoData.id.astype(str).astype(int)

    # Remove Alaska, Hawaii and Puerto Rico.
    stateToRemove = ['02', '15', '72']
    geoData = geoData[~geoData.STATE.isin(stateToRemove)]

    county_data = geoData[(geoData.STATE == state_id) & (geoData.COUNTY == county_id)]

    # partition a county into 10km * 10km grid
    geom = county_data.geometry.iloc[0]
    grid = geo_utils.partition(geom, 0.08)

    # get boundary info of grids
    boundary_array = []
    for i in range(len(grid)):
        lons, lats = grid[i].exterior.coords.xy
        lats = lats.tolist()
        lons = lons.tolist()
        array = np.array([lats[0], lons[0], lats[2], lons[2]])
        array = array.reshape((2, 2))
        boundary_array.append(array)

    return boundary_array


def get_county_name(state_id, county_id):
    """
    Return county name given FIPS code
    :param state_id: FIPS code for the state
    :param county_id: FIPS code for the county
    :return: county name
    """

    # csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input/US-counties.geojson')
    csv_path = "https://github.com/fudonglin/PyPI_resources/blob/main/cropnet/US-counties.geojson?raw=true"
    geoData = gpd.read_file(csv_path)

    # Make sure the "id" column is an integer
    geoData.id = geoData.id.astype(str).astype(int)

    # Remove Alaska, Hawaii and Puerto Rico.
    stateToRemove = ['02', '15', '72']
    geoData = geoData[~geoData.STATE.isin(stateToRemove)]

    county_data = geoData[(geoData.STATE == state_id) & (geoData.COUNTY == county_id)]

    return str(county_data.NAME.values[0])


def get_state_name(state_id):
    """
    Return state name given state FIPS code
    :param state_id: FIPS code for the state
    :return: state name
    """

    state_FIPS_dict = {"01": "ALABAMA",
                       "02": "ALASKA",
                       "04": "ARIZONA",
                       "05": "ARKANSAS",
                       "06": "CALIFORNIA",
                       "08": "COLORADO",
                       "09": "CONNECTICUT",
                       "10": "DELAWARE",
                       "11": "DISTRICT OF COLUMBIA",
                       "12": "FLORIDA",
                       "13": "GEORGIA",
                       "15": "HAWAII",
                       "16": "IDAHO",
                       "17": "ILLINOIS",
                       "18": "INDIANA",
                       "19": "IOWA",
                       "20": "KANSAS",
                       "21": "KENTUCKY",
                       "22": "LOUISIANA",
                       "23": "MAINE",
                       "24": "MARYLAND",
                       "25": "MASSACHUSETTS",
                       "26": "MICHIGAN",
                       "27": "MINNESOTA",
                       "28": "MISSISSIPPI",
                       "29": "MISSOURI",
                       "30": "MONTANA",
                       "31": "NEBRASKA",
                       "32": "NEVADA",
                       "33": "NEW HAMPSHIRE",
                       "34": "NEW JERSEY",
                       "35": "NEW MEXICO",
                       "36": "NEW YORK",
                       "37": "NORTH CAROLINA",
                       "38": "NORTH DAKOTA",
                       "39": "OHIO",
                       "40": "OKLAHOMA",
                       "41": "OREGON",
                       "42": "PENNSYLVANIA",
                       "44": "RHODE ISLAND",
                       "45": "SOUTH CAROLINA",
                       "46": "SOUTH DAKOTA",
                       "47": "TENNESSEE",
                       "48": "TEXAS",
                       "49": "UTAH",
                       "50": "VERMONT",
                       "51": "VIRGINIA",
                       "53": "WASHINGTON",
                       "54": "WEST VIRGINIA",
                       "55": "WISCONSIN",
                       "56": "WYOMING"}

    return state_FIPS_dict[state_id]


def build_request_oauth(oauth, url_request, headers_request, json_request, grid_num):
    """
    Send the oauth request for the image
    :param oauth: the oauth request
    :param url_request: the url to send the request to
    :param headers_request: the header of the request
    :param json_request: the json request
    :param grid_num: the grid number being requested
    :return:
    """

    # Send the request
    while True:
        try:
            response = oauth.request(
                "POST", url_request, headers=headers_request, json=json_request
            )

            img_np = np.array(Image.open(io.BytesIO(response.content)))

            return [img_np, grid_num]
        except Exception:
            # sleep for a second to avoid repeated issues
            time.sleep(1)


# function to process the images
def viz(client_id, client_secret, state, county, curr_date, target_dir, h5_file_name, img_type):
    """
    Get the images as an h5 file in the target directory
    :param: client_id: client id for sentinel hub
    :param: client_secret: client secret for sentinel hub
    :param state: FIPS code for the state
    :param county: FIPS code for the county
    :param curr_date: the date requested
    :param target_dir: the target directory
    :param h5_file_name: name for the h5 file with the images
    :param img_type: the image type
    :return:
    """

    oauth, token = get_token(client_id, client_secret)

    evalscript = build_evalscript(img_type)
    geometry_grids = build_geometry_grids(state, county)

    # Set the request url and headers
    url_request = 'https://services.sentinel-hub.com/api/v1/process'
    headers_request = {
        "Authorization": "Bearer %s" % token['access_token']
    }

    # iterate through the thread pool
    with ThreadPoolExecutor(max_workers=20) as exe:
        # submit the get_imagery requests
        futures = [exe.submit(
            build_request_oauth,
            oauth,
            url_request,
            headers_request,
            build_request_json(evalscript, geometry_grids[i]["geometry"], curr_date),
            i)
            for i in range(len(geometry_grids))]

        # make empty array to store images
        img_array = [None] * len(geometry_grids)

        # store images with grid # as index
        for _ in as_completed(futures):
            # convert from rgba image to rgb
            rgba_image = PIL.Image.fromarray(_.result()[0])
            rgb_image = rgba_image.convert('RGB')
            img_array[_.result()[1]] = np.array(rgb_image)

        hf = h5py.File(target_dir + '/' + h5_file_name, 'a')
        FIPS = state + county
        if FIPS not in hf.keys():
            # create a FIPS group
            grp = hf.create_group(FIPS)
        else:
            grp = hf[FIPS]

        if curr_date not in grp.keys():
            subgrp = grp.create_group(curr_date)
        else:
            subgrp = grp[curr_date]

        # create dataset in date group for img data
        dset = subgrp.create_dataset("data", data=img_array)

        # create dataset in date group for state
        dset = subgrp.create_dataset("state", data=get_state_name(state), shape=1)

        # create dataset in date group for county
        dset = subgrp.create_dataset("county", data=get_county_name(state, county).upper(), shape=1)

        # create dataset in date group for grid boundaries
        dset = subgrp.create_dataset("coordinates", data=get_grid_boundaries(str(FIPS[0:2]), str(FIPS[2:])))

        # close the h5 file
        hf.close()


def plot_image(image_arr):
    """
    Plot the image
    :param image_arr: the image data
    :return:
    """

    plt.figure(figsize=(8, 8))
    plt.axis('off')
    plt.tight_layout()
    plt.imshow(image_arr)
    plt.show()


def get_daterange(start_date, end_date, step):
    """
    Give the dates in a range
    :param start_date: start date
    :param end_date: end date
    :param step: increment in days
    :return:
    """
    while start_date <= end_date:
        yield start_date
        start_date += step


def get_previous_day(curr_date: str, delta: int, date_format: str = '%Y-%m-%d') -> str:
    """
    Get the previous day
    :param curr_date: current date
    :param delta: how many days to go back
    :param date_format: format of the dates
    :return: the previous day
    """

    curr_date = datetime.datetime.strptime(curr_date, date_format).date()
    prev_date = curr_date - timedelta(days=delta)
    prev_date = prev_date.strftime(date_format)
    return prev_date


def get_imagery(client_id, client_secret, target_dir, state, county, start_date, end_date, curr_date, img_type):
    """
    Get the imagery for a county for a period of days
    :param img_type: specify the type of image to download, i.e., ["AG", "NDVI"]
    :param: client_id: client id for sentinel hub
    :param: client_secret: client secret for sentinel hub
    :param target_dir: directory where data should be saved
    :param state: state FIPS code
    :param county: county FIPS code
    :param start_date: start date for the data
    :param end_date: end date for the data
    :param curr_date: the current date
    :return:
    """

    target_dir = target_dir + "/Sentinel/data"

    if img_type == "AG":
        path_dir = target_dir + "/AG/" + str(start_date.year) + '/' + get_state_abbr(state)
        # Use os.makedirs() to create the directories
        os.makedirs(path_dir, exist_ok=True)

        h5_file_path = "Agriculture" + "_" + state + "_" + get_state_abbr(state) + "_" + str(start_date) + "_" + str(
            end_date) + ".h5"
        viz(client_id, client_secret, state, county, curr_date, path_dir, h5_file_path, "Agriculture")

    elif img_type == "NDVI":
        path_dir = target_dir + "/NDVI/" + str(start_date.year) + '/' + get_state_abbr(state)
        # Use os.makedirs() to create the directories
        os.makedirs(path_dir, exist_ok=True)

        h5_file_path = "NDVI" + "_" + state + "_" + get_state_abbr(state) + "_" + str(start_date) + "_" + str(
            end_date) + ".h5"
        viz(client_id, client_secret, state, county, curr_date, path_dir, h5_file_path, "Vegetation Index")


def get_imagery_multithread(client_id, client_secret, target_dir, state, county, start_date, end_date, num_threads,
                            img_type):
    """
    Get the imagery for a county for a period of days with multithreading
    :param: client_id: client id for sentinel hub
    :param: client_secret: client secret for sentinel hub
    :param target_dir: directory where data should be saved
    :param state: state FIPS code
    :param county: county FIPS code
    :param start_date: start date for the data
    :param end_date: end date for the data
    :param num_threads: number of threads to use
    :return:
    """
    # array of dates to process
    date_array = []

    # create an array of dates to process
    for d in get_daterange(start_date, end_date, step=timedelta(days=1)):
        if (d.day == 1) or (d.day == 15):
            date_array.append(d)

    # number of iterations to fill progress bar
    length = len(date_array)
    # create the progress bar
    pbar = tqdm(total=length, desc='dates processed')  # Init pbar

    # iterate through the thread pool
    with ThreadPoolExecutor(max_workers=num_threads) as exe:
        # submit the get_imagery requests
        futures = [
            exe.submit(get_imagery, client_id, client_secret, target_dir, state, county, start_date, end_date, str(d),
                       img_type) for d in date_array]

        # update the progress bar as threads are completed
        for _ in as_completed(futures):
            pbar.update(n=1)


def get_county_images_date(client_id, client_secret, target_dir, num_threads, start_date, end_date, FIPS, img_type):
    """
    Get the imagery for a county for a period of days with multithreading efficiency
    :param: client_id: client id for sentinel hub
    :param: client_secret: client secret for sentinel hub
    :param target_dir: directory where data should be saved
    :param state: state FIPS code
    :param county: county FIPS code
    :param start_date: start date for the data
    :param end_date: end date for the data
    :param curr_date: the current date
    :return:
    """

    get_imagery_multithread(client_id, client_secret, target_dir, str(FIPS[0:2]), str(FIPS[2:]), start_date, end_date,
                            num_threads, img_type)


def get_county_images_seasonal(client_id, client_secret, target_dir, num_threads, FIPS_arr, year_array, img_type):
    """
    Get the imagery for an array of counties for an array of years
    :param: client_id: client id for sentinel hub
    :param: client_secret: client secret for sentinel hub
    :param target_dir: directory where data should be saved
    :param num_threads: the number of threads
    :param FIPS_arr: array of FIPS codes
    :param year_array: array of years
    :return:
    """

    for i, year in enumerate(year_array):
        for FIPS in FIPS_arr:
            year = int(year)

            print("Year Progress: [{} / {}], Downloading {}'s {} Imagery for the county {}"
                  .format(i + 1, len(year_array), year, img_type, FIPS))

            # winter season for the counties
            if is_before_end_of_current_quarter(date(year, 3, 31)):
                get_county_images_date(client_id, client_secret, target_dir, num_threads, date(year, 1, 1),
                                       date(year, 3, 31), FIPS, img_type)

            # spring season for all the counties
            if is_before_end_of_current_quarter(date(year, 6, 30)):
                get_county_images_date(client_id, client_secret, target_dir, num_threads, date(year, 4, 1),
                                       date(year, 6, 30), FIPS, img_type)

            # summer season for all the counties
            if is_before_end_of_current_quarter(date(year, 9, 30)):
                get_county_images_date(client_id, client_secret, target_dir, num_threads, date(year, 7, 1),
                                       date(year, 9, 30), FIPS, img_type)

            # fall season for all the counties
            if is_before_end_of_current_quarter(date(year, 12, 31)):
                get_county_images_date(client_id, client_secret, target_dir, num_threads, date(year, 10, 1),
                                       date(year, 12, 31), FIPS, img_type)


def get_counties(fips_state):
    """
    Get the counties in a particular state
    :param fips_state: FIPS code for the state
    :return: an array of counties in the state
    """

    # csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input/US-counties.geojson')

    csv_path = "https://github.com/fudonglin/PyPI_resources/blob/main/cropnet/US-counties.geojson?raw=true"
    geoData = gpd.read_file(csv_path)

    # geoData = gpd.read_file('./input/US-counties.geojson')

    # Make sure the "id" column is an integer
    geoData.id = geoData.id.astype(str).astype(int)

    # Remove Alaska, Hawaii and Puerto Rico.
    stateToRemove = ['02', '15', '72']
    geoData = geoData[~geoData.STATE.isin(stateToRemove)]

    county = geoData[(geoData.STATE == fips_state)].COUNTY
    county_val = county.values
    county = [int(l) for l in county_val]
    county = sorted(county)
    for i in range(len(county)):
        county[i] = str(county[i]).zfill(3)

    print(county)

    return county


def get_relevant_FIPS():
    """
    Get the state and county FIPS codes that are relevant to the model
    :return: state FIPS array and county FIPS array
    """

    df_relevant_fips = pandas.read_csv('relevant_counties.csv')
    states_fips = np.asarray(df_relevant_fips['state_ansi'].values)
    states_fips = [int(val) for val in states_fips]
    for i in range(len(states_fips)):
        states_fips[i] = str(states_fips[i]).zfill(2)

    counties_fips = np.asarray(df_relevant_fips['county_ansi'].values)
    counties_fips = [int(val) for val in counties_fips]
    for i in range(len(counties_fips)):
        counties_fips[i] = str(counties_fips[i]).zfill(3)

    return states_fips, counties_fips


def delete_fips(h5_file_path, fips):
    """
    Delete the data for a particular county in an h5 file
    :param h5_file_path: path to the h5 file
    :param fips: FIPS code of county to delete
    :return:
    """

    with h5py.File(h5_file_path, "a") as myfile:
        del myfile[fips]

        try:
            myfile[fips].value
        except KeyError as err:
            # print(err)
            pass
