import streamlit as st
import pandas as pd
import random
import base64
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from cryptography.fernet import Fernet
import pickle

st.set_page_config(page_title='Home Workout Generator', page_icon='💪', initial_sidebar_state='collapsed')
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)
def encrypt_users(users, key):
    cipher_suite = Fernet(key)
    encrypted_users = cipher_suite.encrypt(pickle.dumps(users))
    return encrypted_users
def InitializeLogin():
    if 'name' not in st.session_state:
        st.session_state['name'] = None
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None
    if 'username' not in st.session_state:
        st.session_state['username'] = None
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

st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)

InitializeLogin()
config = Authenticator()
Background()


if st.session_state['authentication_status']:
    st.write(f'**Welcome {st.session_state['name']}**')

button1,button2,button3,buffer = st.columns([.45,.8,.8,1.5], vertical_alignment='bottom')

with button1:
    if not st.session_state['authentication_status']:
        if st.button('**Login**'):
            st.switch_page('pages/1_Login.py')
    else:
        
        st.session_state['authenticator'].logout('**Logout**', 'main')
with button2:
    if st.session_state['authentication_status']:
        if st.button('**Reset Password**', use_container_width=True):
            st.switch_page('pages/5_Reset_Password.py')
with button3:
    if st.session_state['authentication_status']:
        if st.button('**Update Details**', use_container_width=True):
            st.switch_page('pages/6_Update_Details.py')

def GenerateExercises(selected_muscles, number):
    count=0
    exercise_list = pd.DataFrame(columns=['name', 'type', 'description', 'reps']) #empty datafram to hold info on chosen exercises
    while count < number: #while the exercise number limit has not been reached
        rand = random.randrange(0,len(selected_muscles)) #choose a random number from range of selected exercise list length
        if selected_muscles.iloc[rand]['name'] not in exercise_list['name'].tolist(): #if exercise has not already been chosen (no duplicates)
            if (set(exercise_list['type']) == set(selected_muscles['type'])) or (selected_muscles.iloc[rand]['type'] not in set(exercise_list['type'])): #if exercise type is not already chosen or all types have already been chosen
                exercise_list.loc[len(exercise_list)] = selected_muscles.iloc[rand] #add exercise to list
                count = count + 1
    return exercise_list 

guide = 'Choose what muscles you want to hit and the number of exercises you want to do and a random workout will be generated for you. All exercises can be done from your home only using dumbbells.'
st.header('Home Workout Generator', divider='red', anchor=False)
with st.expander('**About App**'):
    st.write(guide)
exercises = pd.read_csv('Data/Exercises.csv') #load exercise file
types = st.multiselect('**Which muscle groups do you want to hit**', options=['Chest', 'Shoulders', 'Arms', 'Back', 'Legs', 'Core']) #request exercise types desired from type list
selected_muscles = exercises[exercises['type'].isin(types)] #filtered exercise list


col1,col2 = st.columns([1,1], vertical_alignment='bottom')
number = col1.number_input(f'**Number Of Exercises | Max: {len(selected_muscles)}**', step=1, min_value=0, max_value=len(selected_muscles)) #request number of exercises that doesn't exceed quantity of avaiable exercises
generate =  col2.button('**Generate**', type='primary', use_container_width=True) #generate exercises button
if generate:
    exercise_list = GenerateExercises(selected_muscles, number) #generate random exercises
    for index, row in exercise_list.iterrows(): #for each exercise chosen
        if row['reps'] == 'AMRAP': #if the reps is AMRAP
            st.markdown(f'<p class="big-font"><b>{row['name']}: 3 sets x {row['reps']}<b></p>',  unsafe_allow_html=True, help='AMRAP = As Many Reps As Possible') #display exercise and sets x reps and explain what AMRAP means
        else:
            st.markdown(f'<p class="big-font"><b>{row['name']}: 3 sets x {row['reps']}<b></p>',  unsafe_allow_html=True) #display exercise and sets x reps
        with st.expander('**DEMO**'): #more demo  and description expander
            st.markdown(row['description']) #show exercise description
            st.video('Data/ExerciseVids/' + row['name'].lower().replace(" ", "") + '.MOV', loop=True, autoplay=False, muted=True) #play demo video