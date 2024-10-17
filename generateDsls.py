from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd

def read_file(path):
    file = open(path, "r")
    content = file.read()
    file.close()
    return content

def import_dsls():
    dsl_list = []
    for folder in os.listdir("data/DSL2Gen"):
        file_path = os.path.join(os.path.join("data/DSL2Gen", folder), 'description.txt')
        content = read_file(file_path)
        dsl_list.append((folder,content.strip()))
    return dsl_list

def get_prompts():
    if not os.path.exists("data/input_output_GPT.csv"):
        example = read_file("data/Example/3shot.txt")
        dsl_list = import_dsls()
        df = pd.DataFrame(dsl_list, columns=['DSL_Name', 'Description'])
        df['Prompt'] = example + "\n### \nGenerate the lists of model classes and associations from the following given description.\nDescription: " + df['Description']
        df.to_csv('data/input_output_GPT.csv', index=False)
    else:
        df = pd.read_csv('data/input_output_GPT.csv')
    return df

df = get_prompts()

outputs = []
for prompt in df.Prompt:
    load_dotenv()
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(model="gpt-4", messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ])

    response = response.choices[0].message.content
    outputs.append(response)

df["Output"] = outputs
df.to_csv('data/input_output_GPT.csv', index=False)