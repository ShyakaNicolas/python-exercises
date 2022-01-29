import urllib.request,urllib.parse,urllib.error
from bs4 import BeautifulSoup
import ssl 

ctx=ssl.create_default_context()
ctx.check_hostname= False
ctx.verify_mode=ssl.CERT_NONE

links="http://py4e-data.dr-chuck.net/comments_1360090.html"
html=urllib.request.urlopen(links,context=ctx).read() 
soup=BeautifulSoup(html,'html.parser')
tags=soup('span')
s=0
c=0
for tag in tags:
    c+=1
    s+=int(tag.contents[0])
print ("count is",c)
print ("sum is",s)

