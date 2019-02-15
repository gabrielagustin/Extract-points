# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 10:58:49 2019

@author: gag

Script that reads the CSV file. with the complete data set 
and performs the boxplot of the variables for all points. 

"""

import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


#### data file
file = "/.../NAME.csv"
df = pd.read_csv(file, sep=',', decimal=",")

print(list(df))
print(df)

sns.set()


#### se agrupa por: Fecha y Coordenadas y se calcula la media de las variables. Es decir, se calcula la
#### media para cada dia de cada punto o lo que es lo mismo, se promedia las pasadas del satelite en el día.
 
group_data = df.groupby(['Date','Coordinates_KML'], sort=False)['/Brightness_Temperature/tb_h', '/Brightness_Temperature/tb_v'].mean() #sum function
print(group_data)

df1 = group_data
df1 = df1.reset_index()
print(df1)
print(list(df1))

df1 = df1.rename(index=str, columns={"/Brightness_Temperature/tb_h": "Tb_h[K]", "/Brightness_Temperature/tb_v": "Tb_v[K]"})
print(list(df1))

fig1, ax1 = plt.subplots()
plt.title('SMAP L1B - November Flight Line')
sns.boxplot(x="Date", y="Tb_h[K]",
            data=df1, color="skyblue")
plt.xticks(rotation=45, fontsize=8)


fig2, ax2 = plt.subplots()
plt.title('SMAP L1B - November Flight Line')
sns.boxplot(x="Date", y="Tb_v[K]",
            data=df1, color="skyblue")
plt.xticks(rotation=45, fontsize=8)




group_data = df.groupby(['Date','Coordinates_KML'])['/Brightness_Temperature/toa_h', '/Brightness_Temperature/toa_v'].mean() #sum function
print(group_data)

df2 = group_data
df2 = df2.reset_index()
print("Despues de agrupar!")
print(df2)
print(list(df2))
df2 = df2.rename(index=str, columns={"/Brightness_Temperature/toa_h": "Toa_h[K]", "/Brightness_Temperature/toa_v": "Toa_v[K]"})


fig3, ax3 = plt.subplots()
plt.title('SMAP L1B - November Flight Line')
sns.boxplot(x="Date", y="Toa_h[K]",
            data=df2, color="skyblue")
plt.xticks(rotation=45, fontsize=8)


fig4, ax4 = plt.subplots()
plt.title('SMAP L1B - November Flight Line')
sns.boxplot(x="Date", y="Toa_v[K]",
            data=df2, color="skyblue")
plt.xticks(rotation=45, fontsize=8)


plt.show()
