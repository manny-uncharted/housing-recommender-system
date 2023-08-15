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
from streamlit_chat import message
st.set_page_config(page_title = 'Rent Price Prediction', page_icon = ':bar_chart:', layout = 'wide')
import json

BASE_DIR = pathlib.Path().resolve()
EXPORT_DIR = BASE_DIR / 'housing_data'
ALL_PROPERTIES_PATH = EXPORT_DIR / 'all_properties.txt'
CATBOOST_MODEL_PATH = EXPORT_DIR / 'catboost_model'
CATEGORIES_PATH = EXPORT_DIR / 'categories.json'
MINI_PROPERTIES_PATH = EXPORT_DIR / 'mini_properties.txt'
df_path = BASE_DIR / 'housing data\Rentola-1.csv'
df = pd.read_csv(df_path)
df.columns = [col.replace(':','') for col in df.columns]

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



if 'responses' not in st.session_state.keys():
    st.session_state['responses'] = []
    st.session_state.responses.append("Hi 😉, I am Sammy a price prediction chatbot that helps you estimate the value of your property")
    st.session_state.responses.append('Please input details of the house of the house you want to predict, how many bedrooms do you want the house to have?')

    
if 'queries' not in st.session_state.keys():
    st.session_state['queries'] = []
    st.session_state['queries'].append('Hello Sammy👋')

if 'features_dict' not in st.session_state.keys():
     st.session_state['features_dict']  = {}


features = ['Bedrooms','Bathrooms', 'Furnished','Property type','City']
questions_dict = {'Bathrooms':'Specify the number of bathrooms in the house', 'Furnished':'IS the house furnished','Property type':'Specify Property type of the house','City':'What city is the property located in'}
accepted_values = {'Bedrooms':'num', 'Bathrooms':'num', 'Furnished' : ['Yes','No'], 'Property type': categories['Property type'], 'City': categories['City']}


if 'k' not in st.session_state.keys():
     st.session_state.k = 0




with st.container():
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_input("You:", key='input')
        submit_button = st.form_submit_button(label='Send')

    if submit_button:
        st.session_state['queries'].append(user_input)
        st.write(st.session_state.k)
        try:
            answer =  int(user_input) 
        except:
            answer = user_input 

        accepted = accepted_values[features[st.session_state.k]]

        if accepted == 'num':
            if type(answer) == int :
                
            
                st.session_state['features_dict'][features[st.session_state.k]] = answer 

                if st.session_state.k<=4:
                    st.session_state.k +=1

                    st.session_state['current_question'] = questions_dict[features[st.session_state.k]]
                    st.session_state.responses.append(st.session_state['current_question']) 
            
                
            else : 
                st.session_state['current_question'] = 'Error, please follow the specified format \n' + questions_dict[features[st.session_state.k]] 
                st.session_state.responses.append(st.session_state['current_question']) 

        else :
        
            if str(answer).strip().capitalize()  in accepted: 
                st.session_state['features_dict'][features[st.session_state.k]] = str(answer).strip().capitalize()
                st.session_state.k +=1
                if st.session_state.k <=4:
                    st.session_state['current_question'] = questions_dict[features[st.session_state.k]]
                    st.session_state.responses.append(st.session_state['current_question']) 
                   
            
                
            else:
                st.session_state['current_question'] = 'Error, please follow the specified format \n' + questions_dict[features[st.session_state.k]] 
                st.session_state.responses.append(st.session_state['current_question']) 

if st.session_state.k == 5:
    features_dict = st.session_state.features_dict
    features_dict['latitude'] = df[df['City']==features_dict['City']].latitude.mean()
    features_dict['longitude'] = df[df['City']==features_dict['City']].longitude.mean()
    features_dict['Furnished'] = "NaN" if str(features_dict['Furnished']).strip().capitalize() == 'No' else 'Furnished'

    features_df = pd.DataFrame(features_dict, index = [0])
    samp_df = features_df.copy()
    #st.dataframe(features_df)

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

    st.session_state["responses"].append(f'Estimated Rent Value of House is £{preds[0]:,.0f}')

inversed_queries = st.session_state['queries'][::-1]
inversed_responses = st.session_state['responses'][::-1]
with st.container():
        for i in range(1,len(inversed_queries)+1):
            message(inversed_responses[i-1], key=str(i))
            message(inversed_queries[i-1], is_user=True, key=str(i) + '_user')
        message(inversed_responses[-1], key=str(-1))
        



