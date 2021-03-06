# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 10:58:49 2019

@author: gag

Script that reads the CSV file. with the complete data set 
and performs the plot of the variables. For this, the mean and 
the deviation are calculated using panda group operations over points.
Finally, it creates a new .CSV file with these data. 


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

#### se filtran los datos cuya distancia del punto KML a los centros de los pixeles del HDF
#### superan los 30 km
df['Distance[degree]'] = (df['Distance[degree]']/360)*np.pi*12756.2

#### se agrupa por: Fecha y Coordenadas y se calcula la media de las variables. Es decir, se calcula la
#### media para cada dia de cada punto o lo que es lo mismo, se promedia las pasadas del satelite en el día.
 
group_data1 = df.groupby(['Date','Coordinates_KML'], sort=False)['/Brightness_Temperature/tb_h', '/Brightness_Temperature/tb_v'].mean()
# print(group_data1)


#### Luego, se vuelve a agrupar por punto (coordinates) para todas las fechas y se calcula la media y el STD
group_data2 = group_data1.groupby(['Coordinates_KML'], sort=False)['/Brightness_Temperature/tb_h',
'/Brightness_Temperature/tb_v'].agg({'mean', 'std'})

print(group_data2)

group_data2 = group_data2.reset_index(drop=False)
print(group_data2)
#### se genera un nuevo archivo .CSV con los estadisticos por punto
group_data2.to_csv("/home/gag/Escritorio/DataSet_Dec_Flight_Dec_mean_std.csv", decimal = ".")

#### se genera la grafica
# fig1, ax1 = plt.subplots()
ax1= group_data2.plot(style='.')
plt.title('SMAP L1B - December Flight Line December')
ax1.set_xlabel("Point")
ax1.set_ylabel("Brightness_Temperature[K]")

plt.show()
