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
with col1:
    number = st.number_input(f'**Number Of Exercises | Max: {len(selected_muscles)}**', step=1, min_value=0, max_value=len(selected_muscles)) #request number of exercises that doesn't exceed quantity of avaiable exercises
with col2:
    generate =  st.button('**Generate**', type='primary', use_container_width=True) #generate exercises button
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