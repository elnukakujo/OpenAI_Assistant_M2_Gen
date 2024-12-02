import os
import json
from dotenv import load_dotenv 
from conversion import *

import google.generativeai as genai
import typing_extensions as typing

def gemini_generate(model, message):
    return model.generate_content(
        message,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json"
        )
    )

def gemini_prepare_shots_prompt(shots, sys_role):
    message = ""
    if len(shots) > 0:
        for shot in shots:
            description = shot[0]
            solution = shot[1]
            
            message += f"**Prompt**: {sys_role}\n"
            message += f"* Textual Description: {description}\n"
            message += f"* Metamodel: {solution}\n\n"
    return message

def gemini_unique_call(model, prompt):
    sys_role = "You are an expert in designing and validating class diagrams for domain models returning only valid Json files. You receive textual description of a problem domain and return a valid json object using the same format as the shots."
    if len(prompt["prompt_ex"]) > 0:
        message = gemini_prepare_shots_prompt(prompt["prompt_ex"], sys_role)
    else:
        message = ""
    message += f"**Prompt**: {sys_role}\n"
    message += f"* Textual Description: {prompt['user_prompt']}\n"
    response = gemini_generate(model, message)
    return response.text

def gemini_task_call(model, prompt, divide):
    if divide == "auto":
        sys_role = "You are an expert in designing CRUD operation tasks for another LLM to build a metamodel. A metamodel is composed of enumerations and classes. Classes are composed of attributes with types (int, double, boolean, Date, string, and enumerations custom types) and relationships which have multiplicities and can be inherit, associate or contain. You receive a textual description of a problem domain and return a list of 10 CRUD operation very detailed and precise tasks in a 1D json array containing only str of what the other LLM should do to create a correct metamodel. Do not talk about CRUD operations in the tasks. The other LLM won't have access to this description so always specify everything to him."
        message = f"**Prompt**: {sys_role}\n"
        message += f"* Textual Description: {prompt['user_prompt']}\n"
        response = gemini_generate(model, message)
        tasks = json.loads(response.text)
    elif divide == "manual":
        tasks = prompt["user_prompt"].split('\n\n')
    else:
        raise Exception("Invalid divide method")

    sys_role = "You are an expert in designing and validating class diagrams for domain models returning only valid Json files. You receive tasks with the format of CRUD operations as well as a model from previous tasks and return a valid json object using the same format as the shots above. A metamodel is composed of enumerations and classes. Classes are composed of attributes with types (int, double, boolean, Date, string, and enumerations custom types) and relationships which have multiplicities and can be inherit, associate or contain."
    
    message = gemini_prepare_shots_prompt(prompt["prompt_ex"], sys_role)
    response = {}
    i=0
    for task in tasks:
        print("----------------------")
        print(f"Task {i}: {task}")
        message += f"**Prompt**: {sys_role}\n"
        message += f"* Task: {task}\n"
        message += f"* Previous Metamodel: {json.dumps(response)}\n"
        response = gemini_generate(model, message).text
        print(convert_json2nl(response))
        i+=1
    return response

def gemini_call(prompt, divide, llm_name):
    load_dotenv()
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel(llm_name)
    if divide != "":
        response = gemini_task_call(model, prompt, divide)
    else:
        response = gemini_unique_call(model, prompt)
    return response