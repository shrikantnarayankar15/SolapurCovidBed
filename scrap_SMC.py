from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
st.set_page_config(layout='wide')

@st.cache
def dataScrap():
    with open('solapurMNC.txt', 'rb') as f:
        return f.read()

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
        return smc.DF2.iloc[:,[1,2,3,7]].sort_values(by=['शिलक बेड'], ascending=False)

@st.cache
def district():
    distrinctCases = pd.read_csv('districts.csv')
    return distrinctCases

@st.cache
def districtVaccineDetails():
    vaccinated = pd.read_csv('cowin_vaccine_data_districtwise.csv')
    return vaccinated

if __name__ == '__main__':
    url = 'http://117.247.89.137:85/'

    smc = scrapSMC(url)
    availableBeds = smc.getHospitalWiseAvailability()
    availableBeds = availableBeds[availableBeds['Vacant Beds']!=0]
    columns = availableBeds.columns
    columns = [column.upper().replace('VACANT ', '') for column in columns]
    availableBeds.columns = columns
    print(columns)
    
    
    totalVacantBeds = availableBeds['BEDS'].sum(axis=0)
    availableBeds = availableBeds.style.background_gradient(cmap='RdPu', low=.5, high=0).highlight_null('red')
    st.title('Bed Availability Data for Solapur.   (Available: '+str(totalVacantBeds)+')')
    col1, col2 = st.beta_columns(2)
    
    col1.subheader('Hospital Wise Beds Availability of Vacant Beds (Click Column to sort)')
    col1.dataframe(availableBeds)
    
    distrinctCases = district()
    solapur = distrinctCases[distrinctCases['District']=='Solapur']
    solapur = solapur.iloc[-1].rename('Solapur Data')
    solapur = solapur.to_frame()
    solapur = solapur.drop('Other')
    

    
    mahatmaBeds = smc.getHospitalWiseAvailabilityMahatma()
    totalVacantBeds = mahatmaBeds['शिलक बेड'].sum(axis=0)
    mahatmaBeds = mahatmaBeds.style.background_gradient(cmap='RdPu', low=.5, high=0).highlight_null('PuRd')
    col2.subheader('महात्मा फुले जन आरोग्यसाठी राखीव बेडची माहिती.   (Available: '+str(totalVacantBeds)+')')
    col2.write(mahatmaBeds)

    my_expander = st.beta_expander(label='Covid And Vaccination Details')
    
    col5, col6 = my_expander.beta_columns(2)
    vaccinated = districtVaccineDetails()
    solapur = vaccinated[vaccinated['District']=='Solapur']
    data1=solapur.iloc[:,-10:].values[0]
    data2=vaccinated.iloc[0].values[-10:]
    final_data = pd.Series(index=data2, data=data1).rename('Solapur Data')

    col5.subheader('Solapur Covid Details')
    col5.dataframe(solapur.T, width=400)
    col6.subheader('Vaccinatation Details')
    col6.dataframe(final_data.T)
