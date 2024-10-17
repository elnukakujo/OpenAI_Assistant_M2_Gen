from openai import OpenAI
from dotenv import load_dotenv
import os

def read_file(path):
    file = open(path, "r")
    content = file.read()
    file.close()
    return content 

def write_file(path, content):
    file = open(path, "w")
    file.write(content)
    file.close()
    return True

def get_prompt(dslName: str):
    example = read_file("../data/Example/3shot.txt")
    dslDesc = read_file("../data/DSL2Gen/" + dslName + "/description.txt")
    prompt = example + "\n### \nGenerate the lists of model classes and associations from the following given description.\nDescription: " + dslDesc
    write_file("prompt.txt", prompt)
    return prompt

prompt = get_prompt("HBMS")

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
response = client.chat.completions.create(model="gpt-4", messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
])

response = response.choices[0].message.content
if write_file("output.txt", response):
    print("Output written to output.txt")
else:
    print("Error writing output")