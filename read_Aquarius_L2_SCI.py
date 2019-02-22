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



def read_AQUARIUS_L2SCI_HDF_box(FILE_NAME, box_lat, box_lon, nameVariableArray):
    """
    Lee la imagen satelital AQUARIUS_L2SCI en formato .H5

    """
    db=pd.DataFrame()
    pd.options.mode.chained_assignment = None
    with h5py.File(FILE_NAME, mode='r') as f:
        for i in range(0, len(nameVariableArray)):
            nameVariable = nameVariableArray[i]
            print('Variable a extraer:' +str(nameVariable))
            data = f[nameVariable][:]
            # data = f[nameVariable][:,:,0]
            print(data.shape)         
            # Get the geolocation data
            latitude = f['/Navigation/scat_latfoot'][:,:,0] #cellatfoot #sclat
            # latitude = latitude*-1
            print(latitude)
            # print(latitude.shape)
            longitude = f['/Navigation/scat_lonfoot'][:,:,0] #cellonfoot #sclon
            # longitude = longitude*-1
            print(longitude)
            # print(longitude.shape)

            # ##### se lee solo el box_lat y box_lon de la variable
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

    with h5py.File(FILE_NAME, mode='r') as f:
        print('--------------------------------------------------------------------')
        print('Names of the groups in HDF5 file:')
        for key in f.keys():
             print(key) #Names of the groups in HDF5 file.
        print('--------------------------------------------------------------------')
        #Get the HDF5 group
        groupName = 'Aquarius Data'
        # groupName = 'Navigation'
        group = f[groupName]

        #Checkout what keys are inside that group.
        print('Keys are inside that group: ' + str(groupName))
        for key in group.keys():
            print(key)
        print('--------------------------------------------------------------------')




        
        ####--------------------------------------------------------------------
        #### Names of the groups in HDF5 file:
        # Aquarius Data
        # Aquarius Flags
        # Block Attributes
        # Converted Telemetry
        # Navigation    
        ####--------------------------------------------------------------------
        # Keys are inside that group: Aquarius Data
        ####--------------------------------------------------------------------
        # EIA_SSS_sens
        # EIA_err
        # IU_coupling_SSS_sens
        # IU_coupling_err
        # Kpc_HH_ant
        # Kpc_HH_toa
        # Kpc_HV_ant
        # Kpc_HV_toa
        # Kpc_VH_ant
        # Kpc_VH_toa
        # Kpc_VV_ant
        # Kpc_VV_toa
        # Kpc_total
        # NEDT_3_SSS_sens
        # NEDT_3_err
        # NEDT_H_SSS_sens
        # NEDT_H_err
        # NEDT_V_SSS_sens
        # NEDT_V_err
        # RFI_level_SSS_sens
        # RFI_level_err
        # SSS
        # SSS_matchup
        # SSS_nolc
        # SSS_unc
        # SSS_unc_EIA
        # SSS_unc_IU_coupling
        # SSS_unc_NEDT_3
        # SSS_unc_NEDT_H
        # SSS_unc_NEDT_V
        # SSS_unc_RFI_level
        # SSS_unc_TbV_ice_contam
        # SSS_unc_TbV_land_contam
        # SSS_unc_galact_Ta
        # SSS_unc_moon_Ta
        # SSS_unc_ran
        # SSS_unc_surface_temp
        # SSS_unc_sys
        # SSS_unc_wind_dir_rand
        # SSS_unc_wind_speed_rand
        # SSS_unc_wind_speed_syst
        # anc_SSS_argo
        # anc_SSS_hycom
        # anc_Tb_dw
        # anc_Tb_up
        # anc_cwat
        # anc_sm
        # anc_subsurf_temp
        # anc_surface_pressure
        # anc_surface_temp
        # anc_surface_temp_SSS_sens
        # anc_surface_temp_err
        # anc_swe
        # anc_swh
        # anc_trans
        # anc_wind_dir
        # anc_wind_speed
        # density
        # rad_Ta3
        # rad_Ta30
        # rad_TaH
        # rad_TaH0
        # rad_TaV
        # rad_TaV0
        # rad_TbH
        # rad_TbH_nolc
        # rad_TbH_rc
        # rad_TbH_rc_nolc
        # rad_TbV
        # rad_TbV_ice_contam_SSS_sens
        # rad_TbV_ice_contam_err
        # rad_TbV_land_contam_SSS_sens
        # rad_TbV_land_contam_err
        # rad_TbV_nolc
        # rad_TbV_rc
        # rad_TbV_rc_nolc
        # rad_Tb_consistency
        # rad_Tb_consistency_nolc
        # rad_Tf3
        # rad_Tf30
        # rad_TfH
        # rad_TfH0
        # rad_TfV
        # rad_TfV0
        # rad_dtb_sst_wspd_H
        # rad_dtb_sst_wspd_V
        # rad_exp_Ta3
        # rad_exp_Ta3_hhh
        # rad_exp_TaH
        # rad_exp_TaH_hhh
        # rad_exp_TaV
        # rad_exp_TaV_hhh
        # rad_exp_TbH
        # rad_exp_TbH0
        # rad_exp_TbV
        # rad_exp_TbV0
        # rad_far_rot_ang
        # rad_galact_Ta_SSS_sens
        # rad_galact_Ta_dir_3
        # rad_galact_Ta_dir_H
        # rad_galact_Ta_dir_V
        # rad_galact_Ta_err
        # rad_galact_Ta_ref_3
        # rad_galact_Ta_ref_GO_H
        # rad_galact_Ta_ref_GO_V
        # rad_galact_Ta_ref_H
        # rad_galact_Ta_ref_V
        # rad_galact_dTa_H
        # rad_galact_dTa_V
        # rad_geo_rot_ang
        # rad_hh_wind_speed
        # rad_hhh_wind_speed
        # rad_ice_frac
        # rad_land_frac
        # rad_moon_Ta_SSS_sens
        # rad_moon_Ta_err
        # rad_moon_Ta_ref_3
        # rad_moon_Ta_ref_H
        # rad_moon_Ta_ref_V
        # rad_pol_rot_ang
        # rad_solar_Ta_bak_3
        # rad_solar_Ta_bak_H
        # rad_solar_Ta_bak_V
        # rad_solar_Ta_dir_3
        # rad_solar_Ta_dir_H
        # rad_solar_Ta_dir_V
        # rad_solar_Ta_ref_3
        # rad_solar_Ta_ref_H
        # rad_solar_Ta_ref_V
        # rad_toa_H
        # rad_toa_H_nolc
        # rad_toa_V
        # rad_toa_V_nolc
        # rad_toi_3
        # rad_toi_H
        # rad_toi_V
        # rad_wind_dir_rand_SSS_sens
        # rad_wind_dir_rand_err
        # rad_wind_speed_rand_SSS_sens
        # rad_wind_speed_rand_err
        # rad_wind_speed_syst_SSS_sens
        # rad_wind_speed_syst_err
        # rim_anom
        # rim_anom1
        # rim_anom3
        # rim_anom5
        # rim_bf_irr
        # rim_irr
        # rim_pss
        # rim_sss
        # scat_HH_ant
        # scat_HH_exp
        # scat_HH_toa
        # scat_HV_ant
        # scat_HV_exp
        # scat_HV_toa
        # scat_VH_ant
        # scat_VH_exp
        # scat_VH_toa
        # scat_VV_ant
        # scat_VV_exp
        # scat_VV_toa
        # scat_esurf_H
        # scat_esurf_H_uncertainty
        # scat_esurf_V
        # scat_esurf_V_uncertainty
        # scat_ice_frac
        # scat_land_frac
        # scat_tot_toa
        # scat_wind_speed
        # spiciness
        # wind_uncertainty
        ####--------------------------------------------------------------------

        
        name = '/Aquarius Data/rad_toa_H'

        box_lat = [-85, -65]
        box_lon = [120, 180]

        nameVariableArray = ['/Aquarius Data/rad_toa_H', '/Aquarius Data/rad_toa_V']

        df = read_AQUARIUS_L2SCI_HDF_box(FILE_NAME, box_lat, box_lon, nameVariableArray)
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
        name = '/Aquarius Data/rad_toa_H'
        # m.scatter(df.Longitude, df.Latitude, c=df['Brightness Temperature (10.7GHz,H)'], s=1, cmap=plt.cm.jet,
        #         edgecolors=None, linewidth=0)
        m.scatter(df.Longitude, df.Latitude, c=df[name], s=1, cmap=plt.cm.jet,
                edgecolors=None, linewidth=0)
        cb = m.colorbar(location="bottom", pad=0.7)    
        cb.set_label('[°K]')
        plt.title(name)

        plt.show()
    

if __name__ == "__main__":

    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
    # hdffile = '/home/gag/Escritorio/Extract/Aquarius/Q2015001000100.L2_SCI_V5.0'
    hdffile = '/home/gag/Escritorio/Extract/Aquarius/Q2015053093500.L2_SCI_V5.0'

    try:
        hdffile = os.path.join(os.environ['HDFEOS_ZOO_DIR'], hdffile)
    except KeyError:
        pass

    run(hdffile)

