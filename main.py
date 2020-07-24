import folium
import pandas

data = pandas.read_csv("landings.csv")
data = data[data['year'] > 2005]
# data = data.drop(['year'], axis = 1)
data = data.drop_duplicates()
data = data.dropna()
lat = list(data["reclat"])
lon = list(data["reclong"])
year = list(data["year"])

def date_color(y):
    if y < 2010:
        return 'yellow'
    else:
        return 'red'


map = folium.Map(location=[24.7041, 77.10],
                zoom_start=6, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name="Meteorites")

for lt, ln, y in zip(lat, lon, year):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=int(y), radius = 10, fill_color= date_color(y), color = 'grey', fill = True, fill_opacity= 0.6 ))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), 
style_function = lambda x: {'fillColor': 'green' 
if x['properties']['POP2005'] < 2500000 
else 'blue' if 2500000 <= x['properties']['POP2005'] < 50000000 
else 'red' 
}))

map.add_child(fgp)
map.add_child(fgv)


map.add_child(folium.LayerControl())

map.save("index.html")
