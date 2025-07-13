import requests
import csv
from config import Config

api_key = Config.api_key
api_url = 'https://developer.nps.gov/api/v1'
endpoint = 'campgrounds'
start = 0
limit = 50

# makes a csv with the headers we want
with open('api_calls/campground_list.txt', 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    writer.writerow(['name', 'parkcode', 'url'])

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
    # for each row in the resulting data, write the values to the appropriate csv
    for row in range(0, len(api_results['data'])):
        name = api_results['data'][row]['name']
        parkcode = api_results['data'][row]['parkCode']
        campground_url = api_results['data'][row]['url']
        with  open('api_calls/campground_list.txt', 'a', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow([name, parkcode, campground_url])
    # update start to look for next 50 instances. 
    start += limit


# name
# parkCode
# url
# latitude
# longitude

# while start < total: 
    # call request, append values to output
    # then finish call. 

# store the park IDs, campground names, addresses and other information in some database. 
# park IDs will be required for microservices that need that information. 
# address information will be required for microservice which has to vend weather information. 