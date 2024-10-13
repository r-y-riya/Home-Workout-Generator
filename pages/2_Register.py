import streamlit as st
import yaml
import Workout_Generator

st.set_page_config(page_title='Home Workout Generator', page_icon='💪')
Workout_Generator.Background()
Workout_Generator.InitializeLogin()
config = Workout_Generator.Authenticator()

try:
    if st.session_state['authenticator'].register_user(location='main', captcha=False, merge_username_email=True):
        st.success('User registered successfully')
        config['credentials']['usernames'] = Workout_Generator.encrypt_users(config['credentials']['usernames'], st.secrets['key'])
        with open('config.yaml', 'w') as file: 
            yaml.dump(config, file, default_flow_style=False)
except Exception as e:
    st.error(e)

col1, col2, col3 = st.columns([1,1,4])
with col1:
    if st.button('**Exit**', type='primary', use_container_width=True):
        st.switch_page('Workout_Generator.py')
with col2:
    if st.button('**Login**', type='primary', use_container_width=True):
        st.switch_page('pages/1_Login.py')