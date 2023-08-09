import os
import io
import pandas as pd
import streamlit as st
import pdfplumber
import pathlib
from dotenv import load_dotenv
import smtplib
from typing import List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from modules.chatbot import Chatbot
from modules.embedder import Embedder

BASE_DIR = pathlib.Path().resolve()
folder_path = BASE_DIR / 'data'
# DATA_PATH = folder_path / 'properties.txt'
DATA_PATH = folder_path / 'try_properties.txt'

load_dotenv()




class Utilities:

    @staticmethod
    def load_api_key():
        """
        Loads the OpenAI API key from the .env file or 
        from the user's input and returns it
        """
        if not hasattr(st.session_state, "api_key"):
            st.session_state.api_key = None
        #you can define your API key in .env directly
        if os.path.exists(".env") and os.environ.get("OPENAI_API_KEY") is not None:
            user_api_key = os.environ["OPENAI_API_KEY"]
            st.sidebar.success("API key loaded from .env", icon="🚀")
        else:
            if st.session_state.api_key is not None:
                user_api_key = st.session_state.api_key
                st.sidebar.success("API key loaded from previous input", icon="🚀")
            else:
                user_api_key = st.sidebar.text_input(
                    label="#### Your OpenAI API key 👇", placeholder="sk-...", type="password"
                )
                if user_api_key:
                    st.session_state.api_key = user_api_key

        return user_api_key

    
    @staticmethod
    def handle_upload():
        """
        Handles and display uploaded_file
        :param file_types: List of accepted file types, e.g., ["csv", "pdf", "txt"]
        """
        uploaded_file = pathlib.Path(DATA_PATH)
        if uploaded_file is not None:
            def show_txt_file(uploaded_file):
                file_container = st.expander("Your TXT file:")
                with open(uploaded_file, "r") as file:
                    file.seek(0)
                    content = file.read()
                file_container.write(content)

                       
            file_extension = get_file_extension(uploaded_file)
            if file_extension== ".txt" : 
                show_txt_file(uploaded_file)

        else:
            st.session_state["reset_chat"] = True

        #print(uploaded_file)
        return uploaded_file

    @staticmethod
    def setup_chatbot(uploaded_file, model, temperature, template):
        """
        Sets up the chatbot with the uploaded file, model, and temperature
        """
        embeds = Embedder()

        with st.spinner("Processing...") and open(uploaded_file, "rb") as file:
            # with open(uploaded_file, "r") as file:
            file.seek(0)
            file_contents = file.read()
            # print(file_contents)
            file_name = get_file_extension(uploaded_file)
            # Get the document embeddings for the uploaded file
            vectors = embeds.retrieveDocumentEmbeddings(file_contents, file_name)
            print(vectors)

            qa_template = template

            # Create a Chatbot instance with the specified model and temperature
            chatbot = Chatbot(model, temperature, vectors, qa_template=qa_template)
        st.session_state["ready"] = True

        return chatbot

    

def get_file_extension(uploaded_file):
    file_ext = os.path.splitext(uploaded_file)[0].lower()
    return file_ext.split("/")[-1]


def send_emails(email_list, body_content, subject, email_from, pswd):

    for person in email_list:

        # Make the body of the email
        body = f"""
        Dear {person},\n \n 
        Thank you for submitting your suggestions to us. We would follow up on your comments and make prompt improvements. \n \n ,
        {body_content}
        """

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person
        msg['Subject'] = subject

        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))
        smtp_port = 587                 # Standard secure SMTP port
        smtp_server = "smtp.gmail.com"  # Google SMTP Server

        # Cast as string
        text = msg.as_string()
        # Connect with the server
        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Succesfully connected to server")
        print()


        # Send emails to "person" as list is iterated
        print(f"Sending email to: {person}...")
        TIE_server.sendmail(email_from, person, text)
        print(f"Email sent to: {person}")
        print()

    # Close the port
    TIE_server.quit()