import pandas as pd
import numpy as np
#import heartpy as hp
from matplotlib import pyplot as plt
from scipy.signal import medfilt
import json
import datetime
import os
import time

def get_time_domain_features(nn_intervals) -> dict:
    # nn_intervals(ms) => 60000/bpm

    # nn intervals의 차이 (각 인접한 다음 nn interval의 차)
    diff_nni = np.diff(nn_intervals)
    # 데이터 길이
    length_int = len(nn_intervals)

    # Basic statistics
    # 
    mean_nni = np.mean(nn_intervals)
    median_nni = np.median(nn_intervals)
    range_nni = max(nn_intervals) - min(nn_intervals)

    sdsd = np.std(diff_nni)
    rmssd = np.sqrt(np.mean(diff_nni ** 2))

    nni_50 = sum(np.abs(diff_nni) > 50)
    pnni_50 = 100 * nni_50 / length_int
    nni_20 = sum(np.abs(diff_nni) > 20)
    pnni_20 = 100 * nni_20 / length_int
    rmssd = np.sqrt(np.mean(np.square(np.diff(nn_intervals))))

    # Feature found on github and not in documentation
    cvsd = rmssd / mean_nni

    # Features only for long term recordings
    sdnn = np.std(nn_intervals, ddof=1)  # ddof = 1 : unbiased estimator => divide std by n-1
    cvnni = sdnn / mean_nni

    # Heart Rate equivalent features, heart_rate => bpm
    heart_rate_list = np.divide(60000, nn_intervals)
    mean_hr = np.mean(heart_rate_list)
    min_hr = min(heart_rate_list)
    max_hr = max(heart_rate_list)
    std_hr = np.std(heart_rate_list)

    time_domain_features = {
        'mean_nni': mean_nni,
        'rmssd': rmssd,
        'sdnn': sdnn,
        'sdsd': sdsd,
        'nni_50': nni_50,
        'pnni_50': pnni_50,
        'nni_20': nni_20,
        'pnni_20': pnni_20,
        'rmssd': rmssd,
        'median_nni': median_nni,
        'range_nni': range_nni,
        'cvsd': cvsd,
        'cvnni': cvnni,
        'mean_hr': mean_hr,
        "max_hr": max_hr,
        "min_hr": min_hr,
        "std_hr": std_hr,
    }

    return time_domain_features

def date_conv(date_str):
    return '20' + date_str[:2] + '-' + date_str[2:4] + '-' + date_str[4:]

def hrv_stress(hrv_dict_):
    sdnn_max = 100
    sdnn_min = 0
    rmssd_max = 100
    rmssd_min = 0
    
    # SDNN 스트레스 계산
    sdnn_score = (hrv_dict_['sdnn'] - sdnn_min) / (sdnn_max - sdnn_min)
    sdnn_stress_score = max(0, min(10, 10 * sdnn_score))
    
    return sdnn_stress_score

def bind_hours(df_):
    cnt = 1
    cnt_ = 0
    hours_cnt = 0
    flags = 0
    time_idx = 0
    res_list = []
    #df.loc[0] = {'endTime':'2009-01-01 15:59:00', 'bpm':40}
    df_ = pd.concat([pd.Series({'endTime':'2009-01-01 15:58:00+09:00', 'bpm':40}).to_frame().T, df_], ignore_index=True)
    #df_ = pd.concat([pd.Series({'endTime':'2009-01-01 15:59:00+09:00', 'bpm':40}).to_frame().T, df_], ignore_index=True)
    #print(df_)
    while True:
        cnt += 1
        time_idx += 1
        if cnt + 1 > len(df_) - 1:
            if len(df_[cnt_:cnt]) == 60:
                res_list.append(df_[cnt_:cnt].reset_index(drop=True))
            break
        if str(df_['endTime'][cnt-1])[-11:-9] == '00':
            time_idx = cnt - 1
            if pd.to_datetime(df_['endTime'][cnt]) - pd.to_datetime(df_['endTime'][time_idx]) == datetime.timedelta(minutes=1):
                cnt_ = time_idx
                while True:
                    if cnt + 1 > len(df_) - 1:
                        if len(df_[cnt_:cnt]) == 60:
                            res_list.append(df_[cnt_:cnt].reset_index(drop=True))
                        break
                    cnt += 1
                    if pd.to_datetime(df_['endTime'][cnt]) - pd.to_datetime(df_['endTime'][cnt-1]) != datetime.timedelta(minutes=1):
                        break
                    if pd.to_datetime(df_['endTime'][cnt]) - pd.to_datetime(df_['endTime'][cnt_]) == datetime.timedelta(hours=1):
                        res_list.append(df_[cnt_:cnt].reset_index(drop=True))
                        hours_cnt += 1
                        cnt -= 1
                        break
                    else:
                        continue

    return res_list

