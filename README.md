# SigCapPreprocessing

All of the ``data_MM_DD_YY_K`` files are raw data collected directly for SigCap. The number at the end corresponds to the measurement's key which can be referenced in the [Measurement Keys](#measurement-keys) section. 

## Contents

- [Preprocessing](#preprocessing)
- [Symbol "Heatmap"](#symbol-heatmap)
- [Simple Heatmap](#simple-heatmap)
- [Weighted Heatmap](#weighted-heatmap)
- [Measurement Keys](#measurement-keys)


## Preprocessing

The ``scripts`` folder contains the ``preprocessing.py`` file which has functions that makes it easier for us to analyze the files. Import with:

	from scripts.preprocessing import *

You can load all of the data from a measurement by using the ``getData()`` function. Example:

	data = getData('data_01_28_22_1')

The details on what that new data structure returns is documented in the ``preprocessing.py`` file. 

In order to get data specifically from the CBRS node on Davison quad:

	duke_data = getDukeNodeData(data)

## Symbol "Heatmap"

This is an alternative to using a heat map. We need to split up the locations into bins based on their signal strengths and assign a color to them. For now bins are:

- No signal: red
- Low Signal (> -150 dBm): yellow
- Usable Signal ( > -100 dBm): blue
- Good signal ( > -50 dBm): green

First, we obtain our locations:

	data = getData('YOUR_DATASET')
	locations = getLocationDF(data)

Then, we split them up by our bins:

	no_signal_index = np.where([(np.array(data['cell_info']['ss']) <= -100)])[1]
	little_signal_index = np.where([(np.array(data['cell_info']['ss']) > -100) & (np.array(data['cell_info']['ss']) < -90)])[1]
	medium_signal_index = np.where([(np.array(data['cell_info']['ss']) >= -90) & (np.array(data['cell_info']['ss']) < -80)])[1]
	high_signal_index = np.where(np.array(data['cell_info']['ss']) >= -80)[0]
	
Add the color bar:

	fig, ax = plt.subplots(figsize=(6, 1))
	fig.subplots_adjust(bottom=0.5)
	
	cmap = mpl.cm.viridis
	bounds = [-150, -100, -90, -80, 0]
	cmap = (mpl.colors.ListedColormap(['red', 'yellow', 'blue', 'green'])
		.with_extremes(over='0.25', under='0.75'))
	norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
	fig.colorbar(
	    mpl.cm.ScalarMappable(cmap=cmap, norm=norm),
	    cax=ax,
	    boundaries=[0] + bounds + [13],  # Adding values for extensions.
	    extend='both',
	    ticks=bounds,
	    spacing='proportional',
	    orientation='horizontal',
	    label='signal strength',
	)

Add the appropriate data to multiple layers:

	fig = gmaps.figure(map_type = 'HYBRID')
	no_signal_layer = gmaps.symbol_layer(
	    getLocationDF(data).iloc[no_signal_index],
	    fill_color = 'red',
	    stroke_color = 'red',
	    scale = 2
	)
	little_signal_layer = gmaps.symbol_layer(
	    getLocationDF(data).iloc[little_signal_index],
	    fill_color = 'yellow',
	    stroke_color = 'yellow',
	    scale = 2
	)
	medium_signal_layer = gmaps.symbol_layer(
	    getLocationDF(data).iloc[medium_signal_index],
	    fill_color = 'blue',
	    stroke_color = 'blue',
	    scale = 2
	)
	high_signal_layer = gmaps.symbol_layer(
	    getLocationDF(data).iloc[high_signal_index],
	    fill_color = 'rgba(23, 224, 100, 0.8)',
	    stroke_color = 'rgba(23, 224, 100, 0.8)',
	    scale = 2
	)

Add those layers to the figure:

	fig.add_layer(no_signal_layer)
	fig.add_layer(little_signal_layer)
	fig.add_layer(medium_signal_layer)
	fig.add_layer(high_signal_layer)
	fig

## Simple Heatmap

Note that the measurements can appear somewhat misleading for signal strength, best used for visualizing walking paht. To make a heat map, we need the locations first:
	
	data = getData('YOUR_DATASET')
	locations = getLocationsDF(data)

Then, we plug that into the the Google Maps API:

	fig = gmaps.figure(map_type = 'HYBRID')
	heatmap_layer = gmaps.heatmap_layer(locations)
	fig.add_layer(heatmap_layer)
	fig 					#returns final fig to view

In order to use the Google Maps API you need an API key, make sure that's valid.

## Weighted Heatmap

We need the locations of our measurements as well as the signal strengths associated as weights. For each measurement there are often multiple signal strength measurements, of which, for now, I take the mean. For measurements with no connection to the CBRS node, I note the strength as -300. Each of these strengths (in dB) is modified by a custom function as the API only accepts positive integers, this function in the example below is f(x) = x+300.

	weights = rescaleDB(data, lambda x: x + 300)
	fig = gmaps.figure(map_type = 'HYBRID')
	heatmap_layer = gmaps.heatmap_layer(
    		data = getLocationDF(data),
    		weights = weights, 		#assign our weights
    		max_intensity = max(weights)	#relative to current scope
	)
	fig.add_layer(heatmap_layer)
	fig					#returns final fig to view

# Measurement Keys

- (1): Walking around in Keohane 4E dorm with 2 seconds interval
- (2): Keohane 4E to BC mailroom with 2 seconds interval
- (3): BC mailroom to Keohane 4E with 2 seconds interval
- (4): Bus Stop to Arts Annex with 2 seconds interval
- (5): Arts Annex to Hollows dorm with 2 seconds interval
- (6): Davison to Crowell Quad(House H and G) with 10 seconds interval
- (7): Davison to Crowell Quad(House H and G) with 5 seconds interval
- (8): Davison to Crowell Quad(House H and G) with 1 second interval
- (9): Davison to main quad next to WU with 2 seconds interval
- (10): Keohane 4E to Perkins Library with 2 seconds interval
- (13): Main quad into Perkins Library with 1 second interval
- (18): Walking from throughout quad up to Davison
- (19): Walking throughout Davison Quad
- (20): Walking under Davison Quad along lawn
- (21): Walking behind libraries near Wilkinson from West of quad
