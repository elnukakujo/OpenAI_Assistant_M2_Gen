import pandas as pd
from common import *
import os

def export_ecore():
    df = pd.read_csv('data/input_output_GPT.csv')

    for folder in os.listdir("data/DSL2Gen"):
        output_path = os.path.join(os.path.join("data/generated", folder), 'output.ecore')
        expected_output_path = os.path.join(os.path.join("data/generated", folder), 'solution.ecore')
        write_file(output_path,df["OutputEcore"][df["DSL_Name"]==folder].values[0])
        write_file(expected_output_path,df["Expected_OutputEcore"][df["DSL_Name"]==folder].values[0])