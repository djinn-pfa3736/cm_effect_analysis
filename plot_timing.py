import pandas as pd
import numpy as np
import datetime

import matplotlib.pyplot as plt

import pdb

def convert_to_timestamp(date_str):
    year_str = date_str.split('T')[0]
    hour_str = date_str.split('T')[1]
    hour_str = hour_str.split('Z')[0]

    origin = datetime.datetime(1970, 1, 1)

    year = int(year_str.split('-')[0])
    month = int(year_str.split('-')[1])
    day = int(year_str.split('-')[2])
    hour = int(hour_str.split(':')[0])
    minute = int(hour_str.split(':')[1])
    second = int(hour_str.split(':')[2])
    current = datetime.datetime(year, month, day, hour, minute, second)

    delta = current - origin

    return delta.days*24*60*60 + delta.seconds

df = pd.read_csv("./query_20201105.csv")

occur_date_vec = []
male_date_vec = []
female_date_vec = []
for i in range(len(df)):
    tmp = convert_to_timestamp(df.iloc[i,3])
    occur_date_vec.append(tmp)
    if df.iloc[i,4] == 'male':
        male_date_vec.append(tmp)
    elif df.iloc[i,4] == 'female':
        female_date_vec.append(tmp)

occur_date_vec = np.array(occur_date_vec)
male_date_vec = np.array(male_date_vec)
female_date_vec = np.array(female_date_vec)

date_min = np.min(occur_date_vec)
date_vec = occur_date_vec - date_min
male_date_vec -= date_min
female_date_vec -= date_min

regist_timing_vec = np.zeros(np.max(date_vec) + 1)
regist_timing_vec[date_vec] = 1

gender_vec = np.array([""]*(np.max(date_vec) + 1))
gender_vec[male_date_vec] = "male"
gender_vec[female_date_vec] = "female"

cm_timing_df = pd.read_csv("cm_timing.csv", header=None)
timing_vec = []
for i in range(len(cm_timing_df)):
    tmp = convert_to_timestamp(cm_timing_df.iloc[i,0])
    timing_vec.append(tmp)
timing_vec = timing_vec - date_min

cm_timing_vec = np.zeros(np.max(date_vec) + 1)
cm_timing_vec[timing_vec] = np.sum(regist_timing_vec)
plot_start_idx = 19*10**5
plot_len = 9*10**5

regist_cum_vec = np.cumsum(regist_timing_vec[plot_start_idx:(plot_start_idx + plot_len)])
mean_slope = np.max(regist_cum_vec)/len(regist_cum_vec)
cm_timing_vec = cm_timing_vec[plot_start_idx:(plot_start_idx + plot_len)]
gender_vec = gender_vec[plot_start_idx:(plot_start_idx + plot_len)]

prev_regist = 0
interval = 0
slope_ratio_vec = []
male_count = 0
female_count = 0
male_count_vec = []
female_count_vec = []
total_male_count = 0
total_female_count = 0
for i in range(len(cm_timing_vec)):
    if cm_timing_vec[i] == 0:
        interval += 1
        if gender_vec[i] == 'm':
            male_count += 1
            total_male_count += 1
        elif gender_vec[i] == 'f':
            female_count += 1
            total_female_count += 1
    else:
        slope = (regist_cum_vec[i] - prev_regist)/interval
        slope_ratio_vec.append(slope/mean_slope)

        male_count_vec.append(male_count)
        female_count_vec.append(female_count)

        male_count = 0
        female_count = 0
        interval = 0
        prev_regist = regist_cum_vec[i]

slope_ratio_vec = np.array(slope_ratio_vec)
male_count_vec = np.array(male_count_vec)
female_count_vec = np.array(female_count_vec)

idx_vec = np.where(2.0 < slope_ratio_vec, True, False)
gender_ratio_vec = np.array(female_count_vec[idx_vec]/male_count_vec[idx_vec])

result_df = pd.DataFrame(np.vstack([cm_timing_df.iloc[0:(len(cm_timing_df)-1),0], slope_ratio_vec, male_count_vec, female_count_vec]))

pdb.set_trace()