def stress_plot(stress_list):
    str_date = stress_list[0][0][:10]
    date = []
    date_stress = []
    for i in range(len(stress_list)):
        if str_date in stress_list[i][0]:
            date.append(stress_list[i][0][:16])
            date_stress.append(stress_list[i][1])
    res = [date, date_stress]
    plt.figure(figsize=(14,7))
    plt.axhspan(0, 3, color='blue', alpha=0.3)
    plt.axhspan(3, 7, color='green', alpha=0.3)
    plt.axhspan(7, 10, color='red', alpha=0.3)
    plt.ylim(0,10)
    plt.plot(res[0], res[1], label='Stress', marker='x', color='r')
    plt.title(f'{str_date} Stress Score')
    plt.xlabel('Date')
    plt.ylabel('Score')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # 이미지 저장
    plt.savefig(f'C:/Users/AIA01/Desktop/project/PNUh/pnuh_page/hrv_proc/stress_score_{str_date}.png')
    #plt.show()

###################################################################
# 홍소장님이 나중에 json 파일로 db에 올린다고 하셨기에, 필요 없을 예정 #
with open('C:/Users/AIA01/Desktop/project/PNUh/pnuh_page/hrv_proc/health_data_HeartRateRecord_20240416_154527.json') as f:
    j_data = json.load(f)
        
endtime_ = []
bpm_ = []

for i in range(len(j_data)):
    endtime_.append(pd.to_datetime(j_data[i]['endTime']))
    bpm_.append(j_data[i]['samples'][0]['beatsPerMinute'])
    
hrv_data = {
    'endTime' : endtime_,
    'bpm' : bpm_
}

df_min = pd.DataFrame(hrv_data)
df_min.drop_duplicates(ignore_index=True, inplace=True)
####################################################################

while True:
    #if time.time
    
    # ex) 240331_hrvs.txt -> 240331
    json_file = [x for x in os.listdir('C:/Users/AIA01/Desktop/project/PNUh/pnuh_page/hrv_proc/') if '_hrvs' in x]
    temp_date = json_file[0][:6]
    # ex) 24-03-31
    date_hrv = date_conv(temp_date)
    
    df = df_min.loc[df_min['endTime'].dt.date.astype(str).str.contains(date_hrv), :]
    df.drop_duplicates(ignore_index=True, inplace=True)
    
    df_hours = bind_hours(df)
    
    
    
    hrv_feature = get_time_domain_features(df['bpm'])
    time_hrv_data = []
    for i in range(len(df_hours)):
        time_hrv_data.append([str(df_hours[i]['endTime'][0]), str(df_hours[i]['endTime'][59]), get_time_domain_features(list(60000/df_hours[i]['bpm']))])
    
    a = 3
    
    stress_ = []
    for i in range(len(time_hrv_data)):
        stress_.append([time_hrv_data[i][0][:16], hrv_stress(time_hrv_data[i][2])])
        
    stress_plot(stress_)
    
    df.to_json('C:/Users/AIA01/Desktop/project/PNUh/pnuh_page/hrv_proc/' + json_file[0], orient='records', date_format='iso')
    
    
    
    
    
    
    
    
