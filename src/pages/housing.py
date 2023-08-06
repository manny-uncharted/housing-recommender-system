import os
import streamlit as st
from io import StringIO
import re
import sys
from modules.history import ChatHistory
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar
from pathlib import Path

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
Layout = layout_module.Layout
Utilities = utils_module.Utilities
Sidebar = sidebar_module.Sidebar

st.set_page_config(layout="wide", page_icon="💬", page_title="Housing Recommender system")

# Instantiate the main components
layout, sidebar, utils = Layout(), Sidebar(), Utilities()

layout.show_header()

user_api_key = utils.load_api_key()

if not user_api_key:
    layout.show_api_key_missing()
else:
    os.environ["OPENAI_API_KEY"] = user_api_key

    uploaded_file = utils.handle_upload(["pdf", "txt", "csv"])

    if uploaded_file:

        # Configure the sidebar
        sidebar.show_options()
        sidebar.about()

        # Initialize chat history
        history = ChatHistory()
        try:
            template = """
                As AI assistant Sam, your task is to only recommend properties based on a user's description. You are expected to recommend properties and provide full information about the property listing. If you don't find an exact listing based on the user description, indicate that and provide a property listing about 90% similar to the user description. Also ensure to search your records and provide information according to the user description.
                You have to provide responses in complete sentences and aim for around 99% accuracy. Ensure you give an estimate based on the information the user supplies and your knowledge of the property market and data accessible to you. Do ensure to state that you don't understand when you can't guarantee 99% accuracy. 
                Your default response format has to be followed strictly. Here is your default response formatting when displaying a listing should include: Title, property type, city, monthly rent, bedrooms, furnished, bathrooms, floor, closest station. If the user then requests for more information, you can provide more information about the property listing.

                Please adhere to the following guidelines:

                Provide the context in the given format.
                ======
                context: {context}
                ======
                question: {question}
                Let's proceed with your property-related inquiries or seek suggestions. Feel free to ask any questions!
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

                        sys.stdout = old_stdout

                        history.append("assistant", output)

                        # Clean up the agent's thoughts to remove unwanted characters
                        thoughts = captured_output.getvalue()
                        cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)
                        cleaned_thoughts = re.sub(r'\[1m>', '', cleaned_thoughts)

                        # Display the agent's thoughts
                        with st.expander("Display the agent's thoughts"):
                            st.write(cleaned_thoughts)

                history.generate_messages(response_container)
        except Exception as e:
            st.error(f"Error: {str(e)}")


