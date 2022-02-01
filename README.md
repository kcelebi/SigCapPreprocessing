# SigCapPreprocessing

All of the data_### files are raw data collected directly for SigCap. The number at the end corresponds to the measurement's key which can be referenced in the [Measurement](#Measurement Keys) Keys section. 


# Preprocessing

The ``scripts`` folder contains the ``preprocessing.py`` file which has functions that makes it easier for us to analyze the files. Import with:

	from scripts.preprocessing import *

You can load all of the data from a measurement by using the ``getData()`` function. Example:

	data = getData('data_01_28_22_1')

The details on what that new data structure returns is documented in the ``preprocessing.py`` file. 

To make a heat map, we can need the locations first:
	
	data = getData('YOUR_DATASET')
	locations = getLocationsDF(data)

Then, we plug that into the the Google Maps API:

	fig = gmaps.figure(map_type = 'HYBRID')
	heatmap_layer = gmaps.heatmap_layer(locations)
	fig.add_layer(heatmap_layer)
	fig 					#returns final fig to view


# Measurement Keys

- (1): Walking around in Keohane dorm
- (2): Walking dorm to mailroom
- (3): Walking mailroom to dorm
- (4): Bus to Arts Annex
- (5): Arts Annex to Hollows