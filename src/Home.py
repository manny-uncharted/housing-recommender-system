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



# import streamlit as st
# # from cassandra.cluster import Cluster
# # from cassandra.auth import PlainTextAuthProvider
# # from cassandra.cqlengine import connection
# import hashlib

# # Connect to Cassandra cluster
# # cluster = Cluster(['your_cassandra_node_ip'])
# # session = cluster.connect('your_keyspace')

# # Create users table if not exists
# # session.execute("""
# #     CREATE TABLE IF NOT EXISTS users (
# #         username TEXT PRIMARY KEY,
# #         password TEXT,
# #         email TEXT
# #     )
# # """)

# def make_hashes(password):
#     return hashlib.sha256(str.encode(password)).hexdigest()

# def check_hashes(password, hashed_text):
#     return make_hashes(password) == hashed_text

# def signup(username, password, email):
#     hashed_password = make_hashes(password)
#     # session.execute(
#     #     """
#     #     INSERT INTO users (username, password, email) VALUES (%s, %s, %s)
#     #     """,
#     #     (username, hashed_password, email)
#     # )

# # def login(username, password):
# #     user_data = session.execute(
# #         """
# #         SELECT * FROM users WHERE username = %s
# #         """,
# #         (username,)
# #     ).one()

# #     if user_data and check_hashes(password, user_data.password):
# #         return user_data
# #     return None

# # Streamlit app
# def main():
#     st.title("Login & Signup App")

#     st.sidebar.title("Navigation")
#     page = st.sidebar.radio("Select Page", ["Home", "Login", "Signup"])

#     if page == "Home":
#         st.subheader("Welcome to the App")

#     elif page == "Signup":
#         st.subheader("Signup")
#         new_username = st.text_input("Username")
#         new_email = st.text_input("Email")
#         new_password = st.text_input("Password", type="password")
        
#         if st.button("Signup"):
#             signup(new_username, new_password, new_email)
#             st.success("Signup Successful! Now you can login.")

#     elif page == "Login":
#         st.subheader("Login")
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
        
#         if st.button("Login"):
#             user_data = login(username, password)
#             if user_data:
#                 st.success(f"Welcome {user_data.username}!")
#             else:
#                 st.error("Invalid Username/Password")

# if __name__ == "__main__":
#     main()
