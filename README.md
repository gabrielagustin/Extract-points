# Extract-points
Extraction of points from satellite data using KML files

Satellite Data:

  - SMAP: L1B, L1_S0_LORES and L1C
  - AMSR2 - GW1AM2 Level-1B
  - AQUARIUS L2 SCI


Description:

- read_HDF_using_KML

This script reads the satellite images in H5 format, extracts the environmental variables required within the box of the study area. Within the study area, the values of the variables are extracted in the points (Lat, Lon) of the flight lines received through KML files.

Generates .csv files for each H5 satellite file, which contains the coordinates (Lat, Lon) of the HDF pixel and the KML point, the distance between them and the sensed variables required, as shown: 


        Point_name / Coordinates_KML / Coordinates_HDF / Distance[degree] / tb_h / tb_v


- createBigDataSet

Script that reads all files .CSV by MONTHS within an initial file corresponding to a YEAR. Each file has .CSV files (each file corresponds to a satellite pass per hour) for all days of the month, having more than one pass per day.
It generates a pandas object that owns all the .CSV files and organizes them by date. Then, generate a single .CSV file.


- plotBigDataSet

Script that reads the CSV file. with the complete data set and performs the plot of the variables. For this, the mean and the deviation are calculated using panda group operations.


- functions 

It contains the necessary functions for extracting points such as: reading satellite images in H5 format, reading the KML files, calculating the pixels closest to the points using the Euclidean distance and finally extracting the the physical variables in said pixels.



- MATfilesConvertion

Script that reads the .MAT files and loads the parameters in a pandas object, it is necessary to know what the coordinates of the points are. Then, create a .KML file with the required data.


Dependences:

    python - Geopandas
    python - H5py 
    python - Pykml
    python - Simplekml
    python - Shapely
    python - Pandas
    python - NumPy
    python - Scipy
    python - Matplolib

