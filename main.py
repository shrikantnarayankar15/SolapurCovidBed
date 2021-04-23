from scrap_SMCsite import scrapSMC
import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
from config import districtLink, districtVaccineDetailsLink, style, urlScrap
st.set_page_config(page_title='Solapur Vacant Beds', page_icon='hospitalicon.png', layout='wide')

@st.cache(ttl=60*60*24)
def district(districtLink):
    print("Downloading district")
    distrinctCases = pd.read_csv('https://api.covid19india.org/csv/latest/district_wise.csv')
    return distrinctCases

@st.cache(ttl=60*60*24)
def districtVaccineDetails(districtVaccineDetailsLink):
    print("Downloading vaccine")
    vaccinated = pd.read_csv(districtVaccineDetailsLink)
    return vaccinated

if __name__ == '__main__':
    import streamlit_analytics
    
    streamlit_analytics.start_tracking()
    #store and get scrapped data
    smc = scrapSMC(urlScrap)

    

    #get Empty Vacant Beds
    availableBeds = smc.getHospitalWiseAvailability()
    availableBeds = availableBeds[availableBeds['Vacant Beds']!=0]
    columns = availableBeds.columns
    columns = [column.upper().replace('VACANT ', '') for column in columns]
    availableBeds.columns = columns
    
    totalVacantBeds = availableBeds['BEDS'].sum(axis=0)
    
    st.title('Bed Availability Data for Solapur.   (Available: '+str(totalVacantBeds)+')')
    st.text("")

    #Option to select hospital
    hospitalFind = st.beta_expander(label='Select Hospital (Click Here)')
    selectedHospitals = hospitalFind.multiselect("Enter Hospital Name:", options=list(availableBeds['HOSPITAL NAME'].values))
    print(selectedHospitals)
    hospitalFind.dataframe(availableBeds[availableBeds['HOSPITAL NAME'].isin(selectedHospitals)])
    
    #first row ui
    col1, col2 = st.beta_columns(2)
    
    #display first column
    availableBeds = availableBeds.style.background_gradient(cmap='RdPu', low=.5, high=0).highlight_null('red')
    col1.subheader('Hospital Wise Beds Availability of Vacant Beds (Click Column to sort)')
    col1.text("")
    col1.dataframe(availableBeds)
    
    #mahatma rakhiv beds data
    mahatmaBeds = smc.getHospitalWiseAvailabilityMahatma()
    totalVacantBeds = mahatmaBeds['शिलक बेड'].sum(axis=0)
    mahatmaBeds = mahatmaBeds.style.background_gradient(cmap='RdPu', low=.5, high=0).highlight_null('PuRd')

    #display second column
    col2.subheader('महात्मा फुले जन आरोग्यसाठी राखीव बेडची माहिती.   (Available: '+str(totalVacantBeds)+')')
    col2.text("")
    col2.write(mahatmaBeds)

    #ui for 2nd row
    my_expander = st.beta_expander(label='Covid And Vaccination Details')
    col3, col4 = my_expander.beta_columns(2)

    # Covid details for Solapur
    distrinctCases = district(districtLink)
    solapur = distrinctCases[distrinctCases['District']=='Solapur']
    solapur = solapur.iloc[-1].rename('Solapur Data')
    solapur = solapur.to_frame()

    #display first column
    col3.subheader('Solapur Covid Details')
    col3.dataframe(solapur, width=400)

    
    #vaccinated details for solapur
    vaccinated = districtVaccineDetails(districtVaccineDetailsLink)
    solapur = vaccinated[vaccinated['District']=='Solapur']
    data1=solapur.iloc[:,-10:].values[0]
    data2=vaccinated.iloc[0].values[-10:]
    final_data = pd.Series(index=data2, data=data1).rename('Solapur Data')  

    #display second column
    col4.subheader('Vaccinatation Details')
    col4.dataframe(final_data.T)
    
    st.markdown(style, unsafe_allow_html=True)
    streamlit_analytics.stop_tracking()
    
