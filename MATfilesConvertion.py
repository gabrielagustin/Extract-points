
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 10:16:04 2018
@author: gag 
Scrip que lee los archivo .MAT y carga los parametros en un objeto pandas,
es necesario conocer cuales son las coordenas de los puntos. Luego, crea un archivo
.KML con los datos requeridos
"""

from scipy.io import loadmat
import pandas as pd
import simplekml
import numpy as np

nameFile ='/.../.mat'
mat = loadmat(nameFile)
#### se extraen los datos de Latitud y Longitud del archivo .mat y crea un objeto pandas
### para esto se necesita conocimiento a priori de la organización del documento .mat

### se sabe que las coordenadas en  longitud y longitud de los puntos se encuentra en el contenedor 
### llamado 'DataGPS'
mdata = mat['DataGPS']
### y las lineas 7 y 8 se corresponden con la latitud y la longitud
lat = mdata[7,:]
lon = mdata[8,:]

print(lat)
print(len(lat))

### se crea un objeto pandas con las coordenadas
d = {'Latitude': lat, 'Longitude': lon}
df = pd.DataFrame(data=d)
df = df.loc[~(df==0).any(axis=1)]
print(df)

### se depuran las datos
pp = df.drop_duplicates(subset=['Latitude', 'Longitude'], keep='first')
pp= pp.reset_index(drop=True)
### a cada punto se le agrega un identificador simple, su indice
pp['name'] = pp.index
print(pp)

### se crea objeto KML y se insertan los puntos extraidos del archivo .MAT
kml=simplekml.Kml()
pp.apply(lambda X: kml.newpoint(name=str(X['name']), coords=[( X["Longitude"],X["Latitude"])]), axis=1)


### finalmente se genera un archivo .KML
outFile = nameFile[:-4]+str('.kml')
print('Se crea archivo KML: '+ str(outFile))
kml.save(outFile)
