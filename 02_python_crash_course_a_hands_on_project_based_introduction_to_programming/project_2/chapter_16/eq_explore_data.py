import json  # for load json file object

from plotly import offline
from plotly.graph_objs import Layout  # for plotting

# from plotly.graph_objs import Scattergeo

# Explore the structure of the data
filename = 'data/eq_data_30_day_m1.json'
with open(filename) as f:
    all_eq_data = json.load(f)

# Save to readable json file
readable_file = 'data/readable_eq_data.json'
with open(readable_file, 'w') as f:
    json.dump(all_eq_data, f, indent=4)

# Extracting
all_eq_dicts = all_eq_data['features']  # Get list ('features' is key of the dictionary)
layout_title = all_eq_data['metadata']['title']

mags, lons, lats, hover_texts = [], [], [], []
for eq_dict in all_eq_dicts:
    mags.append(eq_dict['properties']['mag'])
    lons.append(eq_dict['geometry']['coordinates'][0])
    lats.append(eq_dict['geometry']['coordinates'][1])
    hover_texts.append(eq_dict['properties']['title'])

# Map the earthquakes
# data = [Scattergeo(lon=lons, lat=lats)]  # need to import Scattergeo
data = [{
    'type': 'scattergeo',
    'lon': lons,
    'lat': lats,
    'text': hover_texts,
    'marker': {
        'size': [5 * mag for mag in mags],
        'color': mags,
        'colorscale': 'Viridis',  # a colorscale that ranges from dark blue to bright yellow
        'reversescale': True,  # reverse scale so bright yellow for the lowest and dark blue for the highest
        'colorbar': {'title': 'Magnitude'},  # control appearance of the color scale
    }
}]

fig = {'data': data, 'layout': Layout(title=layout_title)}
offline.plot(fig, filename='global_earthquakes.html')
