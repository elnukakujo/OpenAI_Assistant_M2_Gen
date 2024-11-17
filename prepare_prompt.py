from common import *
from conversion import convert_json2nl
import os

def prepare_prompt_ex(selected_type):
    """
    Prepares a list of prompt examples based on the selected type.
    Args:
        selected_type (str): The type of examples to prepare. It can be "nshot" for all examples
                             or a specific number of examples in the format "{n}shot_{example1}_{example2}_...".
    Returns:
        list: A list of prompt examples, where each example is a list containing a description (str) and a solution (dict).
    Raises:
        ValueError: If the selected_type format is invalid or the number of specified examples does not match the expected count.
    """
    examples_path="data/Example"
    prompt_ex = []
    
    if selected_type == "nshot":
        for example_folder in os.listdir(examples_path):
            example_path = os.path.join(examples_path, example_folder)
            if os.path.isdir(example_path):
                prompt_ex.append([read_txt(f"{example_path}/description.txt"), read_json(f"{example_path}/solution.json")])
        return prompt_ex
    
    elif "shot" in selected_type:
        n = int(selected_type.split("shot")[0])
        example_names = selected_type.split("_")[1:]
        if len(example_names) != n:
            raise ValueError(f"Expected {n} examples, but got {len(example_names)}")
        
        for example_name in example_names:
            example_path = os.path.join(examples_path, example_name)
            if os.path.exists(example_path):
                prompt_ex.append([read_txt(f"{example_path}/description.txt"), read_json(f"{example_path}/solution.json")])
        return prompt_ex
    
    raise ValueError("Invalid example method selected: Look for typos in the example method name or the dsl names, and conform to the documentation.")


def prepare_user_prompt(folder_path):
    """
    Prepares a user prompt based on the provided folder path.
    This function reads a domain description from a text file and optionally 
    includes a starting model from a JSON file if it exists. It then constructs 
    a prompt for generating model classes and associations based on the description.
    Args:
        folder_path (str): The path to the folder containing the description 
                           and optional starting model files.
    Returns:
        str: The constructed prompt for the user.
    """
    user_domain_description=read_txt(f"{folder_path}/description.txt")
    path_start_model = f"{folder_path}/json/pre_model.json"
    
    if os.path.exists(path_start_model):
        user_start_model=read_json(path_start_model)
        if user_start_model != "":
            task = "Task instructions: Using the previous model as a base, generate the lists of model classes and associations from the following given description."
            prompt = "Base model:\n"+convert_json2nl(user_start_model)+"\n"+task+"\nDescription:\n" + user_domain_description
            return prompt
        
    task = "Task instructions: Generate the lists of model classes and associations from the following given description."
    prompt = task+"\nDescription:\n" + user_domain_description
    return prompt


def prepare_prompt(selected_type, DSL_folder):
    """
    Prepares a prompt based on the selected type and DSL folder.

    Args:
        selected_type (str): The type of prompt to prepare.
        DSL_folder (str): The folder containing the DSL data.

    Returns:
        dict: A dictionary containing the prepared example prompt and user prompt.
            - "prompt_ex" (str): The prepared example prompt.
            - "user_prompt" (str): The prepared user prompt.
    """
    path_domain_description = "data/DSL2Gen/"+DSL_folder
    prompt_ex = prepare_prompt_ex(selected_type)
    user_prompt = prepare_user_prompt(path_domain_description)
    return {
        "prompt_ex": prompt_ex,
        "user_prompt": user_prompt
    }