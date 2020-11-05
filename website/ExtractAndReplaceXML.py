#!/usr/bin/python3

#******************************VERSION INFO******************************#
# Version 1.2
# Written by Mohamed Farhan Fazal
# Needed Binaries:  1. urllib
#                   2. bs4
#                   3. re (Regular Expression)
#                   4. io
#******************************VERSION INFO******************************#


from urllib import request
from bs4 import BeautifulSoup
import re
import io

print("""*****************************************************************

                            Hola Amigos!!

*****************************************************************""")

# url = input("\n\nEnter the URL to the Sitemaps Index\nLeave blank for using default:\n\n")
# if len(url) < 1:
#     url = "http://192.168.0.102/sitemap_index.xml"
#     print("Using Default URL:",url)
# else:
#     print("Using URL:",url)
url = "https://ftm.ddns.net/sitemap_index.xml"
print("Using Default URL:",url)

print("\n\n")

handle = request.urlopen(url).read()
soup = BeautifulSoup(handle, 'html.parser')
sitemapTags = soup.find_all("loc")
sitemapURLList = [url]

for sitemaps in sitemapTags:
    if sitemaps.string.endswith(".xml"):
        sitemapURLList.append(sitemaps.string)

# wantToReplace = input("Do you want to replace text in files?\ntype 'y' for yes or 'n' or leave blank for no: \n\n")
wantToReplace = "y"
if wantToReplace == ('y' or 'Y'):
    # textToReplace = input("enter the text to replace: ")
    textToReplace = "//ftm"
    # textToBeReplacedWith = input("enter the text to be replaced with: ")
    textToBeReplacedWith = "//fazals"
# wantHttps = input("\n\nWant to change \"http\" to \"https\" for custom URL?: \ntype 'y' for yes or 'n' or leave blank for no: \n")
wantHttps = 'y'
print("\n\n")
for linksFromSitemaps in sitemapURLList:
    if wantToReplace == ('y' or 'Y'):
        if wantHttps == ('y' or 'Y'):
            textData = request.urlopen(linksFromSitemaps).read().decode().replace(textToReplace,textToBeReplacedWith).replace("http:"+textToBeReplacedWith,"https:"+textToBeReplacedWith)
        else:
            textData = request.urlopen(linksFromSitemaps).read().decode().replace(textToReplace,textToBeReplacedWith)
    else:
        textData = request.urlopen(linksFromSitemaps).read().decode()
    with io.open(linksFromSitemaps.split("/")[-1], "w", encoding="utf-8") as fileToBeWritten:
        fileToBeWritten.write(textData)
        fileToBeWritten.close()

print("""*****************************************************************

                        Voila!! Done!!

*****************************************************************""")
