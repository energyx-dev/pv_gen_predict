import numpy as np
import datetime
import measure
import predict
import error_cal
import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'Noto Sans CJK KR'
plt.rcParams['font.weight'] = 'heavy'
import pandas as pd
from datetime import datetime,timedelta
import seaborn as sns
import sys

def test(strOrgCd : str, pred_strSDate: str, meas_strSDate: str, pred_strEDate: str, meas_strEDate: str, location_name: str, capacity: float, lat: str, lng: str):
    time_delta = timedelta(days=1)
    now = datetime.now()
    today_mark = pred_strEDate + ' 00:00:00+09:00'
    df_measure = measure.measure(meas_strSDate, meas_strEDate, strOrgCd)
    df_predict = predict.predict(lat, lng, location_name, strOrgCd, pred_strSDate, pred_strEDate)
    # df_measure = pd.read_csv('result_1/df_gens_876_2021-08-23.csv', index_col=0, parse_dates=True)
    # df_predict = pd.read_csv('result_1/df_pred_876_2021-08-23.csv', index_col=0, parse_dates=True)
    # df_measure = pd.read_csv('result_1/df_gens_%s_%s.csv' % (strOrgCd,(pd.to_datetime(meas_strEDate)+time_delta).strftime('%Y-%m-%d')), index_col=0, parse_dates=True)
    # df_predict = pd.read_csv('result_1/df_pred_%s_%s.csv' % (strOrgCd,(pd.to_datetime(meas_strEDate)+time_delta).strftime('%Y-%m-%d')), index_col=0, parse_dates=True)
    # print(df_measure, df_predict)
    _, __, df_nmae_hour, df_nmae_1d, ___, df_nce_1d = error_cal.error_cal(lat, lng, pred_strSDate, pred_strEDate, strOrgCd, location_name, capacity)
    
    fig = plt.figure(figsize=(16,9.5))
    plt.subplot(2, 1, 1)
    plt.plot(df_measure.loc[(pd.to_datetime(pred_strSDate)+time_delta).strftime('%Y-%m-%d'):].index, df_measure.loc[(pd.to_datetime(pred_strSDate)+time_delta).strftime('%Y-%m-%d'):].values, df_predict.loc[(pd.to_datetime(pred_strSDate)+time_delta).strftime('%Y-%m-%d'):].index, df_predict.loc[(pd.to_datetime(pred_strSDate)+time_delta).strftime('%Y-%m-%d'):].values)
    plt.plot(pd.to_datetime([today_mark, today_mark]), [0, capacity/3], 'r--')
    plt.title('%s의 태양광 발전량(%dkW)' % (location_name, capacity), fontsize=32, fontweight='heavy')
    fig.suptitle('NOW: %s' % now.strftime("%Y-%m-%d %H:%M:%S"))
    plt.legend(['실제 발전량','예측 발전량'])
    
    plt.subplot(2, 3, 4)
    df_nmae_hour.plot.bar(ax=plt.gca())
    plt.title('시간별 평균절대오차', fontweight='heavy')
    plt.legend(['MAE/capacity(시간단위)'])
    # plt.figure(figsize=(5,5))
    
    df_nmae_1d.index = df_nmae_1d.index.date
    df_nce_1d.index = df_nce_1d.index.date
    #err_cal[3]
    #err_cal_day = pd.concat([err_cal[3],err_cal[5]], axis=1)
    
    plt.subplot(2, 3, 5)
    df_nmae_1d[:-1].plot.bar(ax=plt.gca(),color='gray')
    plt.title('일별 평균절대오차', fontweight='heavy')
    plt.legend(['MAE/capacity(시간단위)'])
    
    plt.subplot(2, 3, 6)
    df_nce_1d[:-1].plot.bar(ax=plt.gca(),color='DarkRed')
    plt.title('일별 누적오차', fontweight='heavy')
    plt.legend(['error/capacity'])
    
    # print(err_cal_day)
    plt.show()
    
    # print("총 조회시간 내의 설치용량 대 평균절대오차", err_cal_876[0])
    # print("총 조회시간 내의 설치용량 대 시간당 평균절대오차", err_cal_876[1])
    # print("총 조회시간 내의 설치용량 대 일당 평균절대오차", err_cal_876[2])
if __name__ == '__main__':
    now = datetime.now()
    pred_strEDate = now.strftime("%Y-%m-%d") #'2021-08-26'
    meas_strEDate = pred_strEDate.replace('-', '') # '20210826'
    pred_strSDate = (now - timedelta(days=6)).strftime("%Y-%m-%d") # '2021-08-20'
    meas_strSDate = pred_strSDate.replace('-', '') # '20210820'
    print("Today: %s" % now)
    
    if len(sys.argv) < 2:
        test('876', pred_strSDate, meas_strSDate, pred_strEDate, meas_strEDate, '신인천소내', 200, '37.4772', '126.6249')
        test('997N', pred_strSDate, meas_strSDate, pred_strEDate, meas_strEDate, '부산복합자재창고', 115, '35.10468', '129.0323')
        test('997G', pred_strSDate, meas_strSDate, pred_strEDate, meas_strEDate, '부산신항', 187, '35.10468', '129.0323')
    else:
        if sys.argv[1] == '신인천소내':
            test('876', pred_strSDate, meas_strSDate, pred_strEDate, meas_strEDate, '신인천소내', 200, '37.4772', '126.6249')
        elif sys.argv[1] == '부산복합자재창고':
            test('997N', pred_strSDate, meas_strSDate, pred_strEDate, meas_strEDate, '부산복합자재창고', 115, '35.10468', '129.0323')
        elif sys.argv[1] == '부산신항':
            test('997G', pred_strSDate, meas_strSDate, pred_strEDate, meas_strEDate, '부산신항', 187, '35.10468', '129.0323')