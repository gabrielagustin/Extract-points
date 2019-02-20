# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:16:04 2018

@author: gag

This script reads the satellite images in H5 format, extracts the environmental variables
required within the box of the study area. Within the study area, the values of the variables 
are extracted in the points (Lat, Lon) of the flight lines received through KML files.

Generates .csv files for each H5 satellite file, which contains the coordinates (Lat, Lon) 
of the HDF pixel and the KML point, the distance between them and the sensed variables required.

"""

import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import geopandas
import h5py
import functions
from time import time


if __name__ == "__main__":
    
    start_time = time()
    mydir = "/.../"
    for file in os.listdir(mydir):
        if file.endswith(".h5"):
            print(file)
            hdfFile = os.path.join(mydir, file)
            print('/home/gag/Escritorio/Extract/'+ file[:-3]+'.csv')
            # print(hdfFile)
            # If a certain environment variable is set, look there for the input
            # file, otherwise look in the current directory.
            # hdfFile = '/home/gag/Escritorio/SMAP_L1B/SMAP_L1B_TB_20137_A_20181108T101842_R16020_001.h5'
            try:
                hdfFile = os.path.join(os.environ['HDFEOS_ZOO_DIR'], hdfFile)
            except KeyError:
                pass

            ##### lee el archivo HDF, se extraen las variables  y se genera el objeto geopandas
            ####-------------------------------------------------------------------------------------
            #### lectura de la imagen H5 completa
            # nameVariable = '/Brightness_Temperature/tb_h'
            # print('Variable a extraer: '+str(nameVariable))
            # pdHDF = functions.readHDF(hdfFile, nameVariableArray)
            ####-------------------------------------------------------------------------------------
            #### lectura de un subset de la imagen H5 
            # box_lat = [-90, -60]
            # box_lon = [105, 180]
            box_lat = [-85, -65]
            box_lon = [120, 180]
            ####-------------------------------------------------------------------------------------
            #### se utilizan distintas funciones de lectura debido al diferente almacenamiento
            #### de las variables y las coordendas (Lat y Lon)
            ####-------------------------------------------------------------------------------------
            ### para las imágenes satelitales SMAP L1B
            ####-------------------------------------------------------------------------------------
            ### para SMAPL1B el nombre de las variables se forma con # nameVariable = group + nameVariable
            # nameVariableArray = ['/Brightness_Temperature/tb_h', '/Brightness_Temperature/tb_v', '/Brightness_Temperature/toa_h', '/Brightness_Temperature/toa_v']
            # pdHDF = functions.read_SMAP_L1B_HDF_box(hdfFile, box_lat, box_lon, nameVariableArray)
            ####-------------------------------------------------------------------------------------
            ### para las imágenes satelitales AMSR2
            ####-------------------------------------------------------------------------------------
            nameVariableArray = ['Brightness Temperature (10.7GHz,H)', 'Brightness Temperature (10.7GHz,V)', 'Brightness Temperature (18.7GHz,H)',
            'Brightness Temperature (18.7GHz,V)', 'Brightness Temperature (23.8GHz,H)', 'Brightness Temperature (23.8GHz,V)',
            'Brightness Temperature (36.5GHz,H)', 'Brightness Temperature (36.5GHz,V)', 'Brightness Temperature (6.9GHz,H)',
            'Brightness Temperature (6.9GHz,V)', 'Brightness Temperature (7.3GHz,H)', 'Brightness Temperature (7.3GHz,V)']
            pdHDF = functions.read_AMSR2_HDF_box(hdfFile, box_lat, box_lon, nameVariableArray)



            gdfHDF = geopandas.GeoDataFrame(pdHDF, geometry='Coordinates')
            # print(gdfHDF)
            print('Variables leidas del archivo HDF:')
            print(list(gdfHDF))

            coordinatesKMLarray = []
            resultArray = []
            namePointArray = []
            numberPointArray = []
            distanceArray = []

            for i in range(1,6):
                name = "flight_"+str(i)
                print("Vuelo: " +str(name))
                ##### lee el archivo KML y se crea un objeto geopandas
                kmlFile = "/home/gag/Escritorio/Lineas_de_vuelo_Antartida/2018_UWBRAD_"+name+".kml"
                pdKML = functions.readKML(kmlFile)
                gdfKML = geopandas.GeoDataFrame(pdKML, geometry='Coordinates')

                # print(gdfKML)
                total_rows = len(gdfKML.index)
                print('Numero de puntos en el KML: ' + str(total_rows))

                print('Numero de elemento en KML: ')
                for i in range(0,total_rows):
                    print(i)
                    ### se extraen los puntos
                    gdfKML_point = gdfKML['Coordinates'].ix[i]
                    namePointArray.append(gdfKML['point_name'].ix[i])
                    # print('Punto a buscar: ' + str(gdfKML_point))
                    coordinatesKMLarray.append(gdfKML_point)
                    ### se busca el valor de la variable en el geopandas del HDF
                    # result = functions.readPixel(gdfHDF, gdfKML_point)
                    distance, result = functions.readPixel(gdfHDF, gdfKML_point)
                    # print('Punto mas cercano:' + str(pixelClosest))
                    # print('Resultado Variable: ' + str(result))
                    resultArray.append(result)
                    distanceArray.append(distance)
                
                geosResult = pd.concat(resultArray)
                #### se agregan los puntos KML 
                geosResult['Coordinates_KML'] = coordinatesKMLarray
                geosResult['Point_name'] = namePointArray
                geosResult['Distance[degree]'] = distanceArray
                # print(list(geosResult))
            # geosResult =geosResult[["Point_name","Coordinates_KML","Coordinates_HDF", "/Brightness_Temperature/tb_h", "/Brightness_Temperature/tb_v", "/Brightness_Temperature/toa_h", "/Brightness_Temperature/toa_v"]] 
            geosResult =geosResult[["Point_name","Coordinates_KML","Coordinates_HDF","Distance[degree]", "/Brightness_Temperature/tb_h", "/Brightness_Temperature/tb_v", "/Brightness_Temperature/toa_h", "/Brightness_Temperature/toa_v"]] 
            geosResult.to_csv('/home/gag/Escritorio/Extract/'+ file[:-3]+'.csv', decimal = ",", index= False)
            print("Archivo creado con exito!")
            elapsed_time = time() - start_time
            print("Elapsed time: %.10f seconds." % elapsed_time)


