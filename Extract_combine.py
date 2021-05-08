from Plot_AQI import avg_data_2013,avg_data_2014,avg_data_2015,avg_data_2016
import requests
import sys
import pandas as pd

#Beautiful Soup is a Python library for pulling data out of HTML and XML files.
from bs4 import BeautifulSoup
import os
import csv

#this function will clean and return all the records of a perticular month

def met_data(month, year):
    
    # opening and reading the html files
    file_html = open('data/Html_Data/{}/{}.html'.format(year,month), 'rb')
    plain_text = file_html.read()

    # this variable contains one perticular record of a month
    tempD = []
    # this variable contains all the records of a perticular month
    finalD = []

    # initializing BeautifulSoup
    soup = BeautifulSoup(plain_text, "lxml")
    #this for loop is used to iterate through all the table bodies and through
    #table rows and table headers to get each and every value
    for table in soup.findAll('table', {'class': 'medias mensuales numspan'}):
        for tbody in table:
            for tr in tbody:
                a = tr.get_text()
                tempD.append(a)
                
    #using this we'll get the no. of rows.There are 15 features
    rows = len(tempD) / 15   
    
    #Iterating through each rows and Features 
    #and Putting all rows in final list which is newtempD
    for times in range(round(rows)):    
        newtempD = []
        #iteratinh through features
        for i in range(15):
            newtempD.append(tempD[0])
            tempD.pop(0)
        finalD.append(newtempD)

    length = len(finalD)
    
    #Popping up last and 0th(mean Totoal) record which is of no use 
    finalD.pop(length - 1)
    finalD.pop(0)   

    for a in range(len(finalD)):
        finalD[a].pop(6)
        finalD[a].pop(13)
        finalD[a].pop(12)
        finalD[a].pop(11)
        finalD[a].pop(10)
        finalD[a].pop(9)
        finalD[a].pop(0)

    return finalD

#this function is used to combine many csv files
def data_combine(year, cs):
    for a in pd.read_csv('data/Real-Data/real_' + str(year) + '.csv', chunksize=cs):
        df = pd.DataFrame(data=a)
        mylist = df.values.tolist()
    return mylist


if __name__ == "__main__":
    
    #creating Real-Data folder if it is not present
    if not os.path.exists("data/Real-Data"):
        os.makedirs("data/Real-Data")
        
    for year in range(2013, 2017):
        
        # this variable will contains all the records of an year
        final_data = []
        
        #Creating csv file for each year
        with open('data/Real-Data/real_' + str(year) + '.csv', 'w') as csvfile:
            #Dialect means the data will like in excel sheet
            wr = csv.writer(csvfile, dialect='excel')
            wr.writerow(
                ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        for month in range(1, 13):
            temp = met_data(month, year)
            final_data = final_data + temp
         
        #This dynamic func will get pm values of all the years    
        pm = getattr(sys.modules[__name__], 'avg_data_{}'.format(year))()

        if len(pm) == 364:
            pm.insert(364, '-')

        #This will append pm values to our data in last column
        #which is our dependent feature
        for i in range(len(final_data)-1):
            
            final_data[i].insert(8, pm[i])

        with open('data/Real-Data/real_' + str(year) + '.csv', 'a') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            for row in final_data:
                flag = 0
                for elem in row:
                    if elem == "" or elem == "-":
                        flag = 1
                if flag != 1:
                    wr.writerow(row)
                    
    data_2013 = data_combine(2013, 600)
    data_2014 = data_combine(2014, 600)
    data_2015 = data_combine(2015, 600)
    data_2016 = data_combine(2016, 600)
     
    total=data_2013+data_2014+data_2015+data_2016
     
    #In Real-Data we have combineed Html data and aqi data
    with open('data/Real-Data/Real_Combine.csv', 'w') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(
            ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        wr.writerows(total)
        
        
df=pd.read_csv('data/Real-Data/Real_Combine.csv')