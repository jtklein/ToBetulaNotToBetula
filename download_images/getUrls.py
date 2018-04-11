import requests
import json
import csv

paging = 0
baseUrl = "http://api.gbif.org/v1/occurrence/search"

# Set up the parameters we want to pass to the API.
parameters = {
    "taxonKey": "2874875",
    "basisOfRecord": "HUMAN_OBSERVATION",
    "mediaType": "StillImage",
    "limit": "100"
}

# Make a get request with these parameters, to get the results count
response = requests.get(baseUrl , params=parameters)

# Get the response data as a python object.
data = response.json()
count = data["count"]

urls = []
while paging < count:
    parameters["offset"] = paging

    # Make a get request with these parameters, to get the results count
    response = requests.get(baseUrl, params=parameters)
    # Print the status code of the response.
    print(response.status_code)

    # Get the response data as a python object.
    data = response.json()
    count = data["count"]

    # Destructure the results to get the image urls
    for result in data["results"]:
        media = result["media"]
        for medium in media:
            try:
                mediumFormat = medium["format"]
                mediumID = medium["identifier"]
                urls.append(mediumID)
                print(mediumID)
            except:
                print("Error")

    paging += 100

output = open('Fagus.txt', 'w')
for item in urls:
  output.write("%s\n" % item)
