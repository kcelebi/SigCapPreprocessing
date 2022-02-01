# SigCapPreprocessing

All of the ``data_MM_DD_YY_K`` files are raw data collected directly for SigCap. The number at the end corresponds to the measurement's key which can be referenced in the [Measurement Keys](#measurement-keys) section. 


# Preprocessing

The ``scripts`` folder contains the ``preprocessing.py`` file which has functions that makes it easier for us to analyze the files. Import with:

	from scripts.preprocessing import *

You can load all of the data from a measurement by using the ``getData()`` function. Example:

	data = getData('data_01_28_22_1')

The details on what that new data structure returns is documented in the ``preprocessing.py`` file. 

## Simple Heatmap

To make a heat map, we need the locations first:
	
	data = getData('YOUR_DATASET')
	locations = getLocationsDF(data)

Then, we plug that into the the Google Maps API:

	fig = gmaps.figure(map_type = 'HYBRID')
	heatmap_layer = gmaps.heatmap_layer(locations)
	fig.add_layer(heatmap_layer)
	fig 					#returns final fig to view

In order to use the Google Maps API you need an API key, make sure that's valid.

## Weighted Heatmap

We need the locations of our measurements as well as the signal strengths associated as weights. For each measurement there are often multiple signal strength measurements, of which, for now, I take the mean. For measurements with no connection to the CBRS node, I note the strength as 0. Each of these strengths (in dB) is scaled by -1 as the API only accepts positive integers:

	weights = [np.mean(x) * -1 if len(x) > 0 else 0 for x in data['cell_info']]

	fig = gmaps.figure(map_type = 'HYBRID')
	heatmap_layer = gmaps.heatmap_layer(
    		data = getLocationDF(data),
    		weights = weights, 		#assign our weights
    		max_intensity = max(weights)	#relative to current scope
	)
	fig.add_layer(heatmap_layer)
	fig					#returns final fig to view

# Measurement Keys

- (1): Walking around in Keohane 4E dorm
- (2): Walking dorm to mailroom
- (3): Walking mailroom to dorm
- (4): Bus to Arts Annex
- (5): Arts Annex to Hollows