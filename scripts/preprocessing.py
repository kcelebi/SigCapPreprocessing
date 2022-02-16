import json
import os
import pandas as pd
import numpy as np

__all__ = ['getData','getLocationDF', 'getSortedKeys', 'getConnectedIndices', 'timeSub', 'rescaleDB', 'getDukeNodeData', 'getForeignData', 'OUT_OF_BOUNDS']

OUT_OF_BOUNDS = -300

'''
	Loads SigCap data files from directory or list of directories to get important 
	information for preprocessing.
	Returns data structure with format:
		data = {
		'id': [measurement keys],
		'location' : {'latitude': [measurement latitudes], 'longitude': [measurement longitudes]},
		'cell_info': [list of signal strength info],
		'time_stamp': [list of time stamps],
		'date' : [list of dates]}
'''
def getData(directory):
	data = {'id': [], 'location' : {'latitude': [], 'longitude': []}, 'cell_info': {'pci': [], 'ss': [], 'band': [], 'freq': []}, 'time_stamp': [], 'date' : [] }

	for i, f in enumerate(os.listdir(directory)):
		new_data = json.load(open(directory + '/' + f))

		signal_strengths = [x['ss'] for x in new_data['cell_info']]

		if len(signal_strengths) == 0:
			data['id'] += [i]
			data['location']['longitude'] += [new_data['location']['longitude']]
			data['location']['latitude'] += [new_data['location']['latitude']]

			data['cell_info']['ss'] += [OUT_OF_BOUNDS]
			data['cell_info']['pci'] += [None]
			data['cell_info']['band'] += [None]
			data['cell_info']['freq'] += [None]
		else:
			for j, v in enumerate(signal_strengths):
				data['id'] += [i]
				data['location']['longitude'] += [new_data['location']['longitude']]
				data['location']['latitude'] += [new_data['location']['latitude']]

				data['cell_info']['ss'] += [v]
				data['cell_info']['pci'] += [new_data['cell_info'][j]['pci']]
				data['cell_info']['band'] += [new_data['cell_info'][j]['band']]
				data['cell_info']['freq'] += [new_data['cell_info'][j]['freq']]

				data['time_stamp'] += [timeFormat(new_data['datetime']['time'])]

				data['date'] += [dateFormat(new_data['datetime']['date'])]

	return data

def getForeignData(data):
	foreign_data = {'id': [], 'location' : {'latitude': [], 'longitude': []}, 'cell_info': {'ss': [], 'pci': [], 'band' : [], 'freq': []}, 'time_stamp': [], 'date' : []}

	for i in range(len(data['id'])):
		if 40 != data['cell_info']['pci'][i] and 20 != data['cell_info']['pci'][i]:
			foreign_data['cell_info']['ss'] += [data['cell_info']['ss'][i]]
		else:
			foreign_data['cell_info']['ss'] += [OUT_OF_BOUNDS]

	foreign_data['id'] = data['id']
	foreign_data['location'] = data['location']
	foreign_data['time_stamp'] = data['time_stamp']
	foreign_data['date'] = data['date']
	foreign_data['cell_info']['pci'] = data['cell_info']['pci']
	foreign_data['cell_info']['band'] = data['cell_info']['band']
	foreign_data['cell_info']['freq'] = data['cell_info']['freq']

	return foreign_data


'''
	Gets data collected only from our CBRS node (pci: 40 or 20). Returns data structure of same format
'''

def getDukeNodeData(data):
	duke_data = {'id': [], 'location' : {'latitude': [], 'longitude': []}, 'cell_info': {'ss': [], 'band': [], 'freq': []}, 'time_stamp': [], 'date' : []}
	for i in range(len(data['id'])):
		if 40 == data['cell_info']['pci'][i] or 20 == data['cell_info']['pci'][i]:
			duke_data['cell_info']['ss'] += [data['cell_info']['ss'][i]]
		else:
			duke_data['cell_info']['ss'] += [OUT_OF_BOUNDS]

	duke_data['id'] = data['id']
	duke_data['location'] = data['location']
	duke_data['time_stamp'] = data['time_stamp']
	duke_data['date'] = data['date']
	duke_data['cell_info']['band'] = data['cell_info']['band']
	duke_data['cell_info']['freq'] = data['cell_info']['freq']

	return duke_data

'''
	Converts location element in data structure to pandas data frame to be
	inputted into Google Maps API
'''
def getLocationDF(data):
	return pd.DataFrame(data['location'])


'''
	Custom function to coerce dBm to something acceptable by Google Maps API
'''
def rescaleDB(data, function):
	return [function(x) for x in data['cell_info']['ss']]



'''
	Return keys in sorted order by the time stamp, can use this to grab other data
	in chronological order.
'''
def getSortedKeys(data):
	return sorted(data['id'], key = lambda x: data['time_stamp'][x])


'''
	Return indices of measurements where a connection to CBRS node is observed
'''
def getConnectedIndices(data):
	return [i for i in data['id'] if len(data['cell_info'][i]) > 0 ]

'''
	Translate timestamp to readable format
'''
def timeFormat(x):
    return x[0:2] + ':' + x[2:4] + ':' + x[4:6] + ':' + x[6:8]

'''
	Translate date to readable format
'''
def dateFormat(x):
	return x[0:4] + ',' + x[4:6] + ',' + x[6::]

'''
	Find time difference between time_stamp x and time_stamp y
'''
def timeSub(x,y):
    if y > x:
        temp = '' + x
        x = '' + y
        y = '' + temp
    x_comp = x.split(':')
    x = int(x_comp[0])*60*60 + int(x_comp[1])*60 + int(x_comp[2]) + int(x_comp[3])/100
    y_comp = y.split(':')
    y = int(y_comp[0])*60*60 + int(y_comp[1])*60 + int(y_comp[2]) + int(y_comp[3])/100
    
    return round(x-y, 4)


