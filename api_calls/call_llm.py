from common import *
from conversion import *
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
from api_calls.llama_call import llama_call
import os
import json

def save_data(prompt,output, DSL_path, llm_name):
    write_json(f'{DSL_path}/json/prompt.json', prompt)
    write_json(f'{DSL_path}/json/output.json', output)
    prompt = prompt_list2string(prompt)
    if os.path.exists(f'{DSL_path}/input_output_GPT.csv'):
        df = pd.read_csv(f'{DSL_path}/input_output_GPT.csv', index_col=0)
        if 'Solution' in df.columns and os.path.exists(f'{DSL_path}/json/solution.json'): 
            solution = convert_json2nl(read_json(f'{DSL_path}/json/solution.json'))
            df = df[['Prompt', 'Output', 'Solution']]
            df.loc[llm_name] = [prompt, convert_json2nl(output), solution]
            
        elif 'Solution' in df.columns and not os.path.exists(f'{DSL_path}/json/solution.json'):
            df = df[['Prompt', 'Output', 'Solution']]
            df.loc[llm_name] = [prompt, convert_json2nl(output), ""]
            
        else:
            df = df[['Prompt', 'Output']]
            df.loc[llm_name] = [prompt, convert_json2nl(output)]
    else:
        if os.path.exists(f'{DSL_path}/json/solution.json'):
            solution = convert_json2nl(read_json(f'{DSL_path}/json/solution.json'))
            df = pd.DataFrame([[prompt, convert_json2nl(output), solution]], columns=['Prompt', 'Output', 'Solution'], index=[llm_name])
        else:
            df = pd.DataFrame([[prompt, convert_json2nl(output)]], columns=['Prompt', 'Output'], index=[llm_name])
    df.index.name = 'LLM_name'
    df.to_csv(f'{DSL_path}/input_output_GPT.csv', index=True)

def gpt_message(prompt, sys_role):
    messages =[{"role": "system", "content": sys_role}]
    for shot in prompt["prompt_ex"]:
        messages.append({"role": "user", "content": shot[0]})
        messages.append({"role": "assistant", "content": json.dumps(shot[1])})
    messages.append({"role": "user", "content": prompt["user_prompt"]})
    return messages

def gpt_call(prompt, llm_name, sys_role):
    load_dotenv()
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(model=llm_name, messages=gpt_message(prompt, sys_role))
    return response.choices[0].message.content

def call_llm(prompt, llm_idx, DSL_folder):
    DSL_path = "data/DSL2Gen/"+DSL_folder
    llm_list = ["gpt-3.5-turbo","gpt-4","Llama3.2-3B-Instruct", "Llama3.2-3B"]
    llm_name = llm_list[llm_idx]
    sys_role = "You are an expert in designing and validating class diagrams for domain models returning valid Json files. RETURN A JSON, RETURN A JSON, RETURN A JSON. FOLLOW THE EXAMPLES AND RETURN A JSON. Ensure all referenced classes are explicitly defined within the input."
    if llm_idx == 2 or llm_idx==3:
        output_M2 = llama_call(sys_role,prompt, llm_name)
    else:
        output_M2 = gpt_call(prompt,llm_name, sys_role)
    save_data(prompt, output_M2, DSL_path , llm_name)