#! /usr/bin/python

# Import modules
import pandas as pd
import os

# Read the experiments
experiments = os.listdir('Data')
# Sort the experiments
experiments.sort()

# Collect the data
date, protein, discription, name, time, area = [], [], [], [], [], []

for experiment in experiments:
    
    # Extract the date of the experiment
    date.append(experiment.split('_')[0])
    
    # Extract the protein name
    protein_ = ''
    for word in experiment.split('_')[1:3]:
        protein_ += word + ' '
    protein.append(protein_[:-1])
    
    # Extract the discription
    discription_ = ''
    for word in experiment.split('_')[3:]:
        discription_ += word + ' '
    discription.append(discription_[:-1].replace('NTA','GUV'))
    
    # Extract the vesicle name
    curves = [x.removesuffix('.csv') for x in os.listdir(f'Data/{experiment}') if '.csv' in x]
    name.append(curves)
    
    # Extract time and area
    for curve in curves:
        # Read the curve data frame
        df_curve = pd.read_csv(f'Data/{experiment}/{curve}.csv')
        # Extract the time component
        time.append(df_curve['Time'].values)
        # Extract the area component
        area.append(df_curve['Area'].values)

# initialize the data frame
df = pd.DataFrame({'Date':date, 'Protein':protein, 'Discription':discription, 'Name':name})
# Explode around the name
df = df.explode('Name').reset_index(drop=True)
# Add the Time and Area columns
df['Time'] = time
df['Area'] = area

# Save the data frame as csv
df.to_pickle('Results/initial_area_curves.pkl')

# Print the data frame
print(df)