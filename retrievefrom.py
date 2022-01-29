import urllib.request,urllib.parse,urllib.error
from bs4 import BeautifulSoup
import ssl
import urllib

ctr=ssl.create_default_context()
ctr.check_hostname=False
ctr.verify_mode=ssl.CERT_NONE

link=input("Enter URL:")
count=int((input("Enter count:")))
pos=int((input("Enter count:")))
print ("Retrieve:",link)
for i in range(0,count):
    html=urllib.request.urlopen(link,context=ctr).read()
    soup=BeautifulSoup(html)
    tags=soup('a')
    link=tags[pos-1].get('href')
result=tags[pos-1].contents[0]
print(result)

