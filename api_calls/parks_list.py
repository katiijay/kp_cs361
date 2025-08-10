import requests
from config import Config

# API variables
api_key = Config.api_key
api_url = 'https://developer.nps.gov/api/v1'
endpoint = 'parks'
start = 0
limit = 50
# DB variables
myclient = Config.mongo_connection
mydb = myclient["CS361"]
mycollection = mydb["parks"]
collectionname = 'parks'

# empties DB collection
mydb[collectionname].drop()

# creates a request string for first iteration. 
first_request = f"{api_url}/{endpoint}?limit=1&start=0&api_key={api_key}"
api_call = requests.get(first_request)
api_results = api_call.json()
total = int(api_results['total'])

# while loop to handle api call result limit. 
while start < total:
    request_string = f"{api_url}/{endpoint}?limit={limit}&start={start}&api_key={api_key}"
    api_call = requests.get(request_string)
    api_results = api_call.json()
    # for each row in the resulting data, write the values to mongodb
    for row in range(0, len(api_results['data'])):
        parkdata = api_results['data'][row]
        mongoimport = { 
                        '_id': parkdata['parkCode'],
                         "data": parkdata
                       }
        x = mycollection.insert_one(mongoimport)
    
    start += limit
print(mydb[collectionname].count_documents({}))