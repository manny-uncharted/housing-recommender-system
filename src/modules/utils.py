import os
import io
import pandas as pd
import streamlit as st
import pdfplumber
import pathlib
from dotenv import load_dotenv

from modules.chatbot import Chatbot
from modules.embedder import Embedder

BASE_DIR = pathlib.Path().resolve()
folder_path = BASE_DIR / 'data'
DATA_PATH = folder_path / 'properties.txt'

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
    def handle_upload(file_types):
        """
        Handles and display uploaded_file
        :param file_types: List of accepted file types, e.g., ["csv", "pdf", "txt"]
        """
        uploaded_file = pathlib.Path(DATA_PATH)
        
        # uploaded_file = st.sidebar.file_uploader("upload", type=file_types, label_visibility="collapsed")
        if uploaded_file is not None:
            def show_csv_file(uploaded_file):
                file_container = st.expander("Your CSV file:")
                with open(uploaded_file, "r") as file:
                    file.seek(0)
                    shows = pd.read_csv(file)
                file_container.write(shows)

            def show_pdf_file(uploaded_file):
                file_container = st.expander("Your PDF file:")
                with open(uploaded_file, "rb") as file:
                    with pdfplumber.open(file) as pdf:
                        pdf_text = ""
                        for page in pdf.pages:
                            pdf_text += page.extract_text() + "\n\n"
                file_container.write(pdf_text)

            def show_txt_file(uploaded_file):
                file_container = st.expander("Your TXT file:")
                with open(uploaded_file, "r") as file:
                    file.seek(0)
                    content = file.read()
                file_container.write(content)

                       
            file_extension = get_file_extension(uploaded_file)

            # Show the contents of the file based on its extension
            #if file_extension == ".csv" :
            #    show_csv_file(uploaded_file)
            if file_extension== ".pdf" : 
                show_pdf_file(uploaded_file)
            elif file_extension== ".txt" : 
                show_txt_file(uploaded_file)

        else:
            st.session_state["reset_chat"] = True

        #print(uploaded_file)
        return uploaded_file

    @staticmethod
    def setup_chatbot(uploaded_file, model, temperature):
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
            vectors = embeds.getDocEmbeds(file_contents, file_name)
            print(vectors)

            # Create a Chatbot instance with the specified model and temperature
            chatbot = Chatbot(model, temperature,vectors)
        st.session_state["ready"] = True

        return chatbot

    

def get_file_extension(uploaded_file):
    file_ext = os.path.splitext(uploaded_file)[0].lower()
    return file_ext.split("/")[-1]