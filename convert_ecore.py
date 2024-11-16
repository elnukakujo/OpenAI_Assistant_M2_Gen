import pandas as pd
from common import *
from conversion import convert_json2ecore
import os

def convert_ecore(dsl_name):
    json_path=f'data/DSL2Gen/{dsl_name}/json/'
        
    csv_path=f'data/DSL2Gen/{dsl_name}/input_output_GPT.csv'
    df = pd.read_csv(csv_path)
            
    df.at[dsl_name, 'OutputEcore'] = convert_json2ecore(read_json(json_path+'output.json'), dsl_name, "output")
    if 'Solution' in df.columns:
        df.at[dsl_name, 'SolutionEcore'] = convert_json2ecore(read_json(json_path+'solution.json'), dsl_name, "solution")

    # Save the updated dataframe to a new CSV file
    df.to_csv(csv_path, index=False)