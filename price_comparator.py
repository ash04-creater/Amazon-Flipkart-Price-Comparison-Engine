# import required files and modules
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

#generating url
def generate_url(part1,part2,search_for,ch):
  url=part1
  list1=list(search_for)
  #print(list1)
  l=len(list1)
  for i in range(0,l):
    if list1[i]==' ':
      list1[i]=ch
    url=url+list1[i]
  url=url+part2
  return url

search_for=input()
amazon_url=generate_url('https://www.amazon.in/s?k=','&ref=nb_sb_noss_1',search_for,'+')
fl_url=generate_url('https://www.flipkart.com/search?q=','&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off',search_for,'%20')

headers = {
    "Host": "www.amazon.in",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}
headers2 = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
r1 = requests.get(amazon_url, headers=headers)
r2=requests.get(fl_url,headers=headers2)
content2=r2.content
content = r1.content
if r1.status_code!=200 or r2.status_code!=200:
 print('Sorry cannot fetch data for this product right now!!')
 exit()
soup2=BeautifulSoup(content2)
soup1=BeautifulSoup(content)

data={
    "Sold By": [],
    "Product Info": [],
    "Price": [],
    "Link To Site": []
}

#scraping amazon
cnt=0
for t in soup1.find_all('span',attrs={'class':'a-size-medium a-color-base a-text-normal'},text=True):
      data["Sold By"].append('Amazon')
      data["Product Info"].append(t.get_text())
      cnt+=1
      if cnt==5:
        break
if len(data["Sold By"])==0 :
  for t in soup1.find_all('span',attrs={'class':'a-size-base-plus a-color-base a-text-normal'},text=True):
      data["Sold By"].append('Amazon')
      data["Product Info"].append(t.get_text())
      cnt+=1
      if cnt==5:
        break

cnt=0
for t in soup1.find_all('span',attrs={'class':'a-price-whole'},text=True):
      data["Price"].append(t.get_text())
      cnt+=1
      if cnt==5:
        break
cnt=0
for t in soup1.find_all('a',attrs={'class':'a-link-normal a-text-normal','href':re.compile("^https://www.amazon.in/")},href=True):
      data["Link To Site"].append(t.get('href'))
      cnt+=1
      if cnt==5:
        break


#scraping flipkart
cnt=0
for t in soup2.find_all('div',attrs={'class':'_4rR01T'},text=True):
      data["Sold By"].append('Flipkart')
      data["Product Info"].append(t.get_text())
      cnt+=1
      if cnt==5:
        break

if len(data["Sold By"])<=5:
  for t in soup2.find_all('a',attrs={'class':'s1Q9rs'},title=True):
      data["Sold By"].append('Flipkart')
      data["Product Info"].append(str(t.get_text()))
      cnt+=1
      if cnt==5:
        break

if len(data["Sold By"])<=5:
  for t in soup2.find_all('div',attrs={'class':'_2WkVRV'},text=True):
      data["Sold By"].append('Flipkart')
      data["Product Info"].append(str(t.get_text()))
      cnt+=1
      if cnt==5:
        break
  cnt=0
  for t in soup2.find_all('a',attrs={'class':'IRpwTa'},title=True):
      data["Product Info"][5+cnt]+=' '+str(t.get_text())
      cnt+=1
      if cnt==5:
        break

cnt=0
for t in soup2.find_all('div',attrs={'class':'_30jeq3 _1_WHN1'},text=True):
      data["Price"].append(t.get_text())
      cnt+=1
      if cnt==5:
        break
if len(data["Price"])<=5:
  for t in soup2.find_all('div',attrs={'class':'_30jeq3'},text=True):
      data["Price"].append(t.get_text())
      cnt+=1
      if cnt==5:
        break
cnt=0
for t in soup2.find_all('a',attrs={'class':'_1fQZEK','href':re.compile("^https://www.flipkart.com/")},href=True):
      data["Link To Site"].append(t.get('href'))
      cnt+=1
      if cnt==5:
        break
if len(data["Link To Site"])<=5:
  for t in soup2.find_all('a',attrs={'class':'IRpwTa','href':re.compile("^https://www.flipkart.com/")},href=True):
      data["Link To Site"].append(t.get('href'))
      cnt+=1
      if cnt==5:
        break
if len(data["Link To Site"])<=5:
  for t in soup2.find_all('a',attrs={'class':'s1Q9rs','href':re.compile("^https://www.flipkart.com/")},href=True):
      data["Link To Site"].append(t.get('href'))
      cnt+=1
      if cnt==5:
        break

df=pd.DataFrame(data=data)

for index,rows in df.iterrows():
  if rows["Sold By"]=='Amazon':
    rows["Link To Site"]='https://www.amazon.in'+rows["Link To Site"]
  else:
    rows["Link To Site"]='https://www.flipkart.com'+rows["Link To Site"]

df.to_excel("output.xlsx",index=False)
