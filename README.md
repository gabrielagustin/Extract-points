# Extract-points
Extraction of points from satellite data using KML files

Description:

- read_HDF_using_KML

This script reads the satellite images in H5 format, extracts the environmental variables required within the box of the study area. Within the study area, the values of the variables are extracted in the points (Lat, Lon) of the flight lines received through KML files.

Generates .csv files for each H5 satellite file, which contains the coordinates (Lat, Lon) of the HDF pixel and the KML point, the distance between them and the sensed variables required, as shown: 


        Point_name / Coordinates_KML / Coordinates_HDF / Distance[degree] / tb_h / tb_v



- Functions 

It contains the necessary functions for extracting points such as: reading satellite images in H5 format, reading the KML files, calculating the pixels closest to the points using the Euclidean distance and finally extracting the the physical variables in said pixels.






Dependences:

    python - Geopandas
    python - H5py 
    python - Pykml
    python - Shapely
    python - Pandas
    python - NumPy
    python - Matplolib
