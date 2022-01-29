import urllib.request
import json
url=input("Enter url:")
url=urllib.request.urlopen(url).read()
data=json.loads(url)
total=0
for tags in data['comments']:
     total+=tags["count"]
print(total)    
