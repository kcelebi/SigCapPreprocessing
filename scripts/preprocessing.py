import json
import os
import pandas as pd

__all__ = ['getData','getLocationDF', 'timeSub']

def getData(directory):
	data = {'id': [], 'location' : {'latitude': [], 'longitude': []}, 'cell_info': [], 'time_stamp': [], 'date' : []}
	if type(directory) == list:
		i=0
		for d in directory:
			for f in os.listdir(d):
				print(d + '/' + f)
				new_data = json.load(d + '/' + f)

				data['id'] += [i]

				data['location']['longitude'] += [new_data['location']['longitude']]
				data['location']['latitude'] += [new_data['location']['latitude']]

				data['cell_info'] += [ [x['ss'] if x['ss'] is not None else 0 for x in new_data['cell_info']] ]

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

			data['cell_info'] += [ [x['ss'] if x['ss'] is not None else 0 for x in new_data['cell_info']] ]

			data['time_stamp'] += [timeFormat(new_data['datetime']['time'])]

			data['date'] += [dateFormat(new_data['datetime']['date'])]

			i+= 1
	return data

def getLocationDF(data):
	return pd.DataFrame(data['location'])


def timeFormat(x):
    return x[0:2] + ':' + x[2:4] + ':' + x[4:6] + ':' + x[6:8]

def dateFormat(x):
	return x[0:4] + ',' + x[4:6] + ',' + x[6::]

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
