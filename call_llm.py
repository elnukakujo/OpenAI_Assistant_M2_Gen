from common import *
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import os

def save_data(prompt,output, DSL_path, llm_name):
    if os.path.exists(f'{DSL_path}/input_output_GPT.csv'):
        df = pd.read_csv(f'{DSL_path}/input_output_GPT.csv', index_col=0)
        if 'Solution' in df.columns:
            if os.path.exists(f'{DSL_path}/solution.txt'):
                solution = read_file(f'{DSL_path}/solution.txt')
                df = df[['Prompt', 'Output', 'Solution']]
                df.loc[llm_name] = [prompt, output, solution]
            else:
                raise Exception("The solution.txt file is missing.")
        else:
            df= df[['Prompt', 'Output']]
            df.loc[llm_name] = [prompt, output]
    else:
        if os.path.exists(f'{DSL_path}/solution.txt'):
            solution = read_file(f'{DSL_path}/solution.txt')
            df = pd.DataFrame([[prompt, output, solution]], columns=['Prompt', 'Output', 'Solution'], index=[llm_name])
        else:
            df = pd.DataFrame([[prompt, output]], columns=['Prompt', 'Output'], index=[llm_name])
    df.index.name = 'LLM_name'
    df.to_csv(f'{DSL_path}/input_output_GPT.csv', index=True)

def gpt_call(prompt, llm_name):
    load_dotenv()
    sys_role = "You are an expert class diagram design assistant for domain models. Please strictly follow the given ANTLR grammar for this task. Do not add any additional characters, Java code, or unnecessary formatting. Provide only the output that matches the grammar. Additionally, remember that every class you reference must be defined."+read_file("antlrConversion/ClassDiagram.g4")
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(model=llm_name, messages=[
        {"role": "system", "content": sys_role},
        {"role": "user", "content": prompt}
    ])
    return response.choices[0].message.content

def call_llm(prompt, llm_idx, DSL_folder):
    DSL_path = "data/DSL2Gen/"+DSL_folder
    llm_list = ["gpt-3.5-turbo","gpt-4","llama-3.2-3b-instruct"]
    llm_name = llm_list[llm_idx]
    output_M2 = gpt_call(prompt,llm_name)
    save_data(prompt, output_M2, DSL_path , llm_name)