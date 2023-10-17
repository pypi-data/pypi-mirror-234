# For more information, run "python extract_wrf_data.py -h" from terminal

import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import time
import sys
import os  
import cropnet.utils.geo_grid_recent as gg
from pathlib import Path
import threading
import multiprocessing
import logging
import warnings
import pygrib

# from queue import Queue
class PreprocessWRF:
    def __init__(self):
        #################################################################################################
        ################################### Initialization Parameters ###################################

        self.grib_path = "download/HRRR/wrf_files/realtime_wrf/" # path to the real-time wrf data
        self.precipitation_path = "download/HRRR/wrf_files/precip_wrf/" # path to the 1 hour predicted wrf
        self.write_path = "download/HRRR/extracted_data/" # path to write files to
        
        self.begin_date = "20220101"  # format as "yyyymmdd"
        self.end_date = "20220102" # NOT inclusive of the last day

        self.begin_hour = "00:00" # format as "HH:MM"
        self.end_hour = "01:00" # INCLUSIVE of the last hour (max = 23)

        self.max_workers = 5 # how many threads can run concurrently

        self.passedFips = ['36047', '36081'] # if not passing fips as arg. NEEDS TO BE STR
        
        #################################################################################################

        self.county_df = pd.DataFrame()

        self.lock = multiprocessing.Lock()
        self.herb_lock = multiprocessing.Lock()
        self.precip_lock = multiprocessing.Lock()

        self.extract_flag = True
        self.lat_dict = {}
        self.lon_dict = {}
        self.state_lon_lats = {}


    def main(self):
        start_time = time.time()
        # configure logging
        Path(self.write_path).mkdir(parents=True, exist_ok=True)
        logfilename = self.write_path + 'WRFextraction_' + self.begin_date + '-' + self.end_date + '.log'
        logging.basicConfig(filemode='w', filename=logfilename, format='%(levelname)s - %(message)s')
        #
       
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.handle_args(cur_dir)
        
        # wrfOutput_path = os.path.join(cur_dir, "input/wrfOutput.csv")

        wrfOutput_path = "https://github.com/fudonglin/PyPI_resources/blob/main/cropnet/wrfOutput.csv?raw=true"
        every_county_df = pd.read_csv(wrfOutput_path)

        param_dict_arr = self.separate_by_state(df=every_county_df)
        state_abbrev_df = self.get_state_abbrevs(cur_dir, df=every_county_df)
        
        every_county_df['county'] = every_county_df['county'].apply(self.fix_county_names)
        every_county_df['FIPS'] = every_county_df['FIPS'].apply(self.fix_county_fips)
        every_county_df['stateFips'] = every_county_df['stateFips'].apply(self.fix_state_fips)
        self.read_data(df=every_county_df, st_dict=param_dict_arr, state_abbrev_df=state_abbrev_df)

        # the data is read into hourly, stately files, now read them into daily / monthly files
        csvFiles = self.reopen_files()
        break_flag = False
        csvFile_idx = -1
        while not break_flag:
            tasks = []
            for i in range(0, self.max_workers):
                csvFile_idx += 1
                if csvFile_idx >= len(csvFiles):
                    break_flag = True
                    break
                file = csvFiles[csvFile_idx]
                # t = threading.Thread(target=self.monthly_file_threading, args=(file,))
                t = multiprocessing.Process(target=self.monthly_file_threading, args=(file,))
                tasks.append(t)
                t.start()

            for t in tasks:
                t.join()

        finish = time.time()
        print("\n\n------------- %s seconds ---------------" % (finish - start_time))

    def handle_args(self, cur_dir):
        if len(sys.argv) > 1:
            fips_flag = False
            fips_index = 0
            help_flag = False

            for i in range(1, len(sys.argv)):

                if sys.argv[i] == "--begin_date":
                    self.begin_date = sys.argv[i + 1]

                elif sys.argv[i] == "--end_date":
                    self.end_date = sys.argv[i + 1]

                elif sys.argv[i] == "--fips":
                    fips_flag = True
                    fips_index = i + 1

                elif sys.argv[i] == '-h' or sys.argv[i] == '--help':
                    help_flag = True
                    break

            if help_flag:
                print("This is a file to extract weather parameters from WRF-HRRR GRIB2 files for a select date\n"
                      "range from user specified counties / states. The argument list is as follows: \n\n"
                      "-h --help.......... Display this screen\n"
                      "--fips............. Pass one to a number of fips codes, separated by spaces\n"
                      "--fips state=...... Pass state abbreviations, will extract every county in the given\n"
                      "                    states. Separate states by commas. \n"
                      "                    Ex. --fips state=la,il,ms\n"
                      "                    Spaces are only allowed if the arg is inside quotes\n"
                      "                    Ex. --fips \"state=LA, MS, IL\"\n\n"
                      "Optionally, a user can also pass counties by their FIPS code through the\n"
                      "\"self.passed_fips\" variable included in the initialization parameters.\n\n"
                      "NOTE: County information is generated by the \"geo_grid_recent.py\" file and\n"
                       "is stored in the \"wrfoutput.csv\" file. To skip generation and keep the same info\n"
                       "in the wrfoutput.csv file, do not pass fips and empty the self.passed_fips array.\n")
                exit()

            if fips_flag:
                self.passedFips = []
                for i in range(fips_index, len(sys.argv)):
                    arg = sys.argv[i]
                    if arg.upper().rfind("STATE") != -1:
                        sep = arg.split('=')
                        states = sep[1].split(',')
                        for j in range(len(states)):
                            states[j] = states[j].strip()
                            states[j] = states[j].upper()
                            # print(states[j])
                        # all_county_path = os.path.join(cur_dir, "supplementary/countyFipsandCoordinates.csv")
                        # all_county_path = os.path.join(cur_dir, "input/countyFipsandCoordinates.csv")

                        all_county_path = "https://github.com/fudonglin/PyPI_resources/blob/main/cropnet/countyFipsandCoordinates.csv?raw=true"
                        all_county_df = pd.read_csv(all_county_path, dtype=str)

                        # state_abbrev_path = os.path.join(cur_dir, "input/us-state-ansi-fips2.csv")
                        # state_abbrev_path = os.path.join(cur_dir, "input/us-state-ansi-fips2.csv")

                        state_abbrev_path = "https://github.com/fudonglin/PyPI_resources/blob/main/cropnet/us-state-ansi-fips2.csv?raw=true"
                        state_abbrev_df = pd.read_csv(state_abbrev_path, dtype=str)
                        county_fips = []
                        for state in states:
                            this_state_fips = \
                                state_abbrev_df['st'].where(state_abbrev_df['stusps'] == state).dropna().values[0]
                            county_fips_from_state = all_county_df[
                                all_county_df['fips_code'].str.startswith(this_state_fips)]
                            county_fips_from_state = county_fips_from_state['fips_code'].dropna().values
                            county_fips.append(county_fips_from_state)
                        for arr in county_fips:
                            for val in arr:
                                self.passedFips.append(val)

                    else:
                        if len(arg) == 5:
                            # the correct length for a fips code
                            self.passedFips.append(arg)
                        else:
                            print("Error, the incorrect length of fips argument passed, please try again")
                            exit(0)
                gg.county(fips=self.passedFips, write_path='./')
            else: # if args have been passed, but not fips
                if len(self.passedFips) > 1:
                    # convert string of int
                    gg.county(fips=self.passedFips, write_path='./')
        else: # if no args have been passed
            if len(self.passedFips) > 1:
                gg.county(fips=self.passedFips, write_path='./')

    def separate_by_state(self, df=pd.DataFrame()):
        """

        :param df: a dataframe of fips codes and information obtained by running
                geo_grid
        :return: a dictionary, separated by state. Each state has its own dictionary of
                counties, each county has its own dictionary of parameter information
        """
        state_dict = {}
        for i in range(len(df)):
            if str(df['stateFips'][i]) not in state_dict:
                state_dict[str(df['stateFips'][i])] = {}
            if str(df['FIPS'][i]) not in state_dict[str(df['stateFips'][i])]:
                state_dict[str(df['stateFips'][i])][str(df['FIPS'][i])] = {}
            if str(df['countyGridIndex'][i]) not in state_dict[str(df['stateFips'][i])][str(df['FIPS'][i])]:
                state_dict[str(df['stateFips'][i])][str(df['FIPS'][i])][str(df['countyGridIndex'][i])] = []

        return state_dict

    def get_state_abbrevs(self, cur_dir, df=pd.DataFrame()):
        """
        Make a map of the states and their abbreviations
        :param df: data frame with the state info
        :return: df:: cols = ['stname', 'st', 'stusps'] where stname = full state name,
                     st = state fips and stusps = state abbreviation
        """

        # state_file_path = os.path.join(cur_dir, "supplementary/us-state-ansi-fips2.csv")

        # state_file_path = os.path.join(cur_dir, "input/us-state-ansi-fips2.csv")
        # state_abbrev_df = pd.read_csv(state_file_path, dtype=str)

        csv_path = "https://github.com/fudonglin/PyPI_resources/blob/main/cropnet/us-state-ansi-fips2.csv?raw=true"
        state_abbrev_df = pd.read_csv(csv_path, dtype=str)
        return state_abbrev_df

    def fix_county_names(self, val):
        # find the column for the county name
        # for each element, capitalize, and then if they have the term
        # 'PARISH' or 'COUNTY' then remove it
        val = val.upper()
        if val.rfind('COUNTY') != -1:
            arr = val.split(" COUNTY")
            val = ''
            for elem in arr:
                val += elem
        elif val.rfind('PARISH') != -1:
            arr = val.split(' PARISH')
            val = ''
            for elem in arr:
                val += elem
        val.strip()
        return val

    def fix_county_fips(self, val):
        """

        :param val: the county fips codes, need to be converted from str to int
        :return: a column of the dataframe
        """
        val = str(val)
        if 5 > len(val) > 3:
            # the val only has a length of 4, there's either an error, or there's
            # supposed to be a leading 0
            val = '0' + val
        if len(val) != 5:
            # something's wrong, exit
            print("Something went wrong while fixing the county FIPS codes to include a leading 0")
            exit()
        return val

    def fix_state_fips(self, val):
        val = str(val)
        if 2 > len(val) > 0:
            val = '0' + val
        if len(val) != 2:
            print("Something went wrong while fixing the state FIPS")
            exit()
        return val

    def read_data(self, df=pd.DataFrame(), st_dict={}, state_abbrev_df=pd.DataFrame()):
        """

        :param df: a df acting as the object, holding all of the
                information for all of the counties and their grid indexes
        :param dict: A dict that will hold a given hour's parameter information.
                dict[state][county][countyIndex] = One hour's parameters
        :return: Nun
        """

        # make dictonary of grid indexes and their avg lats and lons to put to find
        # closest points in grib files
        grid_names, lon_lats = self.make_lat_lon_name_arr(df=df)

        # for each hour in each day passed, try to read all the parameters that fudong needs
        # if the file cannot be found, then print a statement notifying the user and append 0s continue
        begin_day_dt = datetime.strptime(self.begin_date, "%Y%m%d")
        end_day_dt = datetime.strptime(self.end_date, "%Y%m%d")
        begin_hour_dt = datetime.strptime(self.begin_hour, "%H:%M")
        end_hour_dt = datetime.strptime(self.end_hour, "%H:%M")

        hour_range = (end_hour_dt - begin_hour_dt).seconds // (60 * 60) + 1
        date_range = (end_day_dt - begin_day_dt).days

        prev_month = ''

        for i in range(0, date_range):
            proc_start_time = time.time()
            break_flag = False
            hour_idx = -1
            while not break_flag:
                tasks = []
                for j in range(0, self.max_workers):
                    hour_idx += 1
                    if hour_idx >= hour_range:
                        break_flag = True
                        break

                    dtobj = begin_day_dt + timedelta(days=i, hours=hour_idx)
                    # if a new month is hit, we need to find the indexes of the closest points and
                    # store them in self.lat_dict and self.lon_dict
                    if dtobj.month != prev_month:
                        prev_month = dtobj.month
                        print("Getting Indexes for date %s" % dtobj.date())
                        self.get_nearest_indexes(dtobj, lon_lats)

                    t = multiprocessing.Process(target=self.r_w_weather_values, args=(dtobj, lon_lats, grid_names,
                                                                                      state_abbrev_df, df))
                    tasks.append(t)
                    t.start()

                for t in tasks:
                    t.join()

            print("------------------ Day's time = %s seconds --------------" % (time.time() - proc_start_time))

    def get_nearest_indexes(self, dtobj, lon_lats):
        # make ten tries, if no worky, exit
        grb = None
        for i in range(0, 10):
            dtobj = dtobj + timedelta(hours=i)
            filename = self.grib_path + dtobj.strftime("%Y") + '/' + dtobj.strftime("%Y%m%d") + '/' + 'hrrr.' + \
                       dtobj.strftime("%Y%m%d") + '.' + dtobj.strftime("%H") + '.00.grib2'
            try:
                grb = pygrib.open(filename)
                break
            except:
                grb = None

        if grb is None:
            print("ERROR: Could not find a suitable grib file to index the nearest points for date %s" % dtobj.date())
            exit()

        # now open it up, find the lat lons of the first layer, and try to find the nearest points
        lats = None
        lons = None
        for g in grb:
            try:
                lats, lons = g.latlons()
                break
            except:
                continue
        if len(lats) < 1 or len(lons) < 1:
            print("ERROR: when grabbing the latlons to do indexing for date %s" % dtobj.date())
            exit()
        grb.close()

        # now for each element in the latlons dicts, find the closest points
        for state in lon_lats:
            for county in lon_lats[state]:
                for idx in lon_lats[state][county]:
                    st_lon = idx[0]
                    st_lat = idx[1]
                    lat_m = np.full_like(lats, st_lat)
                    lon_m = np.full_like(lons, st_lon)
                    dis_m = (lats - lat_m) ** 2 + (lons - lon_m) ** 2
                    p_lat, p_lon = np.unravel_index(dis_m.argmin(), dis_m.shape)
                    self.lat_dict[state][county][idx] = p_lat
                    self.lon_dict[state][county][idx] = p_lon

    def r_w_weather_values(self, dtobj, lon_lats=[], grid_names=[], state_abbrev_df=pd.DataFrame(), df=pd.DataFrame()):
        logger = logging.getLogger()

        with self.herb_lock:
            try:
                filename = self.grib_path + dtobj.strftime("%Y") + '/' + dtobj.strftime("%Y%m%d") + '/' + 'hrrr.' +\
                           dtobj.strftime("%Y%m%d") + '.' + dtobj.strftime("%H") + '.00.grib2'
                grb = pygrib.open(filename)
            except:
                grb = None
        try:
            temp = grb.select(name='2 metre temperature')[0]
            temp_data = temp.values
        except:
            temp_data = None
            temp = None
            logger.warning("Temp vals not found for date %s" % (dtobj.strftime("%Y%m%d %H:%M")))
        try:
            rh = grb.select(name='2 metre relative humidity')[0]
            rh_data = rh.values
        except:
            rh_data = None
            logger.warning("RH vals not found for date %s" % (dtobj.strftime("%Y%m%d %H:%M")))
        try:
            dswrf = grb.select(name='Downward short-wave radiation flux')[0]
            dswrf_data = dswrf.values
        except:
            dswrf_data = None
            logger.warning("DSWRF vals not found for date %s" % (dtobj.strftime("%Y%m%d %H:%M")))
        try:
            u_wind = grb.select(name='U component of wind', level=1000)[0]
            v_wind = grb.select(name='V component of wind', level=1000)[0]
            u_data = u_wind.values
            v_data = v_wind.values
        except:
            u_data = None
            v_data = None
            logger.warning("Wind dir vals not found for date %s " % (dtobj.strftime("%Y%m%d %H:%M")))
        try:
            gust = grb.select(name='Wind speed (gust)')[0]
            gust_data = gust.values
        except:
            gust_data = None
            logger.warning("Wind Gust vals not found for date %s" % (dtobj.strftime("%Y%m%d %H:%M")))

        try:
            grb.close()
        except:
            logger.warning("Grib obj not closed for date %s" % (dtobj.strftime("%Y%m%d %H:%M")))

        #################
         # grab the precip
        ###################
        with self.precip_lock:
            try:
                precip_herb_path = self.precipitation_path + "hrrr/" + dtobj.strftime("%Y%m%d") + '/'
                precip_herb = None
                for file in sorted(os.listdir(precip_herb_path)):
                    if file.rfind("hrrr.t" + dtobj.strftime("%H")) != -1:
                        precip_herb = file
                        break
                precip_herb_path += precip_herb
                precip_grb = pygrib.open(precip_herb_path)
                precip_data = precip_grb.select(name="Total Precipitation")[0]
                precip_data = precip_data.values
                precip_grb.close()
            except:
                precip_data = np.full_like(temp_data, 0)
                logger.warning("Precip values not found for %s" % dtobj.strftime("%Y%m%d %H%M"))

        for state in lon_lats:
            # for each state, find the precipitation value (to save time)
            for county in lon_lats[state]:
                count = -1
                for idx in lon_lats[state][county]:
                    count += 1
                    try:
                        temp_value = temp_data[self.lat_dict[state][county][idx], self.lon_dict[state][county][idx]]
                    except:
                        temp_value = -12345.678
                    try:
                        rh_value = rh_data[self.lat_dict[state][county][idx], self.lon_dict[state][county][idx]]
                    except:
                        rh_value = -12345.678
                    try:
                        dswrf_value = dswrf_data[self.lat_dict[state][county][idx], self.lon_dict[state][county][idx]]
                    except:
                        dswrf_value = 0
                    try:
                        u_value = u_data[self.lat_dict[state][county][idx], self.lon_dict[state][county][idx]]
                        v_value = v_data[self.lat_dict[state][county][idx], self.lon_dict[state][county][idx]]
                    except:
                        u_value = -12345.678
                        v_value = -12345.678
                    try:
                        gust_value = gust_data[self.lat_dict[state][county][idx], self.lon_dict[state][county][idx]]
                    except:
                        gust_value = 0
                    try:
                        precip_value = precip_data[self.lat_dict[state][county][idx], self.lon_dict[state][county][idx]]
                    except:
                        precip_value = 0

                    # state = state fips code , county = county fips code, idx = lon, lat
                    # if we can also loop through the grid_names, we may be able to get the GridIdx
                    # grid_names[state][county][count] = countyFips_GridIdx
                    countyFips_GridIdx = grid_names[state][county][count].split('_')
                    county_fips = str(countyFips_GridIdx[0])
                    grid_Idx = countyFips_GridIdx[1]
                    state_fips = str(county_fips[0:2])
                    try:
                        state_abbrev = \
                            state_abbrev_df['stusps'].where(state_abbrev_df['st'] == state_fips).dropna().values[0]
                    except:
                        print("State abbrev for fips %s Grid Idx %s could not be found, skipping." % (county_fips,
                                                                                                      grid_Idx))
                        continue
                    state_name = \
                        state_abbrev_df['stname'].where(state_abbrev_df['st'] == state_fips).dropna().values[0]
                    county_name = df['county'].where(df['FIPS'] == str(county_fips)).dropna().values[0]
                    df_idx = df.index[
                        (df['FIPS'] == str(county_fips)) & (df['countyGridIndex'] == int(grid_Idx))].tolist()[
                        0]
                    row = [dtobj.strftime("%Y"), dtobj.strftime("%m"), dtobj.strftime("%d"), dtobj.strftime("%H"),
                           'Daily', state_name.upper(), county_name, county_fips, grid_Idx, df['lat (llcrnr)'][df_idx],
                           df['lon (llcrnr)'][df_idx], df['lat (urcrnr)'][df_idx], df['lon (urcrnr)'][df_idx],
                           temp_value, precip_value, rh_value, gust_value, u_value, v_value, dswrf_value]

                    with self.lock:
                        self.write_dict_row(row=row, state_abbrev=state_abbrev)

        print("Grabbed data for " + dtobj.strftime("%Y%m%d %H:%M"))

    def make_lat_lon_name_arr(self, df=pd.DataFrame()):
        """

        :param df: the dataframe of the station data
        :return: a dictionary, key=grid_county_name , val = tuple of avglon, avglat
        """
        names = {}
        lon_lats = {}
        for i in range(len(df)):
            state_fips = str(df['stateFips'][i])
            county_fips = str(df['FIPS'][i])
            grid_county_name = str(df['FIPS'][i]) + '_' + str(df['countyGridIndex'][i])
            avg_lon = (float(df['lon (urcrnr)'][i]) + float(df['lon (llcrnr)'][i])) / 2
            avg_lat = (float(df['lat (urcrnr)'][i]) + float(df['lat (llcrnr)'][i])) / 2

            if state_fips not in names:
                names[state_fips] = {}
                lon_lats[state_fips] = {}
                self.lon_dict[state_fips] = {}
                self.lat_dict[state_fips] = {}
                self.state_lon_lats[state_fips] = []

            if county_fips not in names[state_fips]:
                names[state_fips][county_fips] = []
                lon_lats[state_fips][county_fips] = []
                self.lat_dict[state_fips][county_fips] = {}
                self.lon_dict[state_fips][county_fips] = {}

            names[state_fips][county_fips].append(grid_county_name)
            lon_lats[state_fips][county_fips].append((avg_lon, avg_lat))
            self.lat_dict[state_fips][county_fips][grid_county_name] = []
            self.lon_dict[state_fips][county_fips][grid_county_name] = []
            self.state_lon_lats[state_fips].append((avg_lon, avg_lat))

        return names, lon_lats

    def write_dict_row(self, row=[], state_abbrev=''):
        """

        :param row: a single row from a dictionary, containing all the necessary information
                    to find the file
        :return: nadda
        """
        # find the right file that we needa write to
        # write path + daily_data + year + state_abbrev + countyFips + monthly file
        # <HRRR_<state_fips>_<state_abbrev>_<year>-<month>>.csv
        year = row[0]
        state_name = row[5]
        month = row[1]
        county_fips = row[7]
        state_fips = county_fips[0:2]
        # output_directory = self.write_path + "daily_data/" + year + '/' + state_abbrev + '/'
        output_directory = os.path.join(self.write_path, "daily_data/" + year + '/' + state_abbrev + '/')
        # if it does not already exist, make it
        Path(output_directory).mkdir(parents=True, exist_ok=True)
        output_file_path = output_directory + "HRRR_" + state_fips + '_' + state_abbrev + '_' + year \
                           + '-' + month + '.csv'
        # if the file does not already exist, write the appropriate header out to it
        if not os.path.exists(output_file_path):
            # make the file
            f = open(output_file_path, mode='wt')
            f.write('Year,Month,Day,Hour,Daily/Monthly,State,County,FIPS Code,Grid Index,' +
                    'Lat (llcrnr),Lon (llcrnr),Lat (urcrnr),Lon (urcrnr),Avg Temperature (K),' +
                    'Precipitation (kg m**-2),Relative Humidity (%),Wind Gust (m s**-1),' +
                    'U Component of Wind (m s**-1),V Component of Wind (m s**-1),' +
                    'Downward Shortwave Radiation Flux (W m**-2)\n')
            f.close()
        # now we are free to write out the appropriate information to it
        f = open(output_file_path, mode='a')
        for r in row:
            f.write(str(r) + ',')
        f.write('\n')
        f.close()

    def reopen_files(self):
        csvFiles = []
        directory = self.write_path + "daily_data/"
        for year_folders in sorted(os.listdir(directory)):
            year_path = directory + year_folders + '/'
            if not os.path.isdir(year_path):
                continue
            for state in sorted(os.listdir(year_path)):
                state_path = year_path + state + '/'
                for file in sorted(os.listdir(state_path)):
                    full_path = state_path + file
                    csvFiles.append(full_path)

        return csvFiles

    def monthly_file_threading(self, file):
        print("Get Monthly Avg for %s" % file)
        df = pd.read_csv(file, index_col=False, na_filter=False, na_values='N/A')
        df = self.wind_speed_vpd(df=df)
        df = self.dailyAvgMinMax(df=df)
        df = self.monthlyAvgs(df=df)
        self.final_sendoff(df=df, fullfilepath=file)

    def wind_speed_vpd(self, df=pd.DataFrame()):
        """
               turn the columns for U comp and V comp of wind
               into numpy ndarrays, then feed into the get_wind_speed
               functions. delete the U comp and V comp columns, make a new
               column "Wind Speed(m s**-1)" and put the return value as the
               values of the column

               turn the columns for temperature and humidity into numpy
               ndarrays, then feed into get_vpd function, make a new
               column "Vapor Pressure Deficit (kPa)" and put the return
               value as the values of the column
        """
        u_comp_wind = df['U Component of Wind (m s**-1)']
        u_comp_wind.replace(-12345.678, np.nan, inplace=True)
        u_comp_wind.ffill(inplace=True)
        u_comp_wind.bfill(inplace=True)
        u_comp_wind = u_comp_wind.to_numpy().astype(dtype=float)
        df['U Component of Wind (m s**-1)'] = u_comp_wind

        v_comp_wind = df['V Component of Wind (m s**-1)']
        v_comp_wind.replace(-12345.678, np.nan, inplace=True)
        v_comp_wind.ffill(inplace=True)
        v_comp_wind.bfill(inplace=True)
        v_comp_wind = v_comp_wind.to_numpy().astype(dtype=float)
        df['V Component of Wind (m s**-1)'] = v_comp_wind

        temp = df['Avg Temperature (K)']
        temp.replace(-12345.678, np.nan, inplace=True)
        temp.ffill(inplace=True)
        temp.bfill(inplace=True)
        temp = temp.to_numpy().astype(dtype=float)
        df['Avg Temperature (K)'] = temp

        relh = df['Relative Humidity (%)']
        relh.replace(-12345.678, np.nan, inplace=True)
        relh.ffill(inplace=True)
        relh.bfill(inplace=True)
        relh = relh.to_numpy().astype(dtype=float)
        df['Relative Humidity (%)'] = relh

        wind_speed = self.get_wind_speed(u_comp_wind, v_comp_wind)
        df['Wind Speed (m s**-1)'] = wind_speed

        vpd = self.get_VPD(temp, relh)
        df['Vapor Pressure Deficit (kPa)'] = vpd

        return df

    def get_wind_speed(self, U: np.ndarray, V: np.ndarray) -> np.ndarray:
        '''
        Calculate the average wind speed
        :param U: array_like, U component of wind in 1000 hPa (i.e., layer 32 in HRRR)
        :param V: array_like, V component of wind in 1000 hPa (i.e., layer 32 in HRRR)
        :return:
        '''
        return np.sqrt(np.power(U, 2) + np.power(V, 2))

    def get_VPD(self, T: np.ndarray, RH: np.ndarray) -> np.ndarray:
        '''
        Calculate the Vapor Pressure Deficit (VPD), unit: kPa
        :param T: array_like, temperate (unit: K) at 2 metre (layer 54 in HRRR)
        :param RH: array_like, relative humidity at 2 metre (i.e., layer 58 in HRRR)
        :return:
        '''

        # covert the temperature in Kelvin to the temperature in Celsius
        T = T - 273.15
        E = 7.5 * T / (237.3 + T)
        VP_sat = 610.7 * np.power(10, E) / 1000
        VP_air = VP_sat * RH / 100
        VPD = VP_sat - VP_air

        return VPD

    def dailyAvgMinMax(self, df=pd.DataFrame()):
        df.drop(columns='Hour', inplace=True)
        df.sort_values(['Day'], inplace=True)
        dftoreturn = pd.DataFrame(columns=list(df.columns))
        # dftoreturn.drop(columns='Hour', inplace=True)
        # print(df)
        for col in dftoreturn:
            if col == 'Avg Temperature (K)':
                # need to insert new columns at index of temperature
                index = dftoreturn.columns.get_loc(col)
                dftoreturn.insert(index + 1, "Max Temperature (K)", value=None, allow_duplicates=True)
                dftoreturn.insert(index + 1, "Min Temperature (K)", value=None, allow_duplicates=True)
        # print(list(dftoreturn.columns))
        ##########################################
        # look for a more efficient way to do this
        ##########################################
        grouped_counties = df.groupby(df['County'])
        for county in grouped_counties:
            countydf = pd.DataFrame(county[1])
            grouped_gridindex = countydf.groupby(df['Grid Index'])

            # for each station df
            for gridgroupdf in grouped_gridindex:
                # print(gridgroupdf[1])
                gridindexDf = pd.DataFrame(gridgroupdf[1])
                # print(gridindexDf)
                grouped_day = gridindexDf.groupby(gridindexDf.Day)

                # for each day in each station
                for group in grouped_day:
                    try:
                        current_day = group[0]
                        station_dayDf = pd.DataFrame(group[1])
                    except:
                        print("Did not grab grouped_day.get_group(%s)" % (group))
                        continue
                    avgedRow = []
                    # print(station_dayDf)

                    for col in station_dayDf:
                        if col.rfind('Year') != -1 or col.rfind('Month') != -1 or col.rfind(
                                'Day') != -1 or col.rfind(
                            'State') != -1 or col.rfind('County') != -1 or col.rfind(
                            'Grid Index') != -1 or col.rfind(
                            'FIPS Code') != -1 or col.rfind('Lat (') != -1 or col.rfind('Lon (') != -1:
                            avgedRow.append(station_dayDf[col].iloc[0])
                            # avgedRow.concat()
                            # pd.concat([avgedRow, station_dayDf[col].iloc[0]], ignore_index=True)
                        elif col.rfind('Precipitation') != -1 or col.rfind('adiation') != -1:
                            avgedRow.append(station_dayDf[col].sum())
                        else:
                            # get the average of the row and append it to the avg list
                            try:
                                avgedRow.append(station_dayDf[col].mean())
                            except:
                                avgedRow.append('NaN')
                            # if the column is temperature, find the min, max, then append
                            if col == 'Avg Temperature (K)':
                                avgedRow.append(station_dayDf[col].min())
                                avgedRow.append(station_dayDf[col].max())

                    # now that all the columns have been collected, we need to append the row to the dftoreturn
                    dftoreturn.loc[len(dftoreturn)] = avgedRow
        return dftoreturn

    def monthlyAvgs(self, df=pd.DataFrame()):
        """
        This function will find the monthly average for each county.
        """
        df = df[['Year', 'Month', 'Day', 'Daily/Monthly', 'State', 'County', 'FIPS Code', 'Grid Index',
                 'Lat (llcrnr)', 'Lon (llcrnr)', 'Lat (urcrnr)', 'Lon (urcrnr)',
                 'Avg Temperature (K)', 'Max Temperature (K)', 'Min Temperature (K)', 'Precipitation (kg m**-2)',
                 'Relative Humidity (%)', 'Wind Gust (m s**-1)', 'Wind Speed (m s**-1)',
                 'U Component of Wind (m s**-1)', 'V Component of Wind (m s**-1)',
                 'Downward Shortwave Radiation Flux (W m**-2)', 'Vapor Pressure Deficit (kPa)']]

        ##################################################################
        # fudongs code
        df = df.drop(df.index[(df["Daily/Monthly"] == "Monthly")])

        grouped_df = df.groupby('FIPS Code')

        # calculate the mean value
        columns_to_average = ['Avg Temperature (K)', 'Max Temperature (K)', 'Min Temperature (K)',
                              'Precipitation (kg m**-2)',
                              'Relative Humidity (%)', 'Wind Gust (m s**-1)', 'Wind Speed (m s**-1)',
                              'U Component of Wind (m s**-1)', 'V Component of Wind (m s**-1)',
                              'Downward Shortwave Radiation Flux (W m**-2)',
                              'Vapor Pressure Deficit (kPa)']
        average_values = grouped_df[columns_to_average].mean()

        data = []
        for i, (fips, rows) in enumerate(grouped_df):
            data1 = rows.iloc[:1].copy()
            data.append(data1)

        data = pd.concat(data)
        data = data[
            ['Year', 'Month', 'Day', 'Daily/Monthly', 'State', 'County', 'FIPS Code', 'Grid Index',
             'Lat (llcrnr)', 'Lon (llcrnr)', 'Lat (urcrnr)', 'Lon (urcrnr)']
        ]

        # replace the mean parameters
        merged = data.merge(average_values, how='outer', left_on=["FIPS Code"], right_on=["FIPS Code"])

        # update default columns
        merged['Day'] = "N/A"
        merged['Daily/Monthly'] = 'Monthly'
        merged['Grid Index'] = "N/A"
        merged['Lat (llcrnr)'] = "N/A"
        merged['Lon (llcrnr)'] = "N/A"
        merged['Lat (urcrnr)'] = "N/A"
        merged['Lon (urcrnr)'] = "N/A"

        # append monthly parameters to csv
        df = pd.concat([df, merged], ignore_index=True)

        # convert fips code to string
        df['FIPS Code'] = df['FIPS Code'].astype('Int64').astype('str').str.zfill(5)
        #################################################################
        for col in df:
            if col.rfind('elative Hum') != -1:
                df[col] = df[col].round(decimals=1)
                continue
            try:
                df[col] = df[col].round(decimals=3)
            except:
                continue

        return df

    def final_sendoff(self, df=pd.DataFrame(), fullfilepath=''):
        fullpathsep = fullfilepath.split('/')
        newfilepath = ''
        state_abbrev = ''
        year = ''
        for i in range(len(fullpathsep)):
            if fullpathsep[i].rfind('daily_data') != -1:
                state_abbrev = fullpathsep[i + 2]
                year = fullpathsep[i + 1]
                break
            newfilepath += fullpathsep[i] + '/'
        newfilepath += "data/" + year + '/' + state_abbrev + '/'
        Path(newfilepath).mkdir(parents=True, exist_ok=True)
        write_path = newfilepath + fullpathsep[len(fullpathsep) - 1]
        df.to_csv(write_path, index=False)
        return


if __name__ == "__main__":
    warnings.filterwarnings("ignore", message=".*More than one.*")
    warnings.filterwarnings("ignore", message=".*This pattern is interpreted as a regular expression,.*")
    warnings.filterwarnings("ignore", message=".*The default dtype for empty Series.*")
    warnings.filterwarnings("ignore", message=".*In a future version,.*")
    warnings.filterwarnings("ignore", message=".*SettingWithCopy.*")
    warnings.filterwarnings("ignore", message=".*See the caveats.*")
    p = PreprocessWRF()
    p.main()
