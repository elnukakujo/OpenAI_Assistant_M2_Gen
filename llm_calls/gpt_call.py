from openai import OpenAI
from dotenv import load_dotenv
import json
import os
from conversion import convert_json2nl

def gpt_unique_call(client, prompt, llm_name):
    sys_role = "You are an expert in designing and validating class diagrams from a textual description for domain models returning only valid Json files with only components from the description. Ensure all referenced classes are explicitly defined within the input."
    messages = gpt_prepare_shots_prompt(prompt['prompt_ex'], prompt['user_prompt'], sys_role)
    return client.chat.completions.create(model=llm_name, messages=messages).choices[0].message.content

def gpt_prepare_shots_prompt(shots, prompt, sys_role):
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

def gpt_task_call(client, prompt, divide, llm_name):
    if divide == "auto":
        sys_role = "You are an expert in designing CRUD operation tasks for another LLM to build a metamodel. A metamodel is composed of enumerations and classes. Classes are composed of attributes with types (int, double, boolean, Date, string, and enumerations custom types) and relationships which have multiplicities and can be inherit, associate or contain. You receive a textual description of a problem domain and return a list of 5 very detailed and precise tasks containing CRUD operations in a 1D json array containing only str of what the other LLM should do to create a correct metamodel. Do not talk about CRUD operations in the tasks. The other LLM won't have access to this description so always specify everything to him."
        messages =[{"role": "system", "content": sys_role}]
        messages.append({"role": "user", "content": prompt["user_prompt"]})
        response = client.chat.completions.create(model=llm_name, messages=messages).choices[0].message.content
        try:
            tasks = json.loads(response.strip("```json\n").strip("```"))
        except:
            print(tasks)
            raise Exception("Failed to parse tasks from GPT response")
    elif divide == "manual":
        tasks = prompt["user_prompt"].split('\n\n')
    else:
        raise Exception("Invalid divide method")
    
    response = {}
    sys_role = "You are an expert in designing and validating class diagrams for domain models returning only valid Json files. You receive tasks with the format of CRUD operations as well as a model from previous tasks and return a valid json object using the same format as the shots above. A metamodel is composed of enumerations and classes. Classes are composed of attributes with types (int, double, boolean, Date, string, and enumerations custom types) and relationships which have mul and can be inherit, associate or contain. Return only valid Json files as shown in the shots, and USE THE PREVIOUS METAMODEL AS BASE! USE THE PREVIOUS METAMODEL AS BASE! USE THE PREVIOUS METAMODEL AS BASE!"
    i=0
    for task in tasks:
        print("----------------------")
        print(f"Task {i}: {task}")
        messages = gpt_prepare_shots_prompt(prompt['prompt_ex'], task +"\n Previous metamodel: \n"+json.dumps(response), sys_role)
        response = client.chat.completions.create(model=llm_name, messages=messages).choices[0].message.content
        print(convert_json2nl(response))
        i+=1
    return response, tasks

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
        response, tasks = gpt_task_call(client, prompt, divide, llm_name)
    else:
        response = gpt_unique_call(client, prompt, llm_name)
        tasks = ""
    return response, tasks