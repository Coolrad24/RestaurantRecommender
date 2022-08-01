from asyncio.windows_events import NULL
from posixpath import split
from turtle import done
import pandas as pd
import bs4
from bs4 import BeautifulSoup
import requests
import csv
newData=[]
#header is a dictionary passed thru requests to make sure yelp doesn't block our webscrape
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
url=input("give me a yelp page to scrape")
req=requests.get(url,headers)
soup=BeautifulSoup(req.content,'html.parser')
restuarants=soup.find_all("li",class_= "border-color--default__09f24__NPAKY")
# The Place From Where the Food Originates
region=['Mexican','American','Italian','Indian','Latin American', 'Pakistani', 'Salvadoran','Tex-Mex']
# The Type Of Food To Be Served 
type=['Pizza','Taco','Sandwich','Wing','Hot Dogs','Coffee','Burger','Ice Cream', 'Steak', 'Chicken', 'Pasta','Seafood','Breakfast']
# The Type Of Restaurant Which is Serving This Type Of Food       
genre=['Restaurant','Bar','Fast Food','Bakery','Deli','Gas station', 'Farmers Market']
def getAttrib(arr,text): #this function will parse thru said array and return a value that represents which one shows up the most in the webpage
    present=[] #-will contains elements in the said array that are specifically in the webpage
    splitText=text.split()
    for i in range(len(arr)):
        if (arr[i] in text):
            present.append(arr[i]) #checking if each word is in the webpage and appending to present if so
    most="none"
    if(len(present)!=0):
        mostCount=0
        
        #loop thru all the present words use a count to get how many times its mentioned and return the one that is most mentioned
        for p in present:
            count=0
            for s in splitText:
                if s==p:
                    count+=1
            if(count>=mostCount):
                most=p
    else:
        return "none"
    return arr.index(most)
            

for i in range(len(restuarants)):
    data=[]
    
    try:
         names=restuarants[i].find("a", class_="css-1kb4wkh")
         data.append(names.get_text())
         
         
         
         link=names['href']
         
         
         req2=requests.get('https://www.yelp.com'+link+'?sort_by=rating_asc')

         soup2=BeautifulSoup(req2.content,'html.parser')
         
         pageText=soup2.get_text()
         # Add Restaurant Regions To Our List
         
         
         data.append(getAttrib(region,pageText)+1)
        # Add Restaurant Types To Our List
         data.append(getAttrib(type,pageText)+1)
        # Add Restaurant Genres To Our List
         data.append(getAttrib(genre,pageText)+1)
         
        
         


         ratings=soup2.find('div',{'role':'img'})
         data.append(ratings['aria-label'])
         data.append('https://www.yelp.com'+link)
         
         newData.append(data)#each restaurant's data is added into an array(data), which is then appended to another multidim array(newdata)
        
    except: 
        pass

del newData[0]  
#loop thru newdata array and add each array inside it(contains data of a restaurant) to a new csv row

for n in newData: 
    with open('database.csv','a',newline="") as f:
        csv.writer(f).writerow(n)
print('done')

