#! /usr/bin/env python
#coding = utf-8

# 将原始数据分精度

import scipy.io as sio
import numpy as np
import math

load_fn = 'Originaldata_separate'
load_data = sio.loadmat(load_fn)                                                                                   # 读取文件
load_matrix = load_data['Originaldata_separate']                                                                  #取出Originaldata_separate
#print(load_matrix)
time_shaft = np.array([load_matrix[:,0]])                                                                         #取了Originaldata_separate中Originaldata_separate的第一列
org_meter = np.array([load_matrix[:,1]])                                                                          #取了Originaldata_separate中Originaldata_separate的第二列
#print(time_shaft[0])
#print(time_shaft)

time_interval=60                                                                                                   #设定分精度时间间隔,以分钟为单位
start_time = math.ceil((time_shaft[0][0])*24*60/time_interval)/(24*60/time_interval)                               #分精度的开始时间
stop_time = math.floor(time_shaft[0,time_shaft.shape[1]-1]*24*60/time_interval)/(24*60/time_interval)              # 分精度分精度的结束时间
#print(start_time,(1/(24*60/time_interval)),stop_time)
time_shaft2 = np.array([np.arange(start_time,stop_time,(1/(24*60/time_interval)))])                               #做等差数列
#print(time_shaft2)

time_shaft2 = time_shaft2.T                                                                                       #矩阵转置
org_meter2=[]                                                                                                     #分精度的电表累计读数
org_flag2=[]                                                                                                      #分精度的数据类型标记
time_shaft_round=np.array(((time_shaft*24*60/time_interval).round())/(24*60/time_interval))                       #对数据进行取整
time_shaft_adj=np.vstack((time_shaft_round ,time_shaft-time_shaft_round))
#print(time_shaft_round)
#print(time_shaft2)


#分精度

kk=0
j = 1
for i in range(j,time_shaft2.shape[0]+1):                                                                         #循环从j到time_shaft2的行数
    meter_temp =[]
    diff_temp = []
    l = 0                                                                                                         #各分精度时间单元内的点数
    k = kk +1
    #按分精度时间轴归类原时间轴
    for i in range( k ,time_shaft_round.shape[0]+1):
        print(time_shaft_round[0][k-1]-time_shaft2[0][j-1])
        if time_shaft_round[0][k-1]-time_shaft2[0][j-1]<-0.000001:
            kk = kk +1
            k = kk

        elif (time_shaft_round[0][k-1]-time_shaft2[0][j-1])>= -0.000001 and (time_shaft_round[0][k-1]-time_shaft2[0][j-1]) <= 0.000001:
            l = l + 1
            meter_temp.insert(l-1,org_meter[0][k-1])
            diff_temp.insert(l-1,time_shaft_adj[1][k-1])
            kk = kk+1
            k = kk

        elif time_shaft_round[0][k-1]-time_shaft2[0][j-1]>0.000001:
            break

    if l == 0:                                                                             # 如果该分精度时间单元内没有原时间点, 表累计值赋值-9999
        org_meter2.insert(j-1,-9999)
        org_flag2.insert(j-1,1)

    elif l == 1:                                                                           #如果该分精度时间单元内只有一个原时间点,表累计值为该原时间点的值
        org_meter2.insert(j-1,meter_temp[0])
        if meter_temp[0] < 0:
            org_flag2.insert(j-1,1)
        else:
            org_flag2.insert(j-1, 0)
    elif diff_temp[0]>=0:                                                                 #如果多于两个原时间点在该分精度时间单元内,判断是否原时间点都在分精度点的一侧还是两侧
        org_meter2.insert(j-1,meter_temp[1-1])
        if meter_temp[0] < 0:
            org_flag2.insert(j - 1, 1)
        else:
            org_flag2.insert(j - 1, 0)

        if diff_temp[l-1] <= 0:                                                            #如果在一侧，取最靠近点
            org_meter2.insert(j-1,meter_temp[l-1])
            if meter_temp[0] < 0:
                org_flag2.insert(j - 1, 1)
            else:
                org_flag2.insert(j - 1, 0)

        else:
            m = 1
            for i in range(m,l+1):
                if diff_temp[m-1] * diff_temp[m] <= 0:                                      # 如果在两侧，取临近两点的线性差值
                    org_meter2.insert(j-1,meter_temp[m - 1] - (meter_temp[m] - meter_temp[m - 1]) * diff_temp[m - 1] / (diff_temp[m] - diff_temp[m - 1]))
                if meter_temp[m-1] < 0 or meter_temp[m] < 0:
                    org_flag2.insert(j-1,1)
                else:
                    org_flag2.insert(j-1,0)

org_meter2 = np.array(org_meter2)
org_flag2 = np.array(org_flag2)


org_meter2=org_meter2.T
org_flag2=org_flag2.T




