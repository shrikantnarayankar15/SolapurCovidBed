import requests
import json
import pandas as pd
import streamlit as st
from collections import defaultdict
import datetime

@st.cache(ttl=30*60)
def jsonDataVaccine():
#     dateString = datetime.date.today().strftime('%d-%m-%Y')
    dateString = '04-05-2021'
    payload = {'district_id':375,'date':dateString}
    url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
    data = requests.get(url, payload)
    print(data)
    data = data.json()
    print(data)
    return data

def getVaccine1845():
    data45 = []
    data18 = []
    data = jsonDataVaccine()
    for center in data['centers']:
        row18 = defaultdict()
        row45 = defaultdict()
        row18['center'] = center['name']
        row18['pincode'] = center['pincode']
        row18['fee_type'] = center['fee_type']
        
        row45['center'] = center['name']
        row45['pincode'] = center['pincode']
        row45['fee_type'] = center['fee_type']
        sessions = center['sessions']
        for i in sessions:
            if i['min_age_limit'] == 18:
                row18[i['date']] = i['available_capacity'] if i['available_capacity']>0 else None
            else:
                row45[i['date']] = i['available_capacity'] if i['available_capacity']>0 else None
                
        data45.append(row45)
        data18.append(row18)

    clearedData18 = pd.DataFrame(data18).dropna(thresh=4)
    clearedData45 = pd.DataFrame(data45).dropna(thresh=4)
    return clearedData18, clearedData45
