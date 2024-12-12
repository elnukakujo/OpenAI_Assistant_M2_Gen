import os
import json
from dotenv import load_dotenv 
from conversion import *
import numpy as np

import google.generativeai as genai

def gemini_generate(model, message):
    """
    Generates content using the provided model and message.

    Args:
        model: The model instance used for generating content.
        message: The input message to be processed by the model.

    Returns:
        The generated content in JSON format.
    """
    return model.generate_content(
        message,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json"
        )
    )

def gemini_prepare_shots_prompt(shots, sys_role):
    """
    Prepares a formatted prompt message based on the provided shots and system role.
    Args:
        shots (list of list of str): A list of list of str where each tuple contains a description and a solution.
        sys_role (str): The role of the system to be included in the prompt.
    Returns:
        str: A formatted string containing the prompt message with descriptions and solutions.
    """
    message = ""
    if shots is not None:
        for shot in shots:
            description = shot[0]
            solution = shot[1]
            
            message += f"**Prompt**: {sys_role}\n"
            message += f"* Textual Description: {description}\n"
            message += f"* Model: {solution}\n\n"
    return message

def gemini_unique_call(model, prompt):
    """
    Generates a response from the Gemini model without division in tasks of the textual description.

    Args:
        model: The model to be used for generating the response.
        prompt (dict): A dictionary containing the following keys:
            - "prompt_ex" (list): A list of example prompts.
            - "user_prompt" (str): The textual description of the problem domain.

    Returns:
        str: The text response generated by the Gemini model.
    """
    model_explanation = "A model is composed of enumerations and classes. Classes are either abstract or not abstract, and are composed of attributes with non complex types (int, double, boolean, Date, string, and enumerations custom types) and relationships which have multiplicities and can be inherit, associate or contain. However, models don't have methods."
    sys_role = f"You are an expert in designing and validating class diagrams for domain models returning only valid Json files. {model_explanation} You receive textual description of a problem domain and return a valid json object using the same format as the example before."
    message = gemini_prepare_shots_prompt(prompt["prompt_ex"], sys_role)
    if prompt["pre_model"] is not None:
        sys_role += f"\n To build this model, you build on top of the following partial solution model. Use wisely the defined abstract classes."
    message += f"**Prompt**: {sys_role}\n"
    message += f"* Textual Description: {prompt['user_prompt']}\n"
    if prompt["pre_model"] is not None:
        message += f"* Previous Model: {json.dumps(prompt['pre_model'])}\n"
    response = gemini_generate(model, message)
    return response.text

def gemini_task_call(model, prompt, divide):
    """
    Generates and processes tasks for creating a Model based on a given textual problem description.
    Args:
        model: The model used to generate responses.
        prompt (dict): A dictionary containing the user prompt and example prompts.
            - 'user_prompt' (str): The textual description of the problem domain.
            - 'prompt_ex' (str): Example prompts for preparing the shots.
        divide (str): The method to divide tasks, either "auto" or "manual".
    Returns:
        tuple: A tuple containing:
            - response (str): The final response generated after processing all tasks.
            - tasks (list): A list of tasks generated from the prompt.
    Raises:
        Exception: If the divide method is invalid.
    """
    model_explanation = "A model is composed of enumerations and classes. Classes are either abstract or not abstract, and are composed of attributes with non complex types (int, double, boolean, Date, string, and enumerations custom types) and relationships which have multiplicities and can be inherit, associate or contain. However, models don't have methods."
    if divide == "auto":
        sys_role = f"You are an expert in designing CRUD operation tasks for another LLM to build a Model. {model_explanation} You receive a textual description of a problem domain and return a list of 10 CRUD operation very detailed and precise tasks in a list containing only str of what the other LLM should do to create a Model corresponding to the description. Do not talk about CRUD operations in the tasks. The other LLM won't have access to this description so always specify everything to him."
        
        if prompt["pre_model"] is not None:
            sys_role += f"\n To design those tasks, you build on top of the following partial solution model. Use wisely the defined abstract classes."
        message = f"**Prompt**: {sys_role}\n"
        message += f"* Textual Description: {prompt['user_prompt']}\n"
        if prompt["pre_model"] is not None:
            message += f"* Previous Model: {json.dumps(prompt['pre_model'])}\n"

        response = gemini_generate(model, message)
        if type(json.loads(response.text)) == dict:
            tasks = np.array(list(json.loads(response.text).values())).flatten().tolist()
        else:
            tasks = json.loads(response.text)
    elif divide == "manual":
        tasks = prompt["user_prompt"].split('\n\n')
    else:
        raise Exception("Invalid divide method")

    sys_role = f"You are an expert in designing and validating domain models returning only valid Json files. You receive tasks with the format of CRUD operations as well as a model from previous tasks and return a valid json object using the same format as the shots above. {model_explanation}"
    
    message = gemini_prepare_shots_prompt(prompt["prompt_ex"], sys_role)
    if prompt["pre_model"] is not None:
        sys_role += f"\n To build this model, you build on top of the following partial solution model. Use wisely the defined abstract classes."
        response = prompt["pre_model"]
    else:
        response = {}
    i=0
    for task in tasks:
        print("----------------------")
        print(f"Task {i}: {task}")
        message += f"**Prompt**: {sys_role}\n"
        message += f"* Task: {task}\n"
        message += f"* Previous Model: {json.dumps(response)}\n"
        response = gemini_generate(model, message).text
        print(convert_json2nl(response))
        i+=1
    return response, tasks

def gemini_call(prompt, divide, llm_name):
    """
    Makes a call to the Gemini API using the provided prompt and model name.

    Args:
        prompt (dict): A dictionary containing the following keys:
            - "prompt_ex" (list or None): A list of example prompts with description and solution if available.
            - "user_prompt" (str): The textual description of the problem domain.
            - "pre_model" (dict or None): The pre_model json data if available.
        divide (str): A string indicating whether to divide the task. If not empty, the task will be divided.
        llm_name (str): The name of the language model to be used.

    Returns:
        tuple: A tuple containing the response from the Gemini API and tasks if divide is not empty, otherwise an empty string for tasks.
    """
    load_dotenv()
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel(llm_name)
    if divide != "":
        response, tasks = gemini_task_call(model, prompt, divide)
    else:
        response = gemini_unique_call(model, prompt)
        tasks = ""
    return response, tasks