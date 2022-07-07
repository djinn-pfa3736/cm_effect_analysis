import pandas as pd
import numpy as np
import datetime

import matplotlib.pyplot as plt

import pdb

user_df = pd.read_csv('query_20201105.csv')

def convert_to_timestamp(date_str, adjust_flag):
    current = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')

    if adjust_flag:
        delta = datetime.timedelta(hours = 9)
        current = current + delta

    origin = datetime.datetime(1970, 1, 1)
    diff = current - origin

    return diff.days*24*60*60 + diff.seconds

# convert_to_timestamp(user_df.iloc[0,3], True)

regist_timestamp_vec = np.array([convert_to_timestamp(user_df.iloc[i,3], True) for i in range(len(user_df))])
regist_timing_vec = regist_timestamp_vec - np.min(regist_timestamp_vec)
regist_occur_vec = np.zeros(max(regist_timing_vec) + 1)
regist_occur_vec[regist_timing_vec] = 1

cm_df = pd.read_csv('cm_timing.csv', header=None)
cm_timestamp_vec = np.array([convert_to_timestamp(cm_df.iloc[i,0], False) for i in range(len(cm_df))])

origin = datetime.datetime(1970, 1, 1)
diff_timestamp = regist_timestamp_vec[0] % (24*60*60)
start_date_obj = datetime.timedelta(seconds=int(regist_timestamp_vec[0] - diff_timestamp)) + origin

# start_date = start_date_obj.day
# print(start_date_obj)
baseline_count_dict = {}
cm_count_dict = {}
for i in range(len(regist_timestamp_vec)):
    current = datetime.timedelta(seconds=int(regist_timestamp_vec[i])) + origin
    # print(current)
    if regist_timestamp_vec[i] < cm_timestamp_vec[0]:
        day_idx = (current - start_date_obj).days % 7
        if day_idx in baseline_count_dict:
            hour = current.hour
            baseline_count_dict[day_idx][hour] += 1
        else:
            hour = current.hour
            baseline_count_dict[day_idx] = np.zeros(24)
            baseline_count_dict[day_idx][hour] += 1
    elif (cm_timestamp_vec[0] <= regist_timestamp_vec[i]) and (regist_timestamp_vec[i] < cm_timestamp_vec[-1]):
        # day_idx = (current.day - start_date) % 7
        # print(current)
        day_idx = (current - start_date_obj).days % 7
        diff = current - start_date_obj
        # print(diff.days % 7)

        just_day_idx = current.day
        if day_idx in cm_count_dict:
            hour = current.hour
            if just_day_idx in cm_count_dict[day_idx]:
                cm_count_dict[day_idx][just_day_idx][hour] += 1
            else:
                cm_count_dict[day_idx][just_day_idx] = np.zeros(24)
                cm_count_dict[day_idx][just_day_idx][hour] += 1
        else:
            hour = current.hour
            cm_count_dict[day_idx] = {just_day_idx: np.zeros(24)}
            cm_count_dict[day_idx][just_day_idx][hour] += 1
    else:
        break

age_count = np.zeros(5)
for i in range(len(user_df)):
    # print(type(user_df.iloc[i,2]))
    if not isinstance(user_df.iloc[i,2], float):
        birthday_obj = datetime.datetime.strptime(user_df.iloc[i,2], "%Y-%m-%dT%H:%M:%S")
        regist_obj = datetime.datetime.strptime(user_df.iloc[i,3], '%Y-%m-%dT%H:%M:%SZ')

        delta = datetime.timedelta(hours = 9)
        regist_obj = regist_obj + delta

        diff = regist_obj.year - birthday_obj.year

        if diff <= 29:
            age_count[0] += 1
        elif diff <= 39:
            age_count[1] += 1
        elif diff <= 49:
            age_count[2] += 1
        elif diff <= 59:
            age_count[3] += 1
        elif diff <= 69:
            age_count[4] += 1

pdb.set_trace()
