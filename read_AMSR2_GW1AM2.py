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

import functions



def run(FILE_NAME):

    with h5py.File(FILE_NAME, mode='r') as f:
        print('--------------------------------------------------------------------')
        print('Names of the groups in HDF5 file:')
        for key in f.keys():
            print(key) #Names of the groups in HDF5 file.
        print('--------------------------------------------------------------------') 

        ####--------------------------------------------------------------------
        #### Names of the groups in H5 file:
        # Brightness Temperature (10.7GHz,H)
        # Brightness Temperature (10.7GHz,V)
        # Brightness Temperature (18.7GHz,H)
        # Brightness Temperature (18.7GHz,V)
        # Brightness Temperature (23.8GHz,H)
        # Brightness Temperature (23.8GHz,V)
        # Brightness Temperature (36.5GHz,H)
        # Brightness Temperature (36.5GHz,V)
        # Brightness Temperature (6.9GHz,H)
        # Brightness Temperature (6.9GHz,V)
        # Brightness Temperature (7.3GHz,H)
        # Brightness Temperature (7.3GHz,V)
        # Brightness Temperature (89.0GHz-A,H)
        # Brightness Temperature (89.0GHz-A,V)
        # Brightness Temperature (89.0GHz-B,H)
        # Brightness Temperature (89.0GHz-B,V)
        # Cold Sky Mirror Count 6 to 36
        # Cold Sky Mirror Count 89
        # Earth Azimuth
        # Earth Incidence
        # Hot Load Count 6 to 36
        # Hot Load Count 89
        # Interpolation Flag 6 to 36
        # Interpolation Flag 89
        # Land_Ocean Flag 6 to 36
        # Land_Ocean Flag 89
        # Latitude of Observation Point for 89A
        # Latitude of Observation Point for 89B
        # Longitude of Observation Point for 89A
        # Longitude of Observation Point for 89B
        # Navigation Data
        # Observation Supplement
        # PCD Data
        # Pixel Data Quality 6 to 36
        # Pixel Data Quality 89
        # Position in Orbit
        # Rx Offset_Gain Count
        # SPC Temperature Count
        # SPS Temperature Count
        # Scan Data Quality
        # Scan Time
        # Sun Azimuth
        # Sun Elevation
        ####--------------------------------------------------------------------

    box_lat = [-85, -65]
    box_lon = [120, 180]

    # nameVariableArray = ['Brightness Temperature (10.7GHz,H)', 'Brightness Temperature (10.7GHz,V)', 'Brightness Temperature (18.7GHz,H)',
    # 'Brightness Temperature (18.7GHz,V)', 'Brightness Temperature (23.8GHz,H)', 'Brightness Temperature (23.8GHz,V)',
    # 'Brightness Temperature (36.5GHz,H)', 'Brightness Temperature (36.5GHz,V)', 'Brightness Temperature (6.9GHz,H)',
    # 'Brightness Temperature (6.9GHz,V)', 'Brightness Temperature (7.3GHz,H)', 'Brightness Temperature (7.3GHz,V)']

    nameVariableArray = ['Brightness Temperature (89.0GHz-B,V)', 'Brightness Temperature (89.0GHz-B,H)']

    df = functions.read_AMSR2_HDF_box(FILE_NAME, box_lat, box_lon, nameVariableArray)

    print(list(df))
    print(df)

    #### plot using basemap
    m = Basemap(projection='cyl', resolution='l',
            llcrnrlat= -85, urcrnrlat=-65,
            llcrnrlon=120, urcrnrlon=180)


    m.drawcoastlines(linewidth=0.5)
    m.drawparallels(np.arange(-90, 91, 10),labels=[True,False,False,True])
    m.drawmeridians(np.arange(-180, 180, 15), labels=[True,False,False,True])
    # name = 'Brightness Temperature (89.0GHz-B,V)'
    name = 'Brightness Temperature (89.0GHz-B,H)'
    m.scatter(df.Longitude, df.Latitude, c=df[name], s=1, cmap=plt.cm.jet,
            edgecolors=None, linewidth=0)
    cb = m.colorbar(location="bottom", pad=0.7)    
    cb.set_label('[°K]')
    plt.title(name)

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

