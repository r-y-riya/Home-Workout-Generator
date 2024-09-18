import streamlit as st
import pandas as pd
import random

def GenerateExercises(selected_exercises, number):
    count=0
    while count < number:
        rand = random.randrange(0,len(selected_exercises)) #choose a random number from range of selected exercise list length
        st.write(selected_exercises.iloc[rand])
        count = count + 1

exercises = pd.read_csv('Data/Exercises.csv') #load exercise file
types = st.multiselect('Which muscle groups do you want to hit', options=['Chest', 'Shoulders', 'Arms', 'Back', 'Legs', 'Core'])
selected_exercises = exercises[exercises['type'].isin(types)] #filtered exercise list
number = st.number_input("Number Of Exercises", step=1, min_value=0, max_value=len(selected_exercises))

if st.button('Generate'):
    GenerateExercises(selected_exercises, number)



