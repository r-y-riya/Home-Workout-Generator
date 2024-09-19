import streamlit as st
import pandas as pd
import random

def GenerateExercises(selected_exercises, number):
    count=0
    exercise_list = []
    while count < number:
        rand = random.randrange(0,len(selected_exercises)) #choose a random number from range of selected exercise list length
        exercise_list.append(selected_exercises.iloc[rand])
        count = count + 1
    return exercise_list

exercises = pd.read_csv('Data/Exercises.csv') #load exercise file
types = st.multiselect('Which muscle groups do you want to hit', options=['Chest', 'Shoulders', 'Arms', 'Back', 'Legs', 'Core'])
selected_exercises = exercises[exercises['type'].isin(types)] #filtered exercise list
number = st.number_input("Number Of Exercises", step=1, min_value=0, max_value=len(selected_exercises))

if st.button('Generate'):
    exercise_list = GenerateExercises(selected_exercises, number)
    for x in exercise_list:
        st.write(x)
        st.video('Data/ExerciseVids/' + x['name'].lower().replace(" ", "") + '.MOV', loop=True, autoplay=True, muted=True)