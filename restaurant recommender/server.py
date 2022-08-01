from asyncio.windows_events import NULL
from unicodedata import name
from flask import Flask, jsonify, render_template, send_file, request,url_for,flash,redirect
from flask_cors import CORS, cross_origin
import predicter
import json
import requests
from bs4 import BeautifulSoup
import time
server=Flask(__name__)

cors = CORS(server)
server.config['CORS_HEADERS'] = "Content-Type"
@server.route('/restaurant',methods=['POST','GET'])
def run():
    temp=[]
    if request.method=='POST':
        rname=request.form.get('rname')
        raddress=request.form.get('raddress')
        print(raddress)
        print(rname)
        
        data=[rname,raddress]
        headers = {
        'authority': 'maps.googleapis.com',
        'method' : 'GET',
        'path': '/maps/api/mapsjs/gen_204?csp_test=true',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'zip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.yelp.com',
        'referer': 'https://www.yelp.com/',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'x-client-data': 'CJa2yQEIpbbJAQjBtskBCKmdygEIk6HLAQi4vMwBCMm8zAEIs8HMAQjEwcwBCNbBzAE=',

        }
        cookies = {'enwiki_session': '17ab96bd8ffbe8ca58a78657a918558'}
        print(data)
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
        try:
            for i in range(len(data)):
                data[i]=data[i].replace(" ","+")
                data[i]=data[i].replace(",",'%2C')
            url="https://www.yelp.com/search?find_desc="+data[0]+"&find_loc="+data[1]
            print(url)
            req=requests.get(url,headers=headers)
            
            soup=BeautifulSoup(req.content,'html.parser')
            print(soup.get_text())
            
            restuarants=soup.find_all("li",class_= "border-color--default__09f24__NPAKY")
            
            print(len(restuarants)) 
            ind=NULL
            for i in range(len(restuarants)):
                try:
                    names=restuarants[i].find("a", class_="css-1kb4wkh")
                    print(i)
                    if(names!='none'):
                        if(names.get_text()==rname):
                            ind=i
                            break
                except:
                    print('lol')
            span=restuarants[ind].find('div',class_='css-0 border-color--default__09f24__NPAKY')
            names=span.find('a',class_='css-1vowtmf')
            
            
            try:
                
                link=names['href']
                url='https://www.yelp.com'+link+'&sort_by=rating_asc'
                
                url=url[url.index('redirect_url='):len(url)]
                url=url.replace('redirect_url=',"")
                url=url.replace('%3A',':')
                url=url.replace("%2F",'/')
                t=url.index('&request_id')
                t1=url.index('&sort_')

                url=url.replace(url[t:t1],"")
                url=url.replace('&','?')
                print(url)
                req2=requests.get(url)
                soup2=BeautifulSoup(req2.content,'html.parser')
                pageText=soup2.get_text()
                print(pageText)
                
                print('1')
                ratings=soup2.find('div',{'role':'img'})
                all_reviews=soup2.find_all('li',class_='margin-b5__09f24__pTvws border-color--default__09f24__NPAKY')
                reviews=all_reviews[0:3]
                print('2')
                temp=[]
                temp.append(names.get_text())
                
                temp.append(getAttrib(region,pageText)+1)
                print('3')
                # Add Restaurant Types To Our List
                temp.append(getAttrib(type,pageText)+1)
                # Add Restaurant Genres To Our List
                temp.append(getAttrib(genre,pageText)+1)
                temp.append(ratings['aria-label'])
                
                for r in reviews:
                    rtemp=[]
                    review_stars=r.find('div',{'role':'img'})
                    rtemp.append(review_stars['aria-label'])
                    review_text=r.find('span',class_='raw__09f24__T4Ezm')
                    rtemp.append(review_text.get_text())
                    temp.append(rtemp)
                    print('4')
                print(temp)
            except:
                print('not found')
            Data_dict=temp
            arr=[temp[1],temp[2],temp[3]]
            prediction=predicter.model.predict([arr])
            suggest=predicter.Names[prediction[0]]
            link=predicter.links[prediction[0]]
            
        except:
            suggest='no restaurants found'
            Data_dict="error the restaurant you inputed was not found"
            link=''
    else:
         
        suggest='              '
        Data_dict="             "
        link='                     '
    print(Data_dict)
    return render_template('index.html',data=Data_dict,data2=suggest,data3=link)
if __name__ ==  '__main__':
  server.run(debug=True)
 