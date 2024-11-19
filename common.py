import base64
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from cryptography.fernet import Fernet
import pickle

def Background():    
    st.markdown(
            f"""
            <style>
            .stApp {{
                border: 3px solid black;
                border-top: 63px solid black;
                background: url(data:image/{'jpg'};base64,{base64.b64encode(open('Data/background3.jpg', "rb").read()).decode()});
                background-size: cover
            }}
            </style>
            """,
            unsafe_allow_html=True
        ) #set background image and page border  
def Authenticator():
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    encrypted_users = config['credentials']['usernames']
    cipher_suite = Fernet(st.secrets['key'])
    config['credentials']['usernames'] = pickle.loads(cipher_suite.decrypt(encrypted_users))
    st.session_state['authenticator'] = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    return config
def InitializeLogin():
    if 'name' not in st.session_state:
        st.session_state['name'] = None
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None
    if 'username' not in st.session_state:
        st.session_state['username'] = None
def encrypt_users(users, key):
    cipher_suite = Fernet(key)
    encrypted_users = cipher_suite.encrypt(pickle.dumps(users))
    return encrypted_users