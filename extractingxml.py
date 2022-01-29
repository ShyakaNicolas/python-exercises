import urllib.request
import json
import xml.etree.ElementTree as ET
url=input("Enter url:")
u=urllib.request.urlopen(url)
data=u.read()
xml_data=ET.fromstring(data)
search_str="comments/comment"
count_tags=xml_data.findall(search_str)
total=0
for tags in count_tags:
    c=tags.find('count')
    total+=int(c.text)
print(total)
