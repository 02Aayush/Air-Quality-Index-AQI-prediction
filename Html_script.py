# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 20:04:19 2021

@author: AayushGupta
"""
import os
import time     #execution Time to dwnld all html pages
import requests #It help to dwnld pages in form of html 
import sys      # It allows operating on the interpreter as it provides access to the variables and functions that interact strongly with the interpreter.

#through this function we'll get the dependent feature
def retrieve_html():
    for year in range(2013,2019):          #for years 2017 to 2021
        for month in range(1,13):          #for months 
            if(month<10):
                url='http://en.tutiempo.net/climate/0{}-{}/ws-421820.html'.format(month
                                                                          ,year)
            else:
                url='http://en.tutiempo.net/climate/{}-{}/ws-421820.html'.format(month
                                                                          ,year)
            texts=requests.get(url)   
            text_utf=texts.text.encode('utf=8')   #some characters to fix
            
            if not os.path.exists("data/Html_Data/{}".format(year)):
                os.makedirs("data/Html_Data/{}".format(year))
            with open("data/Html_Data/{}/{}.html".format(year,month),"wb") as output:
                output.write(text_utf)
            
        sys.stdout.flush()  #Flush everything that created in the file
        
if __name__=="__main__":
    start_time=time.time()
    retrieve_html()
    stop_time=time.time()
    print("Time taken {}".format(stop_time-start_time))

# Now we have all tha html pages