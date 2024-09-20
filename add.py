import pandas as pd

exercises = pd.read_csv('Data/Exercises.csv') #load exercise file
exercises = exercises.drop(13,axis=0)
exercises.to_csv('Data/Exercises.csv', index=False)
print(exercises)