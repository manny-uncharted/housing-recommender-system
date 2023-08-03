import os
import streamlit as st
from streamlit_chat import message

class ChatHistory:
    
    def __init__(self):
        self.history_pricing = st.session_state.get("history", [])
        st.session_state["history"] = self.history_pricing

    def default_greeting(self):
        return "Hey Sam ! 👋"

    def default_prompt(self, topic):
        return f"Hello ! Ask me anything about {topic} 🤗"

    def initialize_user_history(self):
        st.session_state["user1"] = [self.default_greeting()]

    def initialize_assistant_history(self, uploaded_file):
        st.session_state["assistant1"] = [self.default_prompt(topic="house prices")]

    def initialize(self, uploaded_file):
        if "assistant1" not in st.session_state:
            self.initialize_assistant_history(uploaded_file)
        if "user1" not in st.session_state:
            self.initialize_user_history()

    def reset(self, uploaded_file):
        st.session_state["history_pricing"] = []
        
        self.initialize_user_history()
        self.initialize_assistant_history(uploaded_file)
        st.session_state["reset_chat"] = False

    def append(self, mode, message):
        st.session_state[mode].append(message)

    def generate_messages(self, container):
        if st.session_state["assistant1"]:
            with container:
                for i in range(len(st.session_state["assistant1"])):
                    message(
                        st.session_state["user1"][i],
                        is_user=True,
                        key=f"history_{i}_user_pricing",
                        avatar_style="big-smile",
                    )
                    message(st.session_state["assistant1"][i], key=str(i), avatar_style="thumbs")

    def load(self):
        if os.path.exists(self.history_pricing_file):
            with open(self.history_pricing_file, "r") as f:
                self.history_pricing = f.read().splitlines()

    def save(self):
        with open(self.history_pricing_file, "w") as f:
            f.write("\n".join(self.history_pricing))
