import streamlit as st
import pandas as pd
import random
import base64

st.markdown(
         f"""
         <style>
         .stApp {{
             border: 3px solid black;
             border-top: 63px solid black;
             background: url(data:image/{'jpg'};base64,{base64.b64encode(open('Data/background.jpg', "rb").read()).decode()});
             background-size: cover

         }}
         </style>
         """,
         unsafe_allow_html=True
     )

def GenerateExercises(selected_muscles, number):
    count=0
    exercise_list = pd.DataFrame(columns=['name', 'type', 'description', 'reps'])
    while count < number:
        rand = random.randrange(0,len(selected_muscles)) #choose a random number from range of selected exercise list length
        if selected_muscles.iloc[rand]['name'] not in exercise_list['name'].tolist():
            if (set(exercise_list['type']) == set(selected_muscles['type'])) or (selected_muscles.iloc[rand]['type'] not in set(exercise_list['type'])):
                exercise_list.loc[len(exercise_list)] = selected_muscles.iloc[rand]
                count = count + 1
    return exercise_list 

guide = 'Choose what muscles you want to hit and the number of exercises you want to do and a random workout will be generated for you. It is recommened to do 3 sets for each exercise but that, along with the recommended reps should be whatever you are comfortable with.'
st.header('At-Home Workout Generator', divider='red', anchor=False, help=guide)
exercises = pd.read_csv('Data/Exercises.csv') #load exercise file
types = st.multiselect('**Which muscle groups do you want to hit**', options=['Chest', 'Shoulders', 'Arms', 'Back', 'Legs', 'Core'])
selected_muscles = exercises[exercises['type'].isin(types)] #filtered exercise list
number = st.number_input("**Number Of Exercises**", step=1, min_value=0, max_value=len(selected_muscles))

if st.button('**Generate**', type='primary'):
    exercise_list = GenerateExercises(selected_muscles, number)
    for index, row in exercise_list.iterrows():
        st.subheader(f'**{row['name']} : 3 sets x {row['reps']}**', anchor=False)
        with st.expander('**DEMO**'):
            st.markdown(row['description'])
            st.video('Data/ExerciseVids/' + row['name'].lower().replace(" ", "") + '.MOV', loop=True, autoplay=True, muted=True)