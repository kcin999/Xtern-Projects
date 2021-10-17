import pandas


df = pandas.read_json("raw_eventbrite.json",orient='values')

print(df)