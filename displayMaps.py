#Imports
import pandas
import requests
import ipyleaflet
import ipywidgets


#Reads the given address file, which I renamed to address.csv
address = pandas.read_csv("address.csv")

url = "https://nominatim.openstreetmap.org/search"

markers = []
for index,row in address.itterrows():
	addressParams = {
		'street': row['Address'].split(', ')[0],
		'city:': row['Address'].split(', ')[1],
		'state': row['Address'].split(', ')[2].split(' ')[0],
		'postalcode': row['Address'].split(', ')[2].split(' ')[1],
		'format': 'json'
	}
	#Leverages openstreetmap API to find the latitude and longitude
	response = requests.get(url, params = addressParams)	
	response.raise_for_status()
	results = response.json()[0]

	#Creates teh marker with PopUP
	popUpMessage = ipywidgets.HTML()
	popUpMessage.value = results['display_name']
	markerToAppend = ipyleaflet.Marker(location=(results['lat'],results['lon']))
	markerToAppend.popup = popUpMessage
	markers.appened(markerToAppend)

#Markers have to be in a tuble, in order for them to be added to the MarkerCluster
markers = tuple(markers)

#centered on the middle of Indianapolis
m = ipyleaflet.Map(center=(39.791000,-86.148003), zoom=10, scroll_wheel_zoom=True)

#Adds the markers
m.add_layer(ipyleaflet.MarkerCluster(markers = markers))

#Display the map
m