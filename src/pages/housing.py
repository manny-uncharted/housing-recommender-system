import os
import streamlit as st
from io import StringIO
import re
import sys
from modules.history import ChatHistory
from modules.layout import Styling
from modules.utils import Utilities
from modules.sidebar import Sidebar
from pathlib import Path
from modules.utils import send_emails, send_emails_recommender
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

sender = os.getenv("MAIL_USERNAME")

password = os.getenv("MAIL_PASSWORD")
#To be able to update the changes made to modules in localhost (press r)
def reload_module(module_name):
    import importlib
    import sys
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
    return sys.modules[module_name]

history_module = reload_module('modules.history')
layout_module = reload_module('modules.layout')
utils_module = reload_module('modules.utils')
sidebar_module = reload_module('modules.sidebar')

ChatHistory = history_module.ChatHistory
Layout = layout_module.Styling
Utilities = utils_module.Utilities
Sidebar = sidebar_module.Sidebar

st.set_page_config(layout="wide", page_icon="💬", page_title="Housing Recommender system")

# Instantiate the main components
layout, sidebar, utils = Styling(), Sidebar(), Utilities()

layout.show_header()

user_api_key = utils.load_api_key()

if not user_api_key:
    layout.show_api_key_missing()
else:
    os.environ["OPENAI_API_KEY"] = user_api_key

    uploaded_file = utils.handle_upload()

    if uploaded_file:

        # Configure the sidebar
        sidebar.show_options()

        # Initialize chat history
        history = ChatHistory()
        try:
            template = """
                "Generate property recommendations based on provided data. Ensure accurate responses matching user preferences. Answer rent-related queries and compute cosine similarity (0.0-1.0) for each recommendation. Follow response format: Title, property type, city, rent, bedrooms, furnished, bathrooms, floor, closest station, cosine similarity score. Ask for more info if needed.

                
                ======
                context: {context}
                ======
                question: {question}
                Proceed with property inquiries!!"
            """
            chatbot = utils.setup_chatbot(
                uploaded_file, st.session_state["model"], st.session_state["temperature"], template=template
            )
            st.session_state["chatbot"] = chatbot

            if st.session_state["ready"]:
                # Create containers for chat responses and user prompts
                response_container, prompt_container = st.container(), st.container()

                with prompt_container:
                    # Display the prompt form
                    is_ready, user_input = layout.prompt_form()

                    # Initialize the chat history
                    history.initialize(uploaded_file)

                    # Reset the chat history if button clicked
                    if st.session_state["reset_chat"]:
                        history.reset(uploaded_file)

                    if is_ready:
                        # Update the chat history and display the chat messages
                        history.append("user", user_input)

                        old_stdout = sys.stdout
                        sys.stdout = captured_output = StringIO()

                        output = st.session_state["chatbot"].conversational_chat(user_input)
                        # output = st.session_state["chatbot"].conversational_chatagent(user_input)

                        sys.stdout = old_stdout
                        # print("Output: ", output)

                        history.append("assistant", output)
                        

                history.dispatch_messages(response_container)
                with st.form("form1", clear_on_submit=True): 
                            subject = "My Recommended property"
                            email = st.text_input("Enter email")

                            submit = st.form_submit_button("Send me my recommendation")
                            receipients = [email]
                            if submit:
                                try:
                                    send_emails_recommender(email_list=receipients , body_content=history.history[-1][-1], subject=subject, email_from=sender, pswd=password)
                                except:
                                    st.write("Error sending email")
                # print("History: ", history.history[-1])
                
        except Exception as e:
            st.error(f"Error: {str(e)}")


