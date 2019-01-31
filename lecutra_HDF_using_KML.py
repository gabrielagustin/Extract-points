# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:16:04 2018

@author: gag
 Script que lee el archivo H5, se extrae el box de la zona de estudio y las variables requeridas. 
 Con estos datos se genera el objeto geopandas. 
 Una vez generado el objeto geopandas del archivo H5 se cargan los archivos KML como geopandas,
 para luego realizar la extracción de los puntos. 
 Para encontrar los puntos en las imagenes satelitales se busca el pixel mas cercano en Latitud y Longitud. 

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
            # print(hdfFile)
            try:
                hdfFile = os.path.join(os.environ['HDFEOS_ZOO_DIR'], hdfFile)
            except KeyError:
                pass
           
            #### el nombre de las variables se forma con # nameVariable = group + nameVariable
            # nameVariable = '/Brightness_Temperature/tb_h'
            # print('Variable a extraer: '+str(nameVariable))
            nameVariableArray = ['/Brightness_Temperature/tb_h', '/Brightness_Temperature/tb_v', '/Brightness_Temperature/toa_h', '/Brightness_Temperature/toa_v']
            ####-------------------------------------------------------------------------------------
            #### lectura de la imagen H5 completa
            # pdHDF = functions.readHDF(hdfFile, nameVariableArray)
            ####-------------------------------------------------------------------------------------
            #### lectura de un subset de la imagen H5 
            box_lat = [-85, -65]
            box_lon = [120, 180]
            pdHDF = functions.readHDF_box(hdfFile, box_lat, box_lon, nameVariableArray)


            #### genera objeto geopandas con la imagen H5
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
                kmlFile = "/.../".kml"
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
       
            geosResult =geosResult[["Point_name","Coordinates_KML","Coordinates_HDF","Distance[degree]", "/Brightness_Temperature/tb_h", "/Brightness_Temperature/tb_v", "/Brightness_Temperature/toa_h", "/Brightness_Temperature/toa_v"]] 
            geosResult.to_csv('/.../'+'.csv', decimal = ",", index= False)
            print("Archivo creado con exito!")
            elapsed_time = time() - start_time
            print("Elapsed time: %.10f seconds." % elapsed_time)

