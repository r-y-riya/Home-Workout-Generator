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

def GenerateExercises(selected_exercises, number):
    count=0
    exercise_list = pd.DataFrame(columns=['name', 'type', 'description', 'reps'])
    while count < number:
        rand = random.randrange(0,len(selected_exercises)) #choose a random number from range of selected exercise list length
        if selected_exercises.iloc[rand]['name'] not in exercise_list['name'].tolist():
            exercise_list.loc[len(exercise_list)] = selected_exercises.iloc[rand]
            count = count + 1
    return exercise_list 

guide = 'Choose what muscles you want to hit and the number of exercises you want to do and a random workout will be generated for you. It is recommened to do 3 sets for each exercise but that, along with the recommended reps should be whatever you are comfortable with.'
st.header('Random Workout Generator', divider='red', anchor=False, help=guide)
exercises = pd.read_csv('Data/Exercises.csv') #load exercise file
types = st.multiselect('**Which muscle groups do you want to hit**', options=['Chest', 'Shoulders', 'Arms', 'Back', 'Legs', 'Core'])
selected_exercises = exercises[exercises['type'].isin(types)] #filtered exercise list
number = st.number_input("**Number Of Exercises**", step=1, min_value=0, max_value=len(selected_exercises))

if st.button('**Generate**', type='primary'):
    exercise_list = GenerateExercises(selected_exercises, number)
    for index, row in exercise_list.iterrows():
        st.write(f'**{row['name']}**')
        st.write(f'**Muscle Group: {row['type']}**')
        st.write(f'**Reps: {row['reps']}**')
        with st.expander('description'):
            st.markdown(row['description'])
            st.video('Data/ExerciseVids/' + row['name'].lower().replace(" ", "") + '.MOV', loop=True, autoplay=True, muted=True)