import os
import streamlit as st
from io import StringIO
import re
import sys
from modules.pricing_hist import ChatHistory
from modules.layout import Styling
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

history = reload_module('modules.pricing_hist')
layout_module = reload_module('modules.layout')
utils_module = reload_module('modules.utils')
sidebar_module = reload_module('modules.sidebar')

ChatHistory = history.ChatHistory
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
        sidebar.about()

        # Initialize chat history
        history1 = ChatHistory()
        try:
            template = """
                As AI assistant Sam, your task is to only determine property prices based on the description a user gives you. You are not expected to recommend any property. Only provide an estimate on what you think the property would cost per square meter and the rent per month cost. You have to provide responses in complete sentences and aim for around 99% accuracy. Ensure you give an estimate based on the information the user supplies and your knowledge of the property market and data accessible to you. Do ensure to state that you don't understand when you can't guarantee 99% accuracy.

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

                    # Initialize the chat history1
                    history1.initialize(uploaded_file)

                    # Reset the chat history1 if button clicked
                    if st.session_state["reset_chat"]:
                        history1.reset(uploaded_file)

                    if is_ready:
                        # Update the chat history1 and display the chat messages
                        history1.append("user1", user_input)

                        old_stdout = sys.stdout
                        sys.stdout = captured_output = StringIO()

                        output = st.session_state["chatbot"].conversational_chat(user_input)

                        sys.stdout = old_stdout

                        history1.append("assistant1", output)

                        # Clean up the agent's thoughts to remove unwanted characters
                        thoughts = captured_output.getvalue()
                        cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)
                        cleaned_thoughts = re.sub(r'\[1m>', '', cleaned_thoughts)

                        # Display the agent's thoughts
                        with st.expander("Display the agent's thoughts"):
                            st.write(cleaned_thoughts)

                history1.generate_messages(response_container)
        except Exception as e:
            st.error(f"Error: {str(e)}")


