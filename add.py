import pandas as pd

exercises = pd.read_csv('Data/Exercises.csv') #load exercise file
exercises.loc[len(exercises.index)] = ['Russian Twist', 'Core', 'Sit on floor, hold your hands together and lean back on butt until feet are hovering. Repeated twist at the waist to bring your hands from side to side. Hold dumbbell to make harder', '30 sec']
exercises.loc[len(exercises.index)] = ['Burpees', 'Legs', 'Start standing, then bend down and put hands on ground and kick feet back to go into plank position. Pull feet back in below torso and jump as high as possible from squatted position. Include pushup at bottom to make harder.', '15']
exercises.to_csv('Data/Exercises.csv', index=False)
print(exercises)