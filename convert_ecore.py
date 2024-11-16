import pandas as pd
from common import *
from conversion import convert_json2ecore
import os

def convert_ecore(dsl_name):
    json_path=f'data/DSL2Gen/{dsl_name}/json/'
            
    convert_json2ecore(read_json(json_path+'output.json'), dsl_name, "output")
    if os.path.exists(json_path+'solution.json'):
        convert_json2ecore(read_json(json_path+'solution.json'), dsl_name, "solution")