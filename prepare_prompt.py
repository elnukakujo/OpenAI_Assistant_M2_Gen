from common import *
from conversion import convert_json2nl
import os

def prepare_prompt_ex(shots):
    """
    Prepares a list of prompt examples based on the selected type.
    Args:
        shots (str): The type of examples to prepare. It can be "nshot" for all examples
                             or a specific number of examples in the format "{n}shot_{example1}_{example2}_...".
    Returns:
        list: A list of prompt examples, where each example is a list containing a description (str) and a solution (dict).
    Raises:
        ValueError: If the shots format is invalid or the number of specified examples does not match the expected count.
    """
    examples_path="data/Example"
    prompt_ex = []
    
    if shots == "nshot":
        for example_folder in os.listdir(examples_path):
            example_path = os.path.join(examples_path, example_folder)
            if os.path.isdir(example_path):
                prompt_ex.append([read_txt(f"{example_path}/description.txt"), read_json(f"{example_path}/solution.json")])
        return prompt_ex
    
    elif "shot" in shots:
        n = int(shots.split("shot")[0])
        example_names = shots.split("_")[1:]
        if len(example_names) != n:
            raise ValueError(f"Expected {n} examples, but got {len(example_names)}")
        
        for example_name in example_names:
            example_path = os.path.join(examples_path, example_name)
            if os.path.exists(example_path):
                prompt_ex.append([read_txt(f"{example_path}/description.txt"), read_json(f"{example_path}/solution.json")])
        return prompt_ex
    
    raise ValueError("Invalid shot method selected: Look for typos in the example method name or the dsl names, and conform to the documentation.")


def prepare_user_prompt(divide, folder_path):
    """
    Prepares a user prompt based on the provided folder path.
    This function reads a domain description from a text file and optionally 
    includes a starting model from a JSON file if it exists. It then constructs 
    a prompt for generating model classes and associations based on the description.
    Args:
        divide (str): The divide method to prepare. It can be "" for no divide, "manual" for manual divide, or "auto" for auto divide.
        folder_path (str): The path to the folder containing the description 
                           and optional starting model files.
    Returns:
        str: The constructed prompt for the user.
    """
    user_domain_description=read_txt(f"{folder_path}/description.txt")
    path_start_model = f"{folder_path}/json/pre_model.json"
    
    if divide == "":
        if os.path.exists(path_start_model):
            user_start_model=read_json(path_start_model)
            if user_start_model != "":
                goal = "Task instructions: Using this previous low recall model as a base to work on, add more enumerations, classes, attributes and relationships from the problem description to the metamodel from the following given description. Additionally prioritize inheritance rel and enumerations when possible rather than additional attributes. For example, BigCity inherit City, rather than having a size attribute or an enumeration CitySize with Big medium, and small."
                prompt = "Base model:\n"+convert_json2nl(user_start_model)+"\n"+goal+"\nDescription:\n" + user_domain_description
                return prompt
        
    goal = "Task instructions: Focus on not losing any infos from the description below to generate a metamodel. Additionally prioritize inheritance rel and enumerations when possible rather than additional attributes."
    prompt = goal+"\nDescription:\n\n" + user_domain_description
    return prompt


def prepare_prompt(shots, divide, DSL_folder):
    """
    Prepares a prompt based on the selected type and DSL folder.

    Args:
        shots (str): The shots to prepare. It can be "0shot" for no shot, "nshot" for all examples or a specific number of examples in the format "{n}shot_{example1}_{example2}_...".
        divide (str): The divide method to prepare. It can be "" for no divide, "manual" for manual divide, or "auto" for auto divide.
        DSL_folder (str): The folder containing the DSL data.

    Returns:
        dict: A dictionary containing the prepared example prompt and user prompt.
            - "prompt_ex" (str): The prepared example prompt.
            - "user_prompt" (str): The prepared user prompt.
    """
    path_domain_description = "data/DSL2Gen/"+DSL_folder
    if shots == "0shot":
        prompt_ex = []
    else:
        prompt_ex = prepare_prompt_ex(shots)
    user_prompt = prepare_user_prompt(divide, path_domain_description)
    return {
        "prompt_ex": prompt_ex,
        "user_prompt": user_prompt
    }