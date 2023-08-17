import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt
from tqdm import tqdm 
import requests
import pickle
import pathlib
import streamlit as st 
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
st.set_page_config(page_title = 'Rent Price Prediction', page_icon = ':bar_chart:', layout = 'wide')
import json

BASE_DIR = pathlib.Path().resolve()
EXPORT_DIR = BASE_DIR / 'data'
ALL_PROPERTIES_PATH = EXPORT_DIR / 'all_properties.txt'
CATBOOST_MODEL_PATH = EXPORT_DIR / 'catboost_model'
CATEGORIES_PATH = EXPORT_DIR / 'categories.json'
MINI_PROPERTIES_PATH = EXPORT_DIR / 'mini_properties.txt'
OPENRENT_PATH = EXPORT_DIR / 'openrent.txt'
OUTPUT_PATH = EXPORT_DIR / 'output.txt'
f = open(CATEGORIES_PATH)
categories = json.load(f)

from catboost import CatBoostRegressor

model = CatBoostRegressor()      # parameters not required.
model.load_model(CATBOOST_MODEL_PATH)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_WAbot = load_lottieurl("https://lottie.host/08db7c19-26bf-400a-89a6-bfd39a0e36af/nsvFXm3afc.json")
st_lottie(lottie_WAbot, speed=1, height=430, key="initial")
st.header('House price Prediction')

st.subheader('Predicting rent price of houses ')
direct_feats = ['Bedrooms', 'latitude','longitude','Bathrooms']
steps = {'Bedrooms':1, 'latitude':0.0001,'longitude':0.0001, 'Bathrooms': 1}

features_dict = {}
with st.form('my_form'):
    st.write("Enter house specifications below")
    with st.container():
        for num,col in enumerate( st.columns(2, gap ='large')):
            ind_feats = list(range(len(direct_feats)))
            kk = [ind for ind in ind_feats if ind%2 == num ]
            for ind in kk :
                features_dict[direct_feats[ind]] = col.number_input(f'**{direct_feats[ind].capitalize()}**',step =steps[direct_feats[ind]])

    col1 , col2 = st.columns(2)
    features_dict['Property type'] = col1.radio('Property type', categories['Property type'])
    features_dict['Furnished'] = col2.radio('Furnished', categories['Furnished'])

    st.markdown('### Select the city the house belongs')
    features_dict['City']  = st.multiselect('City',categories['City'],max_selections = 1 )

    st.markdown('### Select the city of Origin of the player')
    # features_dict['City']  = st.multiselect('City',categories['City'],max_selections = 1 )
    features_dict['City'] = st.selectbox('City', categories['City'])

    submitted = st.form_submit_button("Predict")

    if submitted:
        features_df = pd.DataFrame(features_dict, index = [0])
        samp_df = features_df.copy()
        st.dataframe(features_df)

        for col in categories.keys():
            for value in categories[col]:
                if features_df[col].values[0] ==value:
                    features_df[f'{col}_{value}'] = 1
                else: 
                    features_df[f'{col}_{value}'] = 0
            features_df.drop(col,axis=1,inplace = True)

        features = ['Bedrooms', 'latitude', 'longitude', 'Bathrooms', 'Property type_Apartment', 'Property type_House', 'Property type_Room', 'Property type_Studio', 'City_ commercial road whitechapel, ', 'City_ kings cross', 'City_ london', 'City_ london, ', 'City_ studley court , ', 'City_ surrey quays', 'City_-blackfriarsroad', 'City_20 brock street', 'City_5 spa road', 'City_Albertembankment', 'City_Ambassador building', 'City_Angel', 'City_Archway', 'City_Baker street', 'City_Balham', 'City_Barfleur lane, deptford, se8', 'City_Barking', 'City_Barnet', 'City_Batterseapowerstation', 'City_Belvedere', 'City_Birmingham', 'City_Bloomsbury', 'City_Bollinder place', 'City_Borehamwood', 'City_Brentford', 'City_Brentwood', 'City_Brixton', 'City_Brook street', 'City_Canary wharf', 'City_Canarywharf', 'City_Cedar', 'City_Chelsea', 'City_Chigwell', 'City_Chislehurst', 'City_Church road teddington', 'City_Coventgarden', 'City_Crouch end', 'City_Croydon', 'City_Dartford', 'City_E14', 'City_Ealing common', 'City_Ec3r', 'City_Edgware', 'City_Epsom', 'City_Essex', 'City_Fairmont avenue canary wharf', 'City_Feltham', 'City_Golders green', 'City_Grays', 'City_Greater london', 'City_Greenford', 'City_Hammersmith', 'City_Hammersmith and fulham', 'City_Hampstead', 'City_Hanwell', 'City_Harrow', 'City_Hayes', 'City_Hendon', 'City_Highams park ', 'City_Highgate village', 'City_Hornchurch', 'City_Hounslow', 'City_Ilford', 'City_Isleworth', 'City_Iver', 'City_Jesmond', 'City_Kew', 'City_Kingston upon thames', 'City_Landmark pinnacle', 'City_Leyton', 'City_London', 'City_London 0js', 'City_London sw1p', 'City_Marble arch', 'City_Mill hill', 'City_New malden', 'City_Nine elms', 'City_Notting hill', 'City_Nunhead', 'City_Onestgeorgewharf', 'City_Penywern road, earls court, london, sw5', 'City_Perth road, london n4 3hb', 'City_Pinner', 'City_Rainham', 'City_Rainville road', 'City_Richmond', 'City_Rickmansworth', 'City_Rockmount road, plumstead, se18', 'City_Romford', 'City_Ruislip', 'City_Sevenoaks', 'City_South east england', 'City_South kensington', 'City_South norwood', 'City_Southall', "City_St john's wood", 'City_St johns wood', 'City_Stanmore', 'City_Sunbury-on-thames', 'City_Surbiton', 'City_Surrey', 'City_Sutton', 'City_Sw11', 'City_Sw16', 'City_Sw1h', 'City_Sw1p', 'City_Sw3', 'City_Tadworth', 'City_Teddington', 'City_The mount', 'City_Twickenham', 'City_Uxbridge', 'City_Vauxhall', 'City_Victoria', 'City_W1u', 'City_Walthamstow', 'City_Wandsworth', 'City_Wd23', 'City_Wd24', 'City_Welling', 'City_Wembley', 'City_West kensington', 'City_Westminster', 'City_Whitehall', 'City_Wood', 'City_Woolwich', 'Furnished_Yes']

        features_df = features_df[features]
        preds = model.predict(features_df)

        st.write(f'Estimated Rent Value of House is £{preds[0]:,.0f}')