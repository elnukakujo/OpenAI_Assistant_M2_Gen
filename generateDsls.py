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
        description_path = os.path.join(os.path.join("data/DSL2Gen", folder), 'description.txt')
        solution_path = os.path.join(os.path.join("data/DSL2Gen", folder), 'solution.txt')
        
        description = read_file(description_path)
        solution = read_file(solution_path)
        
        dsl_list.append((folder,description,solution))
    return dsl_list

def get_prompts():
    if not os.path.exists("data/input_output_GPT.csv"):
        example = read_file("data/Example/3shot.txt")
        dsl_list = import_dsls()
        df = pd.DataFrame(dsl_list, columns=['DSL_Name', 'Description', 'Expected_Output'])
        task="Generate the lists of model classes and associations from the following given description."
        df['Prompt'] = example + "\n### \n"+task+"\nDescription: " + df['Description']
        df.to_csv('data/input_output_GPT.csv', index=False)
    else:
        df = pd.read_csv('data/input_output_GPT.csv')
    return df

def save_outputs(df, outputs):
    df["Output"] = outputs
    df=df[['DSL_Name', 'Description', 'Prompt', 'Output', 'Expected_Output']]
    df.to_csv('data/input_output_GPT.csv', index=False)

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

save_outputs(df, outputs)