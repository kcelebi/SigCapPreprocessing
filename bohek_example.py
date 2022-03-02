from bokeh.io import output_notebook
output_notebook()
bokeh_width, bokeh_height = 800, 600

#separate these in different cells

from bokeh.io import show
from bokeh.plotting import gmap
from bokeh.models import GMapOptions
from bokeh.models import ColumnDataSource
from bokeh.transform import linear_cmap
from bokeh.palettes import Plasma256 as palette
from bokeh.models import ColorBar
from bokeh.models import HoverTool

def plot(lat, lng, df, title, zoom = 19, map_type = 'hybrid'):
    gmap_options = GMapOptions(
        lat = lat,
        lng = lng,
        map_type = map_type,
        zoom = zoom
    )
    
    hover = HoverTool(
        tooltips = [
            ('ss', '@ss{0.0}'),
            ('band', '@band{0.0}'),
            ('freq', '@freq{0.0}')
        ]
    )
    
    p = gmap(
        'AIzaSyCtZYWpMyGTqwYhiJ-focuI20YbB461u1M',
        gmap_options,
        title = title,
        width = bokeh_width,
        height = bokeh_height,
        tools = [hover, 'pan']
    )
    
    source = ColumnDataSource(df)
    
    mapper = linear_cmap('ss', palette, -130, -60)
    
    center = p.circle(
        'longitude',
        'latitude',
        size = 8,
        color = mapper,
        source = source
    )
    
    color_bar = ColorBar(color_mapper = mapper['transform'], location = (0,0))
    
    p.add_layout(color_bar, 'right')
    
    show(p)
    
    return p

# separate here too 

#load data
data = getData('../data_03_01_22_19')

#define center
lat = getLocationDF(getDukeNodeData(data))['latitude'][0] # define center of image which can be just any point
lon = getLocationDF(getDukeNodeData(data))['longitude'][0]

#define data frame
df = getLocationDF(getDukeNodeData(data))

#add ss and other info to df
df['ss'] = getDukeNodeData(data)['cell_info']['ss']
df['band'] = getDukeNodeData(data)['cell_info']['band']
df['freq'] = getDukeNodeData(data)['cell_info']['freq']

#plot
p = plot(lat, lon, df, title = 'data_03_01_22_19')