import os
import json

def read_txt(path):
    file = open(path, "r")
    content = file.read()
    file.close()
    return content

def write_txt(path,content):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    file = open(path, "w")
    content = file.write(content)
    file.close()
    return True

def read_json(path):
    file = open(path, "r")
    content = json.load(file)
    file.close()
    return content

def write_json(path, content):
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