import requests
import pandas


#Defines variables needed to grab restaurants needed in the area. 
parameters = {
	"page": 1
}

#Only have 50 calls with x-api-key, before it has to reset. I have used 32/50 to load restaurants.csv
headers = {
	"x-api-key": "739f6f8c1943396257a2d90d37ceca90",
	"x-rapidAPI-key": "6e00fec45fmsh590adad466c652fp14e842jsn5740f26fcb08",
	"X-RapidAPI-Host": "documenu.p.rapidapi.com"
}



#Finds the ZIPs needed from the area
zipCodes = []
address = pandas.read_csv("address.csv")

for index,row in address.iterrows():
	zipCode = row['Address'].split(', ')[2].split(' ')[1]
	zipCodes.append(zipCode)

#Grabs Data

create_dataframe = True

for zipCode in zipCodes:
	total_pages = 1
	parameters = {
		"page": 1
	}
	while parameters['page'] <= total_pages:
		try:
			r = requests.get("https://documenu.p.rapidapi.com/restaurants/zip_code/" + zipCode,params=parameters,headers=headers)
			r.raise_for_status()

			jsonResponse = r.json()

			if create_dataframe:
				restaurants = pandas.json_normalize(jsonResponse,"data")
				create_dataframe = False
			else:
				df2 = pandas.json_normalize(jsonResponse,"data")
				restaurants = restaurants.append(df2,ignore_index=True)
		except:
			print("Skpping call")

		total_pages = jsonResponse['total_pages']
		parameters['page'] = parameters['page'] + 1

restaurants.to_csv("restaurants.csv")