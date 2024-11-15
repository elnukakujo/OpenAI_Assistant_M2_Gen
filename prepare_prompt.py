from common import *
import os

def prepare_prompt_ex(selected_type):
    return read_file(f"data/Example/{selected_type}.txt")

def prepare_user_prompt(folder_path):
    user_domain_description=read_file(f"{folder_path}/description.txt")
    path_start_model = f"{folder_path}/pre_model.txt"
    if os.path.exists(path_start_model):
        user_start_model=read_file(path_start_model)
        if user_start_model != "":
            task = "Task instructions: Using the previous model as a base, generate the lists of model classes and associations from the following given description."
            prompt = "Base model:\n"+user_start_model+"\n"+task+"\nDescription:\n" + user_domain_description
            return prompt
    task = "Task instructions: Generate the lists of model classes and associations from the following given description."
    prompt = task+"\nDescription:\n" + user_domain_description
    return prompt

def prepare_prompt(selected_type, DSL_folder):
    path_domain_description = "data/DSL2Gen/"+DSL_folder
    prompt_ex = prepare_prompt_ex(selected_type)
    user_prompt = prepare_user_prompt(path_domain_description)
    return prompt_ex+"\n### \n"+user_prompt