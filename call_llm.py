from common import *
from conversion import *
from llm_calls.gpt_call import gpt_call
from llm_calls.gemini_call import gemini_call
import pandas as pd
import numpy as np
import os

def save_data(prompt, output, DSL_path, llm_name, shots, divide, tasks):
    """
    Save the provided data to JSON files and update or create a CSV file with the data.
    Args:
        prompt (dict): The prompt data to be saved.
        output (dict): The output data to be saved.
        DSL_path (str): The directory path where the files will be saved.
        llm_name (str): The name of the language model.
        shots (str): The example method to be used in the prompt preparation corresponding to the explanations passed to the LLM, depends on the dsl_names in the data/Example folder.
        divide (str): The method used to divide the data.
        tasks (list): The list of tasks the model used to generate the output in case divide.
    """
    write_json(f'{DSL_path}/json/prompt.json', prompt)
    write_json(f'{DSL_path}/json/output.json', output)
    
    if shots == "nshot":
        shots == f'{str(len(prompt["prompt_ex"]))}shots'
        
    if isinstance(tasks, list) and all(isinstance(task, str) for task in tasks):
        tasks = "\n\n".join(tasks)
    
    if divide == "":
        divide = np.nan
        tasks = np.nan
        
    if os.path.exists(f'{DSL_path}/json/pre_model.json'):
        pre_model = convert_json2nl(read_json(f'{DSL_path}/json/pre_model.json'))
    else:
        pre_model = ""
    
    prompt = prompt_list2string(prompt)
    output = convert_json2nl(output)
    
    if os.path.exists(f'{DSL_path}/json/solution.json'):
        solution = convert_json2nl(read_json(f'{DSL_path}/json/solution.json'))
    else:
        solution = ""
    
    if os.path.exists(f'{DSL_path}/generated.csv'):
        df = pd.read_csv(f'{DSL_path}/generated.csv', index_col=[0, 1, 2])
        df.index.names = ['LLM_name', 'Shots_example', 'Divide_method']  # Set MultiIndex names

        # Define the new row
        new_row = {
            'Tasks': tasks,
            'Prompt': prompt,
            'Pre_model': pre_model,
            'Output': output,
            'Solution': solution
        }

        df.loc[(llm_name, shots, divide)] = list(new_row.values())

    else:
        data = [[tasks, prompt, pre_model, output, solution]]
        columns = ['Tasks', 'Prompt', 'Pre_model', 'Output', 'Solution']
        
        df = pd.DataFrame(data, columns=columns, index=pd.MultiIndex.from_tuples(
            [(llm_name, shots, divide)],
            names=['LLM_name', 'Shots_example', 'Divide_method']
        ))

    # Save the updated DataFrame
    df.to_csv(f'{DSL_path}/generated.csv', index=True)

def call_llm(prompt, divide, llm_idx, DSL_folder, shots):
    """
    Calls a language model (LLM) based on the provided index and saves the generated data.

    Args:
        prompt (dict): A dictionary containing the prepared example prompt and user prompt.
            - "prompt_ex" [[str,str],...] or None): A 2D array of textual description with their corresponding solution model if shots defined.
            - "user_prompt" (str): The prepared user description prompt.
            - "pre_model" (dict or None): The pre-model json data if available.
        divide (str): A parameter to control the division of tasks.
        llm_idx (int): Index of the LLM to be used. 
                       - 0 : "gpt-3.5-turbo", 
                       - 1 : "gpt-4", 
                       - 2 : "gemini-1.5-flash".
        DSL_folder (str): The folder path where the DSL data will be saved.
        shots (str): The example method to be used in the prompt preparation corresponding to the explanations passed to the LLM, depends on the dsl_names in the data/Example folder.
    
    Raises:
        IndexError: If an invalid llm_idx is provided.
    """
    DSL_path = "data/DSL2Gen/"+DSL_folder
    llm_list = ["gpt-3.5-turbo", "gpt-4", "gemini-1.5-flash"]
    llm_name = llm_list[llm_idx]
    if llm_idx in [0,1]:
        output_M2, tasks = gpt_call(prompt, divide, llm_name)
    elif llm_idx == 2:
        output_M2, tasks = gemini_call(prompt, divide, llm_name)
    else:
        raise IndexError("Invalid llm_idx")
    save_data(prompt, output_M2, DSL_path, llm_name, shots, divide, tasks)