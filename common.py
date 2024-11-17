import os
import json

def read_txt(path):
    """
    Reads the content of a text file and returns it as a string.

    Args:
        path (str): The path to the text file.

    Returns:
        str: The content of the text file.
    """
    file = open(path, "r")
    content = file.read()
    file.close()
    return content

def write_txt(path, content):
    """
    Writes the given content to a text file at the specified path. If the directory
    does not exist, it will be created.

    Args:
        path (str): The file path where the content should be written.
        content (str): The content to write to the file.

    Returns:
        bool: True if the file was written successfully.
    """
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    file = open(path, "w")
    content = file.write(content)
    file.close()
    return True

def read_json(path):
    """
    Reads a JSON file from the specified path and returns its content.

    Args:
        path (str): The file path to the JSON file.

    Returns:
        dict: The content of the JSON file as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not a valid JSON.
    """
    file = open(path, "r")
    content = json.load(file)
    file.close()
    return content

def write_json(path, content):
    """
    Writes the given content to a JSON file at the specified path.

    Args:
        path (str): The file path where the JSON content will be written.
        content (str or dict): The content to write to the JSON file. It can be a JSON string or a dictionary.

    Raises:
        Exception: If the content is a string and it is not a valid JSON string.

    Returns:
        bool: True if the content was successfully written to the file.
    """
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except json.JSONDecodeError:
            raise Exception("The content to save is not a valid JSON string.")
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path, "w") as file:
        json.dump(content, file, indent=4)
    return True