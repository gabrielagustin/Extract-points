# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 10:58:49 2019

@author: gag

Script que lee el archivo CSV. con el data set completo
y realiza el plor de las variables

"""

import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

#### data using november flight
# file = "/home/gag/Escritorio/DataSet_Nov_Flight_Nov.csv"
# file = "/home/gag/Escritorio/DataSet_Dec_Flight_Nov.csv"

#### data using december flight
# file = "/home/gag/Escritorio/DataSet_Nov_Flight_Dec.csv"
file = "/home/gag/Escritorio/DataSet_Dec_Flight_Dec.csv"

df = pd.read_csv(file, sep=',', decimal=",")

print(list(df))
print(df)

# dataNew = df[(df['Distance[degree]'] < 0.01)]
# df = dataNew

# del df['Distance[degree]']
# del df['Point_name']
# del df['Coordinates_KML']
# del df['Coordinates_HDF']


sns.set()



#### se agrupa por: Fecha y Coordenadas y se calcula la media de las variables. Es decir, se calcula la
#### media para cada dia de cada punto o lo que es lo mismo, se promedia las pasadas del satelite en el día.
 
group_data = df.groupby(['Date','Coordinates_KML'], sort=False)['/Brightness_Temperature/tb_h', '/Brightness_Temperature/tb_v'].mean()
# print(group_data)


# print("ACA")
# ### voy a agrupar por punto y hago el promedio en el tiempo
# group_data = df.groupby(['Coordinates_KML'], sort=False)['/Brightness_Temperature/tb_h', '/Brightness_Temperature/tb_v'].mean() #sum function

group_data = df.groupby(['Coordinates_KML'], sort=False)['/Brightness_Temperature/tb_h', '/Brightness_Temperature/tb_v'].agg({'mean', 'std'})


print(group_data)
# # group_data = group_data.sort_values(by=['Point_name'])




df1 = group_data
# # # df1 = df1.reset_index()
# # # print(df1)
# # # print(list(df1))

# # df1 = df1.rename(index=str, columns={"/Brightness_Temperature/tb_h": "Tb_h[K]", "/Brightness_Temperature/tb_v": "Tb_v[K]"})
df1 = df1.reset_index(drop=False)
print(df1)

df1.to_csv("/home/gag/Escritorio/DataSet_Dec_Flight_Dec_mean_std.csv", decimal = ",")
# df1.to_csv("/home/gag/Escritorio/DataSet_Dec_Flight_Dec_mean_std.csv", decimal = ",")
# print(list(df1))

# fig1, ax1 = plt.subplots()

ax1= df1.plot(style='.')
plt.title('SMAP L1B - December Flight Line December')
# Set the x-axis label
ax1.set_xlabel("Point")
# Set the y-axis label
ax1.set_ylabel("Brightness_Temperature[K]")
# sns.boxplot(x=df1.index, y="Tb_h[K]",
#             data=df1, color="skyblue")
# plt.xticks(rotation=45, fontsize=8)


# fig2, ax2 = plt.subplots()
# plt.title('SMAP L1B - November Flight Line November')
# sns.boxplot(x=df1.index, y="Tb_v[K]",
#             data=df1, color="skyblue")
# plt.xticks(rotation=45, fontsize=8)








# # # group_data = df.groupby(['Date','Coordinates_KML'])['/Brightness_Temperature/toa_h', '/Brightness_Temperature/toa_v'].mean() #sum function
# # # print(group_data)

# # # df2 = group_data
# # # df2 = df2.reset_index()
# # # print("Despues de agrupar!")
# # # print(df2)
# # # print(list(df2))
# # # df2 = df2.rename(index=str, columns={"/Brightness_Temperature/toa_h": "Toa_h[K]", "/Brightness_Temperature/toa_v": "Toa_v[K]"})


# # # # del df2['Date']
# # # # del df2['Coordinates_KML']

# # # # fig2, ax2 = plt.subplots()
# # # # df2.plot(ax=ax2)

# # # fig3, ax3 = plt.subplots()
# # # plt.title('SMAP L1B - November Flight Line')
# # # sns.boxplot(x="Date", y="Toa_h[K]",
# # #             data=df2, color="skyblue")
# # # plt.xticks(rotation=45, fontsize=8)


# # # fig4, ax4 = plt.subplots()
# # # plt.title('SMAP L1B - November Flight Line')
# # # sns.boxplot(x="Date", y="Toa_v[K]",
# # #             data=df2, color="skyblue")
# # # plt.xticks(rotation=45, fontsize=8)

# # # # , 




# # # # year_labels = df.Date[tick_idx].values
# # # # ax.xaxis.set_ticklabels(year_labels)


# # # # print(groupedMean)

# # # #['/Brightness_Temperature/toa_v']

# # # # # fig, ax = plt.subplots()
# # # # # # plt.plot(result['/Brightness_Temperature/tb_h'], label='tb_h')
# # # # # # result.plot(kind='scatter',x=result.index, y='/Brightness_Temperature/tb_h')
# # # # # result.plot(kind='scatter',x=result.index, y='/Brightness_Temperature/tb_h')
# # # # # plt.legend(loc='upper left')


# # # # # fig, ax = plt.subplots()
# # # # # ax = result.plot.scatter(x= index, y='/Brightness_Temperature/tb_h', label='tb_h')
# # # # # plt.legend(loc='upper left')
# # # # # 

# # # # # fig, ax = plt.subplots()
# # # # # plt.plot(df['/Brightness_Temperature/tb_v'], label='tb_v')
# # # # # plt.legend(loc='upper left')

# # # # # fig, ax = plt.subplots()
# # # # # plt.plot(result['/Brightness_Temperature/toa_v'], label='toa_v')
# # # # # plt.legend(loc='upper left')


plt.show()