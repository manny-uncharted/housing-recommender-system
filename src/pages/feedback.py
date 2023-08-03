import streamlit as st
import sys
import os
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv


# local imports
from modules.sidebar import Sidebar
from modules.layout import Layout
from modules.utils import Utilities
from modules.utils import send_email

load_dotenv()

sender = os.getenv("MAIL_USERNAME")

password = os.getenv("MAIL_PASSWORD")

with st.form("form1", clear_on_submit=True): 
    subject = "Housing Recommender Feedback"
    email = st.text_input("Enter email")
    message = st.text_area("Give your feedback on the chatbot")

    submit = st.form_submit_button("Submit this form")

    if submit:
        send_email(subject, message, sender=sender, recipients=email, password=password)
        st.success("Thank you for your feedback")
        