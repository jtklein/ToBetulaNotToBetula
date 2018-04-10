import uuid
import requests

# Read the urls file
urls = []
with open('output.txt') as f:
    urls = f.read().splitlines()
    print(urls[0])
    
for url in urls:
    f = open(str(uuid.uuid4()) + ".jpg", 'wb')
    f.write(requests.get(url).content)
    f.close()
