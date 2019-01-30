from pykml import parser
from os import path
import pandas as pd
import numpy as np
import math
from shapely.geometry import Point
import h5py


def readKML(filename):

    kml_file = path.join(filename)

    #### se leen los elementos del KML
    with open(kml_file) as f:
        folder = parser.parse(f).getroot().Document.Folder

    #### se separan los elementos, nombres de los puntos y las coordenadas
    plnm=[]
    cordi=[]
    for pm in folder.Placemark:
        plnm1 = pm.name
        plcs1 = pm.Point.coordinates
        plnm.append(plnm1.text)
        cordi.append(plcs1.text)
    # print(cordi)
    # print(plnm)   

    #### se genera el objeto pandas
    db=pd.DataFrame()
    db['point_name']=plnm
    db['cordinates']=cordi

    db['Longitude'], db['Latitude'], db['value'] = zip(*db['cordinates'].apply(lambda x: x.split(',', 2)))
    db["Longitude"] = pd.to_numeric(db["Longitude"])
    db["Latitude"] = pd.to_numeric(db["Latitude"])
    del db['cordinates']
    del db['value']

    db['Coordinates'] = list(zip(db.Longitude, db.Latitude))
    db['Coordinates'] = db['Coordinates'].apply(Point)

    # print(db)

    return db

####------------------------------------------------------------------------------------------------------------

def readHDF(FILE_NAME, nameVariableArray):
    db=pd.DataFrame()
    pd.options.mode.chained_assignment = None
    with h5py.File(FILE_NAME, mode='r') as f:
        for i in range(0, len(nameVariableArray)):
            nameVariable = nameVariableArray[i]
            # print('Variable a extraer:' +str(nameVariable))
            data = f[nameVariable][:]
            units = f[nameVariable].attrs['units']
            longname = f[nameVariable].attrs['long_name']
            _FillValue = f[nameVariable].attrs['_FillValue']
            valid_max = f[nameVariable].attrs['valid_max']
            valid_min = f[nameVariable].attrs['valid_min']        
            invalid = np.logical_or(data > valid_max,
                                data < valid_min)
            invalid = np.logical_or(invalid, data == _FillValue)
            data[invalid] = np.nan
            data = np.ma.masked_where(np.isnan(data), data)
            data = data.flatten('F')
            db[nameVariable] = data

        # Get the geolocation data
        Latitude = f['/Brightness_Temperature/tb_lat'][:]
        Longitude = f['/Brightness_Temperature/tb_lon'][:]

    Latitude = Latitude.flatten('F')
    Longitude = Longitude.flatten('F')
    #### se genera el objeto pandas
    db["Longitude"] = pd.to_numeric(Longitude)
    db["Latitude"] = pd.to_numeric(Latitude)    

    db['Coordinates'] = list(zip(db.Longitude, db.Latitude))
    db['Coordinates'] = db['Coordinates'].apply(Point)

    db = db.dropna()
    return db


####------------------------------------------------------------------------------------------------------------


def readHDF_box(FILE_NAME, box_lat, box_lon, nameVariableArray):
    db=pd.DataFrame()
    pd.options.mode.chained_assignment = None
    with h5py.File(FILE_NAME, mode='r') as f:
        for i in range(0, len(nameVariableArray)):
            nameVariable = nameVariableArray[i]
            # print('Variable a extraer:' +str(nameVariable))
            data = f[nameVariable][:]
            units = f[nameVariable].attrs['units']
            longname = f[nameVariable].attrs['long_name']
            _FillValue = f[nameVariable].attrs['_FillValue']
            valid_max = f[nameVariable].attrs['valid_max']
            valid_min = f[nameVariable].attrs['valid_min']        
            invalid = np.logical_or(data > valid_max,
                                data < valid_min)
            invalid = np.logical_or(invalid, data == _FillValue)
            data[invalid] = np.nan
            data = np.ma.masked_where(np.isnan(data), data)
            data = data.flatten('F')
            
            # Get the geolocation data
            latitude = f['/Brightness_Temperature/tb_lat'][:]
            longitude = f['/Brightness_Temperature/tb_lon'][:]
            lat_index = np.logical_and(latitude > box_lat[0], latitude < box_lat[1])
            lon_index = np.logical_and(longitude > box_lon[0], longitude < box_lon[1])
            box_index = np.logical_and(lat_index, lon_index)
            data = f[nameVariable][box_index]
            #### se genera el objeto pandas
            db[nameVariable] = data
            latitude = f['/Brightness_Temperature/tb_lat'][box_index]
            longitude = f['/Brightness_Temperature/tb_lon'][box_index]


    # Latitude = Latitude.flatten('F')
    # Longitude = Longitude.flatten('F')

    db["Longitude"] = pd.to_numeric(longitude)
    db["Latitude"] = pd.to_numeric(latitude)    

    db['Coordinates'] = list(zip(db.Longitude, db.Latitude))
    db['Coordinates'] = db['Coordinates'].apply(Point)

    db = db.dropna()
    return db


####------------------------------------------------------------------------------------------------------------
# Euclidean Distance
def Euclidean_distance(point1, point2):
    # print('Punto 1:' + str(point1))
    # print('Punto 2:' + str(point2))
    dist = point1.distance(point2) #Euclidean Distance
    # print('distancia: '+ str(dist))
    return dist

def closest(data, this_point):
    pointMinDistance = min(data, key=lambda x: Euclidean_distance(this_point, x))
    minDistance = pointMinDistance.distance(this_point)
    # print('Minima distancia: '+ str(minDistance))
    ### retorna minima distancia y el punto de minima distancia
    return minDistance, pointMinDistance
    # return pointMinDistance


def readPixel(geoPandasHDF, geoPandasKML_point):
    # print('Punto a buscar: ' + str(geoPandasKML_point))
    # pixelClosest = closest(geoPandasHDF['Coordinates'], geoPandasKML_point)
    minDistance, pointMinDistance = closest(geoPandasHDF['Coordinates'], geoPandasKML_point)
    pixelClosest = pointMinDistance
    # print('Punto mas cercano:' + str(pixelClosest))
    result = geoPandasHDF.loc[geoPandasHDF['Coordinates'] == pixelClosest]
    del result['Latitude']
    del result['Longitude']
    result.rename(columns={'Coordinates': 'Coordinates_HDF'}, inplace=True)
    # print(type(result))
    # resultVariable = result[nameVariable].item()
    # print('Resultado: ' + str(result))
    return minDistance, result
    # return result
