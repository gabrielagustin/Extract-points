# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 10:58:49 2019

@author: gag

Script that reads all files .CSV by MONTHS within an initial file corresponding to a YEAR.
Each file has .CSV files (each file corresponds to a satellite pass per hour) for all days 
of the month, having more than one pass per day.
It generates a pandas object that owns all the .CSV files and organizes them by date. 
Then, generate a single .CSV file.


"""


import os
import pandas as pd



directory = "/.../"
arr = sorted(os.listdir(directory))
print(arr)
big_frame = pd.DataFrame()
# for i in range(0, len(arr)):
for i in range(0, 1):
    print(str(arr[i]))
    csvFiles = sorted(os.listdir(directory+str(arr[i])))
    print("Cantidad de archivos .CSV: "+str(len(csvFiles)))
    for j in range(0,len(csvFiles)):
    # for j in range(0,1):
        name = csvFiles[j]
        dateTime = str(name[20:-15])
        time = str(dateTime[9:])
        date = str(dateTime[:-7])
        print("Fecha archivo .CSV: " + date)
        print("Hora archivo .CSV: " + time)
        df = pd.read_csv(directory+str(arr[i])+"/"+str(csvFiles[j]),sep=',', decimal=",")
        df['Date'] = str(date)
        df['Time'] = str(time)
        big_frame = big_frame.append(df, ignore_index=True)

# print(big_frame['Date'])

result = big_frame.sort_values(by=['Date', 'Time'])
result = result[['Date', 'Time','Point_name', 'Coordinates_KML', 'Coordinates_HDF', 'Distance[degree]', '/Brightness_Temperature/tb_h', '/Brightness_Temperature/tb_v', '/Brightness_Temperature/toa_h', '/Brightness_Temperature/toa_v']]
result = result.reset_index(drop=True)
result.set_index('Date',inplace=True)
print(list(result))
result.to_csv("/.../DataSet.csv", decimal = ",")
print("Archivo completo creado con exito!")



          


          
          
