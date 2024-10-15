import streamlit as st
import Workout_Generator

st.set_page_config(page_title='Home Workout Generator', page_icon='💪')

Workout_Generator.Background()
Workout_Generator.InitializeLogin()
config = Workout_Generator.Authenticator()

st.session_state['authenticator'].login(location='main')
    
if st.session_state['authentication_status']:
    st.switch_page('Workout_Generator.py')
elif st.session_state['authentication_status'] == False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] == None:
    st.warning('Please enter your username and password')


col1, col2, col3, col4, col5 = st.columns([.5,.7,1,1,1])
with col1:
    if st.button('**Exit**', type='primary', use_container_width=True):
        st.switch_page('Workout_Generator.py')
with col2:
    if st.button('**Register**', type='primary', use_container_width=True):
        st.switch_page('pages/2_Register.py')
with col3:
    if st.button('**Forgot Password**', type='primary', use_container_width=True):
        st.switch_page('pages/3_Forgot_Password.py')
with col4:
    if st.button('**Forgot Username**', type='primary', use_container_width=True):
        st.switch_page('pages/4_Forgot_Username.py')       

