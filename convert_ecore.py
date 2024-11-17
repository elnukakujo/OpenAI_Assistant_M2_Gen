from common import *
from conversion import convert_json2ecore
import os

def convert_ecore(dsl_name):
    """
    Converts JSON files to Ecore format for a given DSL (Domain-Specific Language).

    This function reads JSON files from a specified directory and converts them to Ecore format.
    It processes two JSON files: 'output.json' and, if it exists, 'solution.json'.

    Args:
        dsl_name (str): The name of the DSL for which the JSON files are to be converted.

    Raises:
        FileNotFoundError: If 'output.json' does not exist in the specified directory.
    """
    json_path=f'data/DSL2Gen/{dsl_name}/json/'

    convert_json2ecore(read_json(json_path+'output.json'), dsl_name, "output")
    if os.path.exists(json_path+'solution.json'):
        convert_json2ecore(read_json(json_path+'solution.json'), dsl_name, "solution")