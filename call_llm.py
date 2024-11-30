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

def gpt_message(prompt, sys_role):
    """
    Constructs a list of messages formatted for a GPT model conversation.

    Args:
        prompt (dict): A dictionary containing the following keys:
            - "prompt_ex" (list): A list of tuples where each tuple contains a user message and the corresponding assistant response.
            - "user_prompt" (str): The final user prompt to be added to the messages.
        sys_role (str): The system role message to be included at the beginning of the conversation.

    Returns:
        list: A list of dictionaries, each representing a message in the conversation. The list starts with the system role message,
              followed by alternating user and assistant messages from the "prompt_ex" list, and ends with the final user prompt.
    """
    messages =[{"role": "system", "content": sys_role}]
    for shot in prompt["prompt_ex"]:
        messages.append({"role": "user", "content": shot[0]})
        messages.append({"role": "assistant", "content": json.dumps(shot[1])})
    messages.append({"role": "user", "content": prompt["user_prompt"]})
    return messages

def gpt_call(prompt, llm_name, sys_role):
    """
    Makes a call to the GPT model using the OpenAI API.

    Args:
        prompt (str): The input prompt to be sent to the GPT model.
        llm_name (str): The name of the language model to be used.
        sys_role (str): The system role to be used in the GPT message.

    Returns:
        str: The content of the response message from the GPT model.
    """
    load_dotenv()
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(model=llm_name, messages=gpt_message(prompt, sys_role))
    return response.choices[0].message.content

def call_llm(prompt, llm_idx, DSL_folder):
    """
    Calls a specified language model (LLM) with a given prompt and saves the output.

    Args:
        prompt (str): The input prompt to be sent to the LLM.
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
    sys_role = "You are an expert in designing and validating class diagrams from a textual description for domain models returning only valid Json files with only components from the description. RETURN A JSON, RETURN A JSON, RETURN A JSON. FOLLOW THE EXAMPLES AND RETURN A JSON. Ensure all referenced classes are explicitly defined within the input."
    output_M2 = gpt_call(prompt,llm_name, sys_role)
    save_data(prompt, output_M2, DSL_path , llm_name)