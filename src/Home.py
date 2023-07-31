import streamlit as st


#Config
st.set_page_config(layout="wide", page_icon="💬", page_title="Sam | Chat-Bot 🤖")


#Title
st.markdown(
    """
    <h2 style='text-align: center;'>Sam, your home-recommendation assistant 🤖</h1>
    """,
    unsafe_allow_html=True,)

st.markdown("---")


#Description
st.markdown(
    """ 
    <h5 style='text-align:center;'>I'm Sam, an intelligent chatbot created by combining 
    the strengths of Langchain and Streamlit. I use large language models to provide
    context-sensitive interactions. My goal is to help you better find the apartment of your choice 🧠</h5>
    """,
    unsafe_allow_html=True)
st.markdown("---")







