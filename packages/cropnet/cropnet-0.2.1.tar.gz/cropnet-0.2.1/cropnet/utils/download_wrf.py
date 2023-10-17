import os
from herbie import Herbie
from datetime import datetime, timedelta
import urllib.error
import sys
from pathlib import Path


class DownloadWrfGrib2:
    def __init__(self):
        self.info = "Download hourly HRRR-WRF data for a select date range " \
                    "using Herbie. Download real time observation data and " \
                    "one hour prediction precipitation files."

        self.download_path = "wrf_files/"  # the desired path to download data

        self.begin_date = "20220101"  # format as "yyyymmdd"
        self.end_date = "20220102"  # NOT inclusive of last day

        self.start_hour = "00:00"  # desired hour to start download from
        self.end_hour = "01:00"  # format as "HH:MM". INCLUSIVE. max = '23:00'

        self.download_flag = 'both' # 'both', 'precip', 'realtime'

    def main(self):
        self.handle_args()
        dtobj = datetime.strptime(self.begin_date + " " + self.start_hour,
                                  "%Y%m%d %H:%M")
        end_dtobj = datetime.strptime(self.end_date + " " + self.end_hour,
                                      "%Y%m%d %H:%M")

        while dtobj.strftime("%Y%m%d") != end_dtobj.strftime("%Y%m%d"):
            if self.download_flag == 'both':
                self.real_time_download(dtobj)
                self.precip_download(dtobj)
            elif self.download_flag == 'precip':
                self.precip_download(dtobj)
            elif self.download_flag == 'realtime':
                self.real_time_download(dtobj)
            else:
                print("Wrong 'download_flag' given. Please enter one of the available options:\n"
                      "  'realtime' = download the full HRRR file for real time measurements\n"
                      "  'precip'   = download the one hour prediction files for precipitation\n"
                      "  'both'     = download both the realtime and one hour prediction of precipitation\n")
                exit()

            if dtobj.hour == end_dtobj.hour:
                hour, minute = map(int, self.start_hour.split(':'))
                dtobj = dtobj + timedelta(days=1)
                dtobj = dtobj.replace(hour=hour)

            dtobj = dtobj + timedelta(hours=1)

        self.cleanup()

    def handle_args(self):
        if len(sys.argv) > 1:
            for i in range(1, len(sys.argv)):

                if sys.argv[i] == "--begin_date":
                    self.begin_date = sys.argv[i+1]
                elif sys.argv[i] == "--end_date":
                    self.end_date = sys.argv[i+1]
                elif sys.argv[i] == "--start_hour":
                    self.start_hour = sys.argv[i+1]
                elif sys.argv[i] == "--end_hour":
                    self.end_hour = sys.argv[i+1]
                elif sys.argv[i] == "--download_path":
                    self.download_path = sys.argv[i+1]
                    
    def real_time_download(self, dtobj):
        herbo = None
        try:
            herbo = Herbie(dtobj, model='hrrr',
                           product='sfc', save_dir=self.download_path, verbose=True,
                           priority=['pando', 'pando2', 'aws', 'nomads',
                                     'google', 'azure'],
                           fxx=0,
                           overwrite=False)
        except:
            print("Could not find grib obj for date: %s" % dtobj.strftime("%Y%m%d"))

        if not herbo:
            print("Could not find grib object for date: %s" % dtobj.strftime("%Y%m%d"))
        else:
            try:
                herbo.download()
                # search through the dir, find the file, change the name
                download_dir = os.path.join(self.download_path, "hrrr/" + str(dtobj.strftime("%Y%m%d")) \
                               + '/')
                searchstring = 'hrrr.t' + str(dtobj.strftime("%H")) + 'z'
                new_file_path = os.path.join(self.download_path, "realtime_wrf/" + str(dtobj.year) + '/' \
                               + str(dtobj.strftime("%Y%m%d")) + '/')
                new_filename = new_file_path + 'hrrr.' + str(dtobj.strftime("%Y%m%d"))\
                               + '.' + str(dtobj.strftime("%H")) + '.00.grib2'

                for filename in os.listdir(download_dir):
                    full_path = os.path.join(download_dir, filename)

                    if searchstring in filename:
                        if not os.path.exists(new_file_path):
                            os.makedirs(new_file_path)
                        os.rename(full_path, new_filename)
            except:
                print("Could not download herbo for %s" % dtobj.strftime("%Y%m%d"))

    def precip_download(self, dtobj):
        herbo = None
        try:
            herbo = Herbie(dtobj, model='hrrr',
                           product='sfc', save_dir=self.download_path,
                           verbose=True,
                           priority=['pando', 'pando2', 'aws', 'nomads',
                                     'google', 'azure'],
                           fxx=1, overwrite=False)
        except:
            print("Could not find PRECIP grib for date %s" % dtobj.strftime("%Y%m%d"))

        if herbo:
            try:
                herbo.download(":APCP:surface")

                # search through the dir, find the file, change the name
                download_dir = os.path.join(self.download_path, "hrrr/" + str(dtobj.strftime("%Y%m%d")) \
                               + '/')
                searchstring = 'hrrr.t' + str(dtobj.strftime("%H")) + 'z'
                new_file_path = os.path.join(self.download_path, "precip_wrf/" + str(dtobj.year) + '/' \
                               + str(dtobj.strftime("%Y%m%d")) + '/')
                new_filename = new_file_path + 'hrrr.' + str(dtobj.strftime("%Y%m%d")) \
                               + '.' + str(dtobj.strftime("%H")) + '.00.grib2'

                for filename in os.listdir(download_dir):
                    full_path = os.path.join(download_dir, filename)

                    if searchstring in filename:
                        if not os.path.exists(new_file_path):
                            os.makedirs(new_file_path)
                        os.rename(full_path, new_filename)

            except ValueError:
                print("no herb obj for " + str(dtobj))
            except urllib.error.URLError:
                print("url error")

    def cleanup(self):
        directory = self.download_path + "hrrr"
        if os.path.isdir(directory):
            for root, dirs, files in os.walk(directory, topdown=False):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    os.rmdir(dir_path)
            os.rmdir(directory)


if __name__ == '__main__':
    d = DownloadWrfGrib2()
    d.main()
