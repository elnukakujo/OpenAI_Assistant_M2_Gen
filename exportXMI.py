import pandas as pd
from common import *
import os

df = pd.read_csv('data/input_output_GPT.csv')

for folder in os.listdir("data/DSL2Gen"):
    output_path = os.path.join(os.path.join("data/DSL2Gen", folder), 'output.xmi')
    expected_output_path = os.path.join(os.path.join("data/DSL2Gen", folder), 'solution.xmi')
    write_file(output_path,df["OutputXMI"][df["DSL_Name"]==folder].values[0])
    write_file(expected_output_path,df["Expected_OutputXMI"][df["DSL_Name"]==folder].values[0])