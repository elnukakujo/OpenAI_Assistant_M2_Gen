from common import *
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
from api_calls.llama_call import llama_call
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

def gpt_call(prompt, llm_name, sys_role):
    load_dotenv()
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(model=llm_name, messages=[
        {"role": "system", "content": sys_role},
        {"role": "user", "content": prompt}
    ])
    return response.choices[0].message.content

def call_llm(prompt, llm_idx, DSL_folder):
    DSL_path = "data/DSL2Gen/"+DSL_folder
    llm_list = ["gpt-3.5-turbo","gpt-4","Llama3.2-3B-Instruct", "Llama3.2-3B"]
    llm_name = llm_list[llm_idx]
    sys_role = "You are an expert in designing and validating class diagrams for domain models. Follow the provided ANTLR grammar strictly, ensuring output adheres precisely to its structure. Do not add Java code, extraneous characters, or unnecessary formatting. Ensure all referenced classes are explicitly defined within the input."+read_file("antlrConversion/ClassDiagram.g4")
    if llm_idx == 2 or llm_idx==3:
        output_M2 = llama_call(sys_role,prompt, llm_name)
    else:
        output_M2 = gpt_call(prompt,llm_name, sys_role)
    save_data(prompt, output_M2, DSL_path , llm_name)