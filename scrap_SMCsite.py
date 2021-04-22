from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import streamlit as st
from config import urlAWS
from urllib.request import urlopen

@st.cache(ttl=60*2)
def dataScrap():
    data = urlopen(urlAWS).read().decode('utf-8')
    return data

class scrapSMC:
    def __init__(self, site_address):
        self.siteAddress=site_address
        self.text = self.getTextData(self.siteAddress)
        self.soup = BeautifulSoup(self.text, features='html.parser')
        self.summaryData = self.soup.find(id='Summary')
        self.allRows = self.summaryData.findAll('tr')
        self.DF1, self.DF2 = self.CreateDataFrame()
        self.processDF1()
        self.processDF2()

    
    def getHeaderTables(self):
        header = [[td.findChildren(text=True) for td in tr.findAll("th")] for tr in self.allRows]
        dataframesRows = []
        for table in header:
            if table:
                rows = []
                for row in table:
                    rows.append(row[0])
                dataframesRows.append(rows)
        return dataframesRows
    
    
    def processDF1(self):
        self.DF1 = self.DF1.apply(pd.to_numeric, errors='ignore')
        self.DF1.drop(['Select'], axis=1, inplace=True)
        self.DF1 = self.DF1.iloc[:-1,:]

    
    def processDF2(self):
        self.DF2 = self.DF2.apply(pd.to_numeric, errors='ignore')
        self.DF2 = self.DF2.iloc[:-1,:]
    
    
    def getAllRowsOfTable(self):
        data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in self.allRows]
        rows = []
        for table in data:
            if table:
                rows.append([row[0] for row in table if row])
        return rows

    
    def getTextData(self, address):
        return dataScrap()

    def CreateDataFrame(self):
        rows = self.getAllRowsOfTable()
        columnsOfTables = self.getHeaderTables()
        dataFrames = []
        for columns in columnsOfTables:
            getValidRows = [row for row in rows if len(row)==len(columns)]
            DF = pd.DataFrame(columns=columns, data=getValidRows) 
            dataFrames.append(DF)

        return dataFrames

    # @st.cache
    def getHospitalWiseAvailability(self):
        vacantBedsColumns = [row for row in self.DF1.columns if 'vacant' in row.lower()]
        
        return self.DF1[['Hospital Name', 'Landline No']+vacantBedsColumns].sort_values(by=['Vacant Beds'], ascending=False)

    # @st.cache
    def getHospitalWiseAvailabilityMahatma(self):
        # vacantBedsColumns = [row for row in self.DF1.columns if 'vacant' in row.lower()]
        return self.DF2.iloc[:,[1,2,3,7]].sort_values(by=['शिलक बेड'], ascending=False)
