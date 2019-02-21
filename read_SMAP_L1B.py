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

# Reduce font size because dataset's long_name attribute  value is very long.
mpl.rcParams.update({'font.size': 10})

def run(FILE_NAME):

    with h5py.File(FILE_NAME, mode='r') as f:
        print('--------------------------------------------------------------------')
        print('Names of the groups in HDF5 file:')
        for key in f.keys():
            print(key) #Names of the groups in HDF5 file.
        print('--------------------------------------------------------------------')
        #Get the HDF5 group
        group = f['Brightness_Temperature']

        #Checkout what keys are inside that group.
        print('Keys are inside that group: Brightness_Temperature')
        for key in group.keys():
            print(key)
        print('--------------------------------------------------------------------')

        
        name = '/Brightness_Temperature/tb_h'
        data = f[name][:]
        units = f[name].attrs['units']
        longname = f[name].attrs['long_name']
        _FillValue = f[name].attrs['_FillValue']
        valid_max = f[name].attrs['valid_max']
        valid_min = f[name].attrs['valid_min']        
        invalid = np.logical_or(data > valid_max,
                            data < valid_min)
        invalid = np.logical_or(invalid, data == _FillValue)
        data[invalid] = np.nan
        data = np.ma.masked_where(np.isnan(data), data)
        
        # Get the geolocation data
        latitude = f['/Brightness_Temperature/tb_lat'][:]
        longitude = f['/Brightness_Temperature/tb_lon'][:]

        
    # m = Basemap(projection='cyl', resolution='l',
    #            llcrnrlat=-90, urcrnrlat=90,
    #            llcrnrlon=-180, urcrnrlon=180)
    # m = Basemap(projection='cyl', resolution='l',
    #            llcrnrlat= -90, urcrnrlat=-40,
    #            llcrnrlon=-180, urcrnrlon=180)

    box_lat = [-90, -60]
    box_lon = [105, 180]
    m = Basemap(projection='cyl', resolution='l',
            llcrnrlat= -85, urcrnrlat=-65,
            llcrnrlon=120, urcrnrlon=180)
    box_lat = [-85, -65]
    box_lon = [120, 180]
    


    # m = Basemap(projection='cyl', resolution='l',
    #             llcrnrlat=-86.88, urcrnrlat=-64.54,
    #             llcrnrlon=119.97, urcrnrlon=176.019)
    m.drawcoastlines(linewidth=0.5)
    m.drawparallels(np.arange(-90, 91, 10),labels=[True,False,False,True])
    m.drawmeridians(np.arange(-180, 180, 15), labels=[True,False,False,True])
    m.scatter(longitude, latitude, c=data, s=1, cmap=plt.cm.jet,
            edgecolors=None, linewidth=0)
    cb = m.colorbar(location="bottom", pad=0.7)    
    cb.set_label(units)

    basename = os.path.basename(FILE_NAME)

    plt.title('{0}\n{1}'.format(basename, longname))
    #fig = plt.gcf()
    plt.show()
#    pngfile = "{0}.py.png".format(basename)
#    fig.savefig(pngfile)

if __name__ == "__main__":

    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
    hdffile = '/home/gag/Escritorio/SMAP_L1B/SMAP_L1B_TB_20137_A_20181108T101842_R16020_001.h5'

    try:
        hdffile = os.path.join(os.environ['HDFEOS_ZOO_DIR'], hdffile)
    except KeyError:
        pass

    run(hdffile)
