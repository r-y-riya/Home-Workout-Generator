import streamlit as st
import yaml
import Workout_Generator
import yagmail
from cryptography.fernet import Fernet

st.set_page_config(page_title='Home Workout Generator', page_icon='💪')
Workout_Generator.Background()
Workout_Generator.InitializeLogin()
config = Workout_Generator.Authenticator()

with open("email.yaml", "r") as f:
    email = yaml.safe_load(f)

encrypted_password = email["encrypted_password"].encode()
cipher_suite = Fernet(st.secrets['key'])
decrypted_password = cipher_suite.decrypt(encrypted_password).decode()

try:
    username_forgot_pw, email_forgot_password, random_password = st.session_state['authenticator'].forgot_password(location='main')
    if username_forgot_pw:
        yag = yagmail.SMTP('homeworkoutgenerate@gmail.com', decrypted_password, host='smtp.gmail.com', port=587, smtp_starttls=True, smtp_ssl=False)
        yag.send(
            to=email_forgot_password,
            subject='Temporary Password',
            contents=f'Your temporary password is: {random_password}<br>Please reset password after logging in'
        )
        st.success(f'New password sent securely to {email_forgot_password}') # Random password to be transferred to user securely
        config['credentials']['usernames'] = Workout_Generator.encrypt_users(config['credentials']['usernames'], st.secrets['key'])
        with open('config.yaml', 'w') as file: 
            yaml.dump(config, file, default_flow_style=False)
    elif username_forgot_pw == False:
        st.error('Username not found')
except Exception as e:
    st.error(e)



col1, col2, col3 = st.columns([1,1,4])
with col1:
    if st.button('**Exit**', type='primary', use_container_width=True):
        st.switch_page('Workout_Generator.py')
with col2:
    if st.button('**Login**', type='primary', use_container_width=True):
        st.switch_page('pages/1_Login.py')