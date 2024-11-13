import streamlit as st
import yaml
import Workout_Generator
from cryptography.fernet import Fernet
import pickle

st.set_page_config(page_title='Home Workout Generator', page_icon='💪')
st.write('Hi')