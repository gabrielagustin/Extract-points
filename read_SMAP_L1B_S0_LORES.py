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



def read_SMAP_L1B_S0_LORES_HDF_box(FILE_NAME, box_lat, box_lon, nameVariableArray):
    """
    Lee la imagen satelital SMAP_L1B_S0_LORES en formato .H5

    """
    db=pd.DataFrame()
    pd.options.mode.chained_assignment = None
    with h5py.File(FILE_NAME, mode='r') as f:
        for i in range(0, len(nameVariableArray)):
            nameVariable = nameVariableArray[i]
            print('Variable a extraer:' +str(nameVariable))
            data = f[nameVariable][:]
            # data = f[nameVariable][:,:,0]
            # print(data)
            # print(data.shape)         
            # Get the geolocation data
            latitude = f['/Sigma0_Data/center_lat_h'][:]
            # latitude = latitude#*-1
            # print(latitude)
            # print(latitude.shape)
            longitude = f['/Sigma0_Data/center_lon_h'][:]
            # longitude = longitude#*-1
            # print(longitude)
            # print(longitude.shape)
            ##### se lee solo el box_lat y box_lon de la variable
            lat_index = np.logical_and(latitude > box_lat[0], latitude < box_lat[1])
            lon_index = np.logical_and(longitude > box_lon[0], longitude < box_lon[1])
            box_index = np.logical_and(lat_index, lon_index)
            # print(box_index)
            # print(box_index.shape)
            data = data[box_index]
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

    with h5py.File(FILE_NAME, mode='r') as f:
        print('--------------------------------------------------------------------')
        print('Names of the groups in HDF5 file:')
        for key in f.keys():
            print(key) #Names of the groups in HDF5 file.
        print('--------------------------------------------------------------------')
#         #Get the HDF5 group
            # Names of the groups in HDF5 file:
            # Metadata
            # Spacecraft_Data
            # Crosstrack_Data
            # Sigma0_Data
        
        # groupName = "Metadata"
        # groupName = 'Spacecraft_Data'
        # groupName = 'Crosstrack_Data'
        groupName = 'Sigma0_Data'
        group = f[groupName]

        #Checkout what keys are inside that group.
        print('Keys are inside that group: '+str(groupName))
        for key in group.keys():
            print(key)
        print('--------------------------------------------------------------------')

        box_lat = [-85, -65]
        box_lon = [120, 180]

        nameVariableArray = ['/Sigma0_Data/sigma0_vh', '/Sigma0_Data/sigma0_vv', '/Sigma0_Data/sigma0_hh', '/Sigma0_Data/sigma0_hv']
        name =  nameVariableArray[2]

        df = read_SMAP_L1B_S0_LORES_HDF_box(FILE_NAME, box_lat, box_lon, nameVariableArray)

        print(list(df))
        print(df)
    


        #### plot using basemap
        m = Basemap(projection='cyl', resolution='l',
                llcrnrlat= -85, urcrnrlat=-65,
                llcrnrlon=120, urcrnrlon=180)


        m.drawcoastlines(linewidth=0.5)
        m.drawparallels(np.arange(-90, 91, 10),labels=[True,False,False,True])
        m.drawmeridians(np.arange(-180, 180, 15), labels=[True,False,False,True])
        m.scatter(df.Longitude, df.Latitude, c=df[name], s=1, cmap=plt.cm.jet,
                edgecolors=None, linewidth=0)
        cb = m.colorbar(location="bottom", pad=0.7)    
        cb.set_label('[°K]')
        plt.title(name)

        plt.show()

if __name__ == "__main__":

    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.

    hdffile = '/.../SMAP_L1B_S0_LORES_02298_D_20150707T165412_R11850_001.h5'
    try:
        hdffile = os.path.join(os.environ['HDFEOS_ZOO_DIR'], hdffile)
    except KeyError:
        pass

    run(hdffile)


