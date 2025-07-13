import requests
import json
import csv

api_key = 'rbysfTN4W6EFbIJxfup47rlbOzBZ16p1ys6wmrsK'
api_url = 'https://developer.nps.gov/api/v1'
endpoint = 'parks'
start = 0
limit = 50

# makes a csv with the headers we want
with open('api_calls/park_list.txt', 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    writer.writerow(['name', 'parkcode', 'park_addresstype', 'park_line1', 'park_city', 'park_statecode', 'park_postalcode', 'park_countrycode'])

# creates a request string for first iteration. 
first_request = f"{api_url}/{endpoint}?limit=1&start=0&api_key={api_key}"
api_call = requests.get(first_request)
api_results = api_call.json()
total = int(api_results['total'])

# print(total)

while start < total:
    request_string = f"{api_url}/{endpoint}?limit={limit}&start={start}&api_key={api_key}"
    api_call = requests.get(request_string)
    api_results = api_call.json()
    for row in range(0, len(api_results['data'])):
        name = api_results['data'][row]['name']
        parkcode = api_results['data'][row]['parkCode']
        park_postalcode = api_results['data'][row]['addresses'][0]['postalCode']
        park_city = api_results['data'][row]['addresses'][0]['city']
        park_statecode = api_results['data'][row]['addresses'][0]['stateCode']
        park_countrycode = api_results['data'][row]['addresses'][0]['countryCode']
        park_line1 = api_results['data'][row]['addresses'][0]['line1']
        park_addresstype = api_results['data'][row]['addresses'][0]['type']
        with  open('api_calls/park_list.txt', 'a', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow([name, parkcode, park_addresstype, park_line1, park_city, park_statecode, park_postalcode, park_countrycode])
    
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