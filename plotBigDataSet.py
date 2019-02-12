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

#### data file
# file = "/.../NAME.csv"

df = pd.read_csv(file, sep=',', decimal=",")

print(list(df))
print(df)

sns.set()


#### se agrupa por: Fecha y Coordenadas y se calcula la media de las variables. Es decir, se calcula la
#### media para cada dia de cada punto o lo que es lo mismo, se promedia las pasadas del satelite en el día.
 
group_data = df.groupby(['Date','Coordinates_KML'], sort=False)['/Brightness_Temperature/tb_h', '/Brightness_Temperature/tb_v'].mean()
# print(group_data)


#### Luego, se vuelve a agrupar por punto (coordinates) para todas las fechas y se calcula la media y el STD
group_data = df.groupby(['Coordinates_KML'], sort=False)['/Brightness_Temperature/tb_h', '/Brightness_Temperature/tb_v'].agg({'mean', 'std'})


print(group_data)

df1 = group_data
df1 = df1.reset_index(drop=False)
print(df1)
#### se genera un nuevo archivo .CSV con los estadisticos por punto
df1.to_csv("/home/gag/Escritorio/DataSet_Dec_Flight_Dec_mean_std.csv", decimal = ",")

#### se genera la grafica
# fig1, ax1 = plt.subplots()
ax1= df1.plot(style='.')
plt.title('SMAP L1B - December Flight Line December')
ax1.set_xlabel("Point")
ax1.set_ylabel("Brightness_Temperature[K]")

plt.show()