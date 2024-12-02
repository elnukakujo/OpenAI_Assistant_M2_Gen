from common import *
from conversion import *
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import os
import json

def save_data(prompt, output, DSL_path, llm_name):
    """
    Save the prompt and output data to JSON and CSV files.
    This function saves the provided prompt and output data to JSON files and updates a CSV file with the data.
    If a solution JSON file exists, it also includes the solution in the CSV file.
    Args:
        prompt (list): The prompt data to be saved.
        output (dict): The output data to be saved.
        DSL_path (str): The directory path where the JSON and CSV files are stored.
        llm_name (str): The name of the language model, used as an index in the CSV file.
    """
    write_json(f'{DSL_path}/json/prompt.json', prompt)
    write_json(f'{DSL_path}/json/output.json', output)
    prompt = prompt_list2string(prompt)
    output = convert_json2nl(output)
    if os.path.exists(f'{DSL_path}/input_output_GPT.csv'):
        df = pd.read_csv(f'{DSL_path}/input_output_GPT.csv', index_col=0)
        if 'Solution' in df.columns and os.path.exists(f'{DSL_path}/json/solution.json'): 
            solution = convert_json2nl(read_json(f'{DSL_path}/json/solution.json'))
            df = df[['Prompt', 'Output', 'Solution']]
            df.loc[llm_name] = [prompt, output, solution]
            
        elif 'Solution' in df.columns and not os.path.exists(f'{DSL_path}/json/solution.json'):
            df = df[['Prompt', 'Output', 'Solution']]
            df.loc[llm_name] = [prompt, output, ""]
            
        else:
            df = df[['Prompt', 'Output']]
            df.loc[llm_name] = [prompt, output]
    else:
        if os.path.exists(f'{DSL_path}/json/solution.json'):
            solution = convert_json2nl(read_json(f'{DSL_path}/json/solution.json'))
            df = pd.DataFrame([[prompt, output, solution]], columns=['Prompt', 'Output', 'Solution'], index=[llm_name])
        else:
            df = pd.DataFrame([[prompt, output]], columns=['Prompt', 'Output'], index=[llm_name])
    df.index.name = 'LLM_name'
    df.to_csv(f'{DSL_path}/input_output_GPT.csv', index=True)

def gpt_shot_prompt_messages(shots, prompt, sys_role):
    """
    Constructs a list of messages for a GPT model based on provided shots, prompt, and system role.

    Args:
        shots (list of tuples): A list of tuples where each tuple contains a user input and the corresponding assistant response.
        prompt (str): The main prompt to be sent to the GPT model.
        sys_role (str): The role of the system to be included in the messages.

    Returns:
        list: A list of dictionaries representing the messages to be sent to the GPT model.
    """
    messages =[{"role": "system", "content": sys_role}]
    if len(shots)>0:
        for shot in shots:
            messages.append({"role": "user", "content": shot[0]})
            messages.append({"role": "assistant", "content": json.dumps(shot[1])})
    messages.append({"role": "user", "content": prompt})
    return messages

def gpt_taskgen_messages(client, llm_name, prompt):
    messages =[{"role": "system", "content": "From a textual description, you generate a list of tasks, in a json array of str format, for another LLM to build a metamodel. Don't give general instructions and instructions an LLM can't follow like build a metamodel, or create a class diagram."}]
    messages.append({"role": "user", "content": prompt})
    return client.chat.completions.create(model=llm_name, messages=messages).choices[0].message.content

def gpt_tasks(client, prompt, divide, llm_name):
    if divide == "manual":
        goal = prompt["user_prompt"].split('\n\n')[0]
        tasks = prompt["user_prompt"].split('\n\n')[1:]
    elif divide == "auto":
        goal = prompt["user_prompt"].split('\n\n')[0]
        tasks = gpt_taskgen_messages(client, llm_name, '.\n'.join(prompt["user_prompt"].split('\n\n')[1:]))
        try:
            tasks = json.loads(tasks.strip("```json\n").strip("```"))
        except:
            print(tasks)
            raise Exception("Failed to parse tasks from GPT response")
    else:
        raise Exception("Invalid divide method")
    i=0
    for task in tasks:
        print(f"Task {i}: {task}")
        sys_role = "You are an expert in designing and validating class diagrams for domain models returning only valid Json files. You follow a set of instruction that you receive one by one to build a metamodel in a systematic way."
        messages = gpt_shot_prompt_messages(prompt['prompt_ex'], goal+'\n'+task, sys_role)
        response = client.chat.completions.create(model=llm_name, messages=messages)
        goal = 'Using this previous model, add more elements to the model or modify the model using this text problem description. ' + json.dumps(response.choices[0].message.content)
        i+=1
    return response

def gpt_call(prompt, divide, llm_name):
    """
    Makes a call to the GPT model using the OpenAI API.

    Args:
        prompt (str): The input prompt to be sent to the GPT model.
        divide (str): The divide method to prepare. It can be "" for no divide, "manual" for manual divide, or "auto" for auto divide.
        llm_name (str): The name of the language model to be used.

    Returns:
        str: The content of the response message from the GPT model.
    """
    load_dotenv()
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    if divide != "":
        response = gpt_tasks(client, prompt, divide, llm_name)
    else:
        sys_role = "You are an expert in designing and validating class diagrams from a textual description for domain models returning only valid Json files with only components from the description. Ensure all referenced classes are explicitly defined within the input."
        messages = gpt_shot_prompt_messages(prompt['prompt_ex'], prompt['user_prompt'], sys_role)
        response = client.chat.completions.create(model=llm_name, messages=messages)
    return response.choices[0].message.content

def call_llm(prompt, divide, llm_idx, DSL_folder):
    """
    Calls a specified language model (LLM) with a given prompt and saves the output.

    Args:
        prompt (str): The input prompt to be sent to the LLM.
        divide (str): The divide method to prepare. It can be "" for no divide, "manual" for manual divide, or "auto" for auto divide.
        llm_idx (int): The index of the LLM to be used from the predefined list.
        DSL_folder (str): The folder path where the output data will be saved.

    Returns:
        None

    Raises:
        IndexError: If llm_idx is out of the range of the llm_list.
        Exception: If there is an error in calling the LLM or saving the data.

    Notes:
        The function supports different LLMs including "gpt-3.5-turbo", "gpt-4",
        and "Llama2-7B-chat". Depending on the LLM selected, 
        it calls either `llama_call` or `gpt_call` with appropriate parameters.
    """
    DSL_path = "data/DSL2Gen/"+DSL_folder
    llm_list = ["gpt-3.5-turbo","gpt-4"]
    llm_name = llm_list[llm_idx]
    output_M2 = gpt_call(prompt, divide, llm_name)
    save_data(prompt, output_M2, DSL_path , llm_name)