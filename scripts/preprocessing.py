import json
import os
import pandas as pd
import numpy as np

__all__ = ['getData','getLocationDF', 'getSortedKeys', 'getConnectedIndices', 'timeSub', 'rescaleDB']

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
	data = {'id': [], 'location' : {'latitude': [], 'longitude': []}, 'cell_info': {'ss': [], 'pci': []}, 'time_stamp': [], 'date' : []}
	if type(directory) == list:
		i=0
		for d in directory:
			for f in os.listdir(d):
				print(d + '/' + f)
				new_data = json.load(d + '/' + f)

				data['id'] += [i]

				data['location']['longitude'] += [new_data['location']['longitude']]
				data['location']['latitude'] += [new_data['location']['latitude']]

				data['cell_info']['ss'] += [mod_mean([x['ss'] for x in new_data['cell_info']])]
				data['cell_info']['pci'] += [ [x['pci'] for x in new_data['cell_info']] ]

				data['time_stamp'] += [timeFormat(new_data['datetime']['time'])]

				data['date'] += [dateFormat(new_data['datetime']['date'])]

				i+= 1


	else:
		i = 0
		for f in os.listdir(directory):
			new_data = json.load(open(directory + '/' + f))
			data['id'] += [i]

			data['location']['longitude'] += [new_data['location']['longitude']]
			data['location']['latitude'] += [new_data['location']['latitude']]

			data['cell_info']['ss'] += [mod_mean([x['ss'] for x in new_data['cell_info']])]
			data['cell_info']['pci'] += [ [x['pci'] for x in new_data['cell_info']] ]
			
			data['time_stamp'] += [timeFormat(new_data['datetime']['time'])]

			data['date'] += [dateFormat(new_data['datetime']['date'])]

			i+= 1
	return data

'''
	Short helper method, sets no signal to a value of -300 dBm
'''
def mod_mean(x):
	return (OUT_OF_BOUNDS if len(x) == 0 else np.mean(x))

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
