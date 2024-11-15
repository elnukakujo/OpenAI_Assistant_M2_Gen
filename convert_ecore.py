import pandas as pd
from common import *
from antlrConversion.conversion import conversion

def convert_ecore(dsl_name):
    csv_path=f'data/DSL2Gen/{dsl_name}/input_output_GPT.csv'
    df = pd.read_csv(csv_path)
            
    df['OutputEcore'] = df['Output'].apply(conversion)
    df['SolutionEcore'] = df['Solution'].apply(conversion)

    # Save the updated dataframe to a new CSV file
    df.to_csv(csv_path, index=False)