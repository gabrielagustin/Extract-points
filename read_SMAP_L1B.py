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

import functions



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

        ####--------------------------------------------------------------------
        # Names of the groups in HDF5 file:
        # Metadata
        # Brightness_Temperature
        # Calibration_Data
        # Spacecraft_Data
        # HighResolution_Calibration_Data
        #### --------------------------------------------------------------------
        # Keys are inside that group: Brightness_Temperature
        # wind_direction_ancillary
        # tb_3
        # solar_specular_reflection_coefficient_h
        # faraday_rotation_correction_h
        # tb_right_ascension
        # ta_3
        # tb_time_utc
        # nedt_h
        # lunar_specular_lon
        # antenna_sidelobe_correction_4
        # galactic_direct_correction_h
        # tb_qual_flag_h
        # antenna_sidelobe_correction_3
        # nedt_v
        # solar_direct_theta
        # specular_right_ascension
        # lunar_specular_theta
        # toa_v
        # ta_filtered_4
        # solar_direct_correction_h
        # atm_loss
        # solar_specular_correction_h
        # ta_filtered_3
        # lunar_specular_reflection_coefficient_v
        # ta_filtered_v
        # antenna_sidelobe_correction_h
        # tb_4
        # solar_specular_phi
        # tb_v_surface_corrected
        # sea_ice_fraction
        # nedt_4
        # antenna_scan_angle
        # lunar_specular_lat
        # solar_specular_correction_4
        # solar_specular_lat
        # tb_h_surface_corrected
        # solar_direct_correction_v
        # tb_upwelling
        # ta_v
        # surface_water_fraction_mb_h
        # tb_lon
        # tb_mode_flag
        # toa_4
        # solar_specular_reflection_coefficient_v
        # tb_qual_flag_3
        # tb_qual_flag_4
        # solar_specular_theta
        # nedt_3
        # surface_water_fraction_mb_v
        # ta_filtered_h
        # wind_speed_ancillary
        # toi_h
        # atm_correction_h
        # galactic_reflected_correction_3
        # ta_4
        # lunar_direct_theta
        # tb_declination
        # lunar_specular_phi
        # galactic_reflected_correction_4
        # faraday_rotation_correction_v
        # solar_specular_lon
        # tb_time_seconds
        # lunar_specular_correction_4
        # specular_declination
        # toa_3
        # tb_lat
        # toi_v
        # earth_boresight_incidence
        # tb_qual_flag_v
        # galactic_direct_correction_v
        # tb_h
        # faraday_rotation_angle
        # antenna_look_angle
        # solar_direct_phi
        # lunar_specular_correction_h
        # antenna_earth_azimuth
        # toi_3
        # earth_boresight_azimuth
        # ta_h
        # lunar_specular_correction_3
        # galactic_reflected_correction_v
        # footprint_surface_status
        # tb_v
        # polarization_rotation_angle
        # toa_h
        # toi_4
        # lunar_specular_reflection_coefficient_h
        # antenna_sidelobe_correction_v
        # solar_specular_correction_v
        # solar_specular_correction_3
        # lunar_direct_phi
        # atm_correction_v
        # galactic_reflected_correction_h
        # lunar_specular_correction_v
        #### --------------------------------------------------------------------

        box_lat = [-85, -65]
        box_lon = [120, 180]


        nameVariableArray = ["/Brightness_Temperature/tb_h", "/Brightness_Temperature/tb_v", 
        "/Brightness_Temperature/toa_h", "/Brightness_Temperature/toa_v"]

        df = functions.read_SMAP_L1B_HDF_box(FILE_NAME, box_lat, box_lon, nameVariableArray)

        print(list(df))
        print(df)

        #### plot using basemap
        m = Basemap(projection='cyl', resolution='l',
                llcrnrlat= -85, urcrnrlat=-65,
                llcrnrlon=120, urcrnrlon=180)


        m.drawcoastlines(linewidth=0.5)
        m.drawparallels(np.arange(-90, 91, 10),labels=[True,False,False,True])
        m.drawmeridians(np.arange(-180, 180, 15), labels=[True,False,False,True])
        # name = "/Brightness_Temperature/tb_h"
        name = "/Brightness_Temperature/tb_v"
        m.scatter(df.Longitude, df.Latitude, c=df[name], s=1, cmap=plt.cm.jet,
                edgecolors=None, linewidth=0)
        cb = m.colorbar(location="bottom", pad=0.7)    
        cb.set_label('[°K]')
        plt.title(name)



        plt.show()


if __name__ == "__main__":

    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
    hdffile = '/.../SMAP_L1B_TB_20137_A_20181108T101842_R16020_001.h5'

    try:
        hdffile = os.path.join(os.environ['HDFEOS_ZOO_DIR'], hdffile)
    except KeyError:
        pass

    run(hdffile)

