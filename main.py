from scrap_SMCsite import scrapSMC
import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
from get_vaccine_data import getVaccine1845
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
    
    # Updated Vaccine Page
#     data18, data45 = getVaccine1845()
    
#     if data18.shape[0] == 0 and data45.shape[0] ==0:
#         st.title('No Vaccine Available for Above 18 and 45(7 days Data)')
#         st.text("")
#     elif data18.shape[0] == 0:
#         st.title('Vaccine Available for above 45 (7 days Data)')
#         st.text("")
#     elif data45.shape[0] == 0:
#         st.title('Vaccine Available for above 18(7 days Data)')
#         st.text("")
#     else:
#         st.title('Above 18 and 45 Vaccine are available (7 days Data)')
#         st.text("")

#     #Option to select Age Group and hospital
#     vaccineAvailable = st.beta_expander(label='For Vaccine Details (Click Here)')
#     col1, col2, col3 = vaccineAvailable.beta_columns(3)
#     selectAgeGroup = col1.selectbox("Select Age Group", ('Above 45','Above 18'))
#     values = None
#     pinValues = None
#     if selectAgeGroup == 'Above 45':
#         values = data45['center'].values
#         pinValues = data45['pincode'].values
#     else:
#         values = data18['center'].values
#         pinValues = data18['pincode'].values
#     selectHospital = col3.multiselect("Enter Hospital Name:", options=list(values))
#     selectedPins = col2.selectbox("Enter Pincode:", options=list(pinValues))
#     selectedData = data45 if selectAgeGroup == 'Above 45' else data18
#     if selectHospital:
#         vaccineAvailable.write(selectedData[selectedData['center'].isin(selectHospital)])
#     elif selectedPins:
#         vaccineAvailable.write(selectedData[selectedData['pincode']==selectedPins])
#     else:
#         vaccineAvailable.write(selectedData)
    # vaccineAvailable.write(data45 if selectAgeGroup == 'Above 45' else data18)
    
    #store and get scrapped data
    smc = scrapSMC(urlScrap)

    #get Empty Vacant Beds
    availableBeds = smc.getHospitalWiseAvailability()
    availableBeds = availableBeds[availableBeds['Vacant Beds']!=0]
    columns = availableBeds.columns
    columns = [column.upper().replace('VACANT ', '') for column in columns]
    availableBeds.columns = columns
    
    totalVacantBeds = availableBeds['BEDS'].sum(axis=0)

    # Title
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
    totalVacantBeds = mahatmaBeds['???????????? ?????????'].sum(axis=0)
    mahatmaBeds = mahatmaBeds.style.background_gradient(cmap='RdPu', low=.5, high=0).highlight_null('PuRd')

    #display second column
    col2.subheader('????????????????????? ???????????? ?????? ?????????????????????????????? ??????????????? ??????????????? ??????????????????.   (Available: '+str(totalVacantBeds)+')')
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
    col3.subheader('Solapur Covid Summary')
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
    
