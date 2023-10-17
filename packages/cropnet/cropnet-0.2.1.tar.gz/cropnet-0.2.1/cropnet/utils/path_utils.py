import os
import datetime


def create_directories_if_not_exist(file_path):
    """
    Create directories if they do not exist
    :param file_path:
    :return:
    """
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)


def get_state_abbr(state_id):
    """
    Return state abbreviation given state FIPS code
    :param state_id: FIPS code for the state
    :return: state abbreviation
    """

    state_FIPS_dict = {"01": "AL",
                       "02": "AK",
                       "04": "AZ",
                       "05": "AR",
                       "06": "CA",
                       "08": "CO",
                       "09": "CT",
                       "10": "DE",
                       "11": "DC",
                       "12": "FL",
                       "13": "GA",
                       "15": "HI",
                       "16": "ID",
                       "17": "IL",
                       "18": "IN",
                       "19": "IA",
                       "20": "KS",
                       "21": "KY",
                       "22": "LA",
                       "23": "ME",
                       "24": "MD",
                       "25": "MA",
                       "26": "MI",
                       "27": "MN",
                       "28": "MS",
                       "29": "MO",
                       "30": "MT",
                       "31": "NE",
                       "32": "NV",
                       "33": "NH",
                       "34": "NJ",
                       "35": "NM",
                       "36": "NY",
                       "37": "NC",
                       "38": "ND",
                       "39": "OH",
                       "40": "OK",
                       "41": "OR",
                       "42": "PA",
                       "44": "RI",
                       "45": "SC",
                       "46": "SD",
                       "47": "TN",
                       "48": "TX",
                       "49": "UT",
                       "50": "VT",
                       "51": "VA",
                       "53": "WA",
                       "54": "WV",
                       "55": "WI",
                       "56": "WY"}

    return state_FIPS_dict[state_id]


def get_quarter(date):
    month = date.month

    if 1 <= month <= 3:
        return 1
    elif 4 <= month <= 6:
        return 2
    elif 7 <= month <= 9:
        return 3
    else:  # October, November, December
        return 4


def is_before_end_of_current_quarter(given_day):
    today = datetime.date.today()
    current_quarter = get_quarter(today)

    if current_quarter == 1:
        end_of_curr_quarter = datetime.date(today.year, 3, 31)
    elif current_quarter == 2:
        end_of_curr_quarter = datetime.date(today.year, 6, 30)
    elif current_quarter == 3:
        end_of_curr_quarter = datetime.date(today.year, 9, 30)
    else:  # Quarter 4
        end_of_curr_quarter = datetime.date(today.year, 12, 31)

    return given_day < end_of_curr_quarter
