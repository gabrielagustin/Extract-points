# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:16:04 2018

@author: gag
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
    mydir = "/home/gag/Escritorio/SMAP_L1B/"
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
            #### el nombre de las variables se forma con # nameVariable = group + nameVariable
            # nameVariable = '/Brightness_Temperature/tb_h'
            # print('Variable a extraer: '+str(nameVariable))
            nameVariableArray = ['/Brightness_Temperature/tb_h', '/Brightness_Temperature/tb_v', '/Brightness_Temperature/toa_h', '/Brightness_Temperature/toa_v']
            ####-------------------------------------------------------------------------------------
            #### lectura de la imagen H5 completa
            # pdHDF = functions.readHDF(hdfFile, nameVariableArray)
            ####-------------------------------------------------------------------------------------
            #### lectura de un subset de la imagen H5 
            # box_lat = [-90, -60]
            # box_lon = [105, 180]
            box_lat = [-85, -65]
            box_lon = [120, 180]
            pdHDF = functions.readHDF_box(hdfFile, box_lat, box_lon, nameVariableArray)



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

