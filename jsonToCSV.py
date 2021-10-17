import pandas
import json

#Opens Raw JSON
with open("raw_eventbrite.json", encoding='utf-8') as data_file:
	data = json.load(data_file)

#Takes JSON and brings it all to it's own level
df = pandas.json_normalize(data,'results')

#Takes care of escapte characters, like line-breaks.
df['summary'] = df['summary'].str.replace("\\n","")

#Keeps only the columns that I want
df = df[['id','start_date','start_time','_type','end_date','end_time','primary_organizer_id','primary_organizer.name','name','summary','primary_venue.name','primary_venue.address.longitude','primary_venue.address.latitude','primary_venue.address.localized_address_display']]

print(df)
df.to_csv("eventbrite.csv",index=False)