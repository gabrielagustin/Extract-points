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



def read_SMAP_L1C_HDF_box(FILE_NAME, box_lat, box_lon, nameVariableArray):
    """
    Lee la imagen satelital AQUARIUS_L2SCI en formato .H5

    """
    db=pd.DataFrame()
    pd.options.mode.chained_assignment = None
    with h5py.File(FILE_NAME, mode='r') as f:
        for i in range(0, len(nameVariableArray)):
            nameVariable = nameVariableArray[i]
            print('Variable a extraer:' +str(nameVariable))
            data = f[nameVariable][:,:,0]
            print(data.shape)         
            # Get the geolocation data
            latitude = f['/Sigma0_Data/cell_lat'][:]
            print(latitude.shape)
            longitude = f['/Sigma0_Data/cell_lon'][:]
            print(longitude.shape)

            ##### se lee solo el box_lat y box_lon de la variable
            lat_index = np.logical_and(latitude > box_lat[0], latitude < box_lat[1])
            lon_index = np.logical_and(longitude > box_lon[0], longitude < box_lon[1])
            box_index = np.logical_and(lat_index, lon_index)
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

        groupName = 'Spacecraft_Data'
        group = f[groupName]

        #Checkout what keys are inside that group.
        print('Keys are inside that group: '+str(groupName))
        for key in group.keys():
            print(key)
        print('--------------------------------------------------------------------')

        box_lat = [-85, -65]
        box_lon = [120, 180]

        nameVariableArray = ['/Sigma0_Data/cell_kp_vv_aft']

        df = read_SMAP_L1C_HDF_box(FILE_NAME, box_lat, box_lon, nameVariableArray)

        print(list(df))
        print(df)
    


    #     # m = Basemap(projection='cyl', resolution='l',
    #     #             llcrnrlat=-86.88, urcrnrlat=-64.54,
    #     #             llcrnrlon=119.97, urcrnrlon=176.019)
    #     m.drawcoastlines(linewidth=0.5)
    #     m.drawparallels(np.arange(-90, 91, 10),labels=[True,False,False,True])
    #     m.drawmeridians(np.arange(-180, 180, 15), labels=[True,False,False,True])
    #     m.scatter(longitude, latitude, c=data, s=1, cmap=plt.cm.jet,
    #             edgecolors=None, linewidth=0)
    #     cb = m.colorbar(location="bottom", pad=0.7)    
    #     # cb.set_label(units)

    #     # basename = os.path.basename(FILE_NAME)

    #     # plt.title('{0}\n{1}'.format(basename, longname))
    #     #fig = plt.gcf()
    #     plt.show()
    # #    pngfile = "{0}.py.png".format(basename)
    # #    fig.savefig(pngfile)

if __name__ == "__main__":

    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
    hdffile = '/home/gag/Escritorio/Extract/SMAP_L1C/SMAP_L1C_S0_HIRES_01065_A_20150414T084156_R11850_001.h5'

    try:
        hdffile = os.path.join(os.environ['HDFEOS_ZOO_DIR'], hdffile)
    except KeyError:
        pass

    run(hdffile)


