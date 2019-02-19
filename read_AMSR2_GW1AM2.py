# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:16:04 2018

@author: gag


"""

import os

import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import pandas as pd
from shapely.geometry import Point


# Reduce font size because dataset's long_name attribute  value is very long.
mpl.rcParams.update({'font.size': 10})


def read_AMSR2_HDF_box(FILE_NAME, box_lat, box_lon, nameVariableArray):
    """
    Lee la imagen satelital AMSR2 en formato .H5
    Recibe el path completo de la image, el box del área específica y las variables a leer
    A diferencia de la función anterior sólo lee una porción de la imagen satelital,
    lee el área que recibe en box
    Retorna un objeto pandas el cual posee como columnas las coordenadas (Lat, Lon)
    y las variables leidas para cada pixel. 
    """
    db=pd.DataFrame()
    pd.options.mode.chained_assignment = None
    with h5py.File(FILE_NAME, mode='r') as f:
        for i in range(0, len(nameVariableArray)):
            nameVariable = nameVariableArray[i]
            # print('Variable a extraer:' +str(nameVariable))
            data = f[nameVariable][:]         
            # Get the geolocation data
            if (nameVariable.find("89.0GHz") != -1):        
                latitude = f['Latitude of Observation Point for 89A'][:]
                # print(latitude)
                longitude = f['Longitude of Observation Point for 89A'][:]
                # print(longitude)
            else:
                print("Is NOT at 89.0GHz")
                #### con AMSR2 la diferencia esta en que para la longitud de onda 89GHz
                #### posee un sobremuestreo con respecto a las demas frecuencias
                latitude = f['Latitude of Observation Point for 89A'][:]
                # print(latitude)
                longitude = f['Longitude of Observation Point for 89A'][:]
                # print(longitude)
                latitude = latitude[:, ::2]
                longitude = longitude[:, ::2]


            ##### se lee solo el box_lat y box_lon de la variable
            lat_index = np.logical_and(latitude > box_lat[0], latitude < box_lat[1])
            lon_index = np.logical_and(longitude > box_lon[0], longitude < box_lon[1])
            box_index = np.logical_and(lat_index, lon_index)
            data = f[nameVariable][box_index]
            #### se genera el objeto pandas
            db[nameVariable] = data
            ##### se lee solo el box_lat y box_lon de las coordenadas
            latitude = latitude[box_index]
            longitude = longitude[box_index]

    db["Longitude"] = pd.to_numeric(longitude)
    db["Latitude"] = pd.to_numeric(latitude)    

    db['Coordinates'] = list(zip(db.Longitude, db.Latitude))
    db['Coordinates'] = db['Coordinates'].apply(Point)

    db = db.dropna()
    return db






def run(FILE_NAME):

    # with h5py.File(FILE_NAME, mode='r') as f:
    #     print('--------------------------------------------------------------------')
    #     print('Names of the groups in HDF5 file:')
    #     for key in f.keys():
    #         print(key) #Names of the groups in HDF5 file.
    #     print('--------------------------------------------------------------------')
    #     #Get the HDF5 group

    #     #### Names of the groups in H5 file:

    #     # Brightness Temperature (10.7GHz,H)
    #     # Brightness Temperature (10.7GHz,V)
    #     # Brightness Temperature (18.7GHz,H)
    #     # Brightness Temperature (18.7GHz,V)
    #     # Brightness Temperature (23.8GHz,H)
    #     # Brightness Temperature (23.8GHz,V)
    #     # Brightness Temperature (36.5GHz,H)
    #     # Brightness Temperature (36.5GHz,V)
    #     # Brightness Temperature (6.9GHz,H)
    #     # Brightness Temperature (6.9GHz,V)
    #     # Brightness Temperature (7.3GHz,H)
    #     # Brightness Temperature (7.3GHz,V)
    #     # Brightness Temperature (89.0GHz-A,H)
    #     # Brightness Temperature (89.0GHz-A,V)
    #     # Brightness Temperature (89.0GHz-B,H)
    #     # Brightness Temperature (89.0GHz-B,V)
    #     # Cold Sky Mirror Count 6 to 36
    #     # Cold Sky Mirror Count 89
    #     # Earth Azimuth
    #     # Earth Incidence
    #     # Hot Load Count 6 to 36
    #     # Hot Load Count 89
    #     # Interpolation Flag 6 to 36
    #     # Interpolation Flag 89
    #     # Land_Ocean Flag 6 to 36
    #     # Land_Ocean Flag 89
    #     # Latitude of Observation Point for 89A
    #     # Latitude of Observation Point for 89B
    #     # Longitude of Observation Point for 89A
    #     # Longitude of Observation Point for 89B
    #     # Navigation Data
    #     # Observation Supplement
    #     # PCD Data
    #     # Pixel Data Quality 6 to 36
    #     # Pixel Data Quality 89
    #     # Position in Orbit
    #     # Rx Offset_Gain Count
    #     # SPC Temperature Count
    #     # SPS Temperature Count
    #     # Scan Data Quality
    #     # Scan Time
    #     # Sun Azimuth
    #     # Sun Elevation


    box_lat = [-85, -65]
    box_lon = [120, 180]

    nameVariableArray = ['Brightness Temperature (10.7GHz,H)', 'Brightness Temperature (10.7GHz,V)', 'Brightness Temperature (18.7GHz,H)',
    'Brightness Temperature (18.7GHz,V)', 'Brightness Temperature (23.8GHz,H)', 'Brightness Temperature (23.8GHz,V)',
    'Brightness Temperature (36.5GHz,H)', 'Brightness Temperature (36.5GHz,V)', 'Brightness Temperature (6.9GHz,H)',
    'Brightness Temperature (6.9GHz,V)', 'Brightness Temperature (7.3GHz,H)', 'Brightness Temperature (7.3GHz,V)']

    # nameVariableArray = ['Brightness Temperature (89.0GHz-B,V)', 'Brightness Temperature (89.0GHz-B,H)']

    df = read_AMSR2_HDF_box(FILE_NAME, box_lat, box_lon, nameVariableArray)

    print(list(df))
    print(df)

    #### plot using basemap
    m = Basemap(projection='cyl', resolution='l',
            llcrnrlat= -85, urcrnrlat=-65,
            llcrnrlon=120, urcrnrlon=180)


    m.drawcoastlines(linewidth=0.5)
    m.drawparallels(np.arange(-90, 91, 10),labels=[True,False,False,True])
    m.drawmeridians(np.arange(-180, 180, 15), labels=[True,False,False,True])
    m.scatter(df.Longitude, df.Latitude, c=df['Brightness Temperature (10.7GHz,H)'], s=1, cmap=plt.cm.jet,
            edgecolors=None, linewidth=0)
    # m.scatter(df.Longitude, df.Latitude, c=df['Brightness Temperature (89.0GHz-B,V)'], s=1, cmap=plt.cm.jet,
    #         edgecolors=None, linewidth=0)
    cb = m.colorbar(location="bottom", pad=0.7)    
    cb.set_label('[°K]')

    plt.show()

if __name__ == "__main__":

    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
    hdffile = '/home/gag/Escritorio/Extract/AMSR2/GW1AM2_201811010415_215A_L1SGBTBR_2220220.h5'

    try:
        hdffile = os.path.join(os.environ['HDFEOS_ZOO_DIR'], hdffile)
    except KeyError:
        pass

    run(hdffile)
