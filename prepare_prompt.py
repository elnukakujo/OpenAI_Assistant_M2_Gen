from common import *
from conversion import convert_json2nl
import os

def prepare_prompt_ex(shots):
    """
    Prepares a list of prompt examples based on the specified shot method.
    Args:
        shots (str): A string specifying the shot method. It can be "nshot" for 
                     including all examples in the directory, or a string in the 
                     format "{n}shot_{example1}_{example2}_..." where {n} is the 
                     number of examples to include and {example1}, {example2}, etc. 
                     are the names of the specific examples.
    Returns:
        list: A list of prompt examples, where each example is a list containing 
              the description text and the solution JSON.
    Raises:
        ValueError: If the number of specified examples does not match {n} or if 
                    an invalid shot method is provided.
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
    return user_domain_description


def prepare_prompt(shots, DSL_folder):
    """
    Prepares a prompt based on the selected type and DSL folder.

    Args:
        shots (str): The shots to prepare. It can be "0shot" for no shot, "nshot" for all examples or a specific number of examples in the format "{n}shot_{example1}_{example2}_...".
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
    user_prompt = prepare_user_prompt(path_domain_description)
    return {
        "prompt_ex": prompt_ex,
        "user_prompt": user_prompt
    }