import os

from prepare_prompt import prepare_prompt
from call_llm import call_llm
from convert_ecore import convert_ecore

def main(example_method, DSL_name, llm_idx):
    print("Preparing the prompt...")
    prompt = prepare_prompt(example_method, DSL_name)
    print("----------------------")
    print("Preparing the call to the API...")
    call_llm(prompt, llm_idx, DSL_name)
    print("----------------------")
    print("Converting the output to Ecore...")
    convert_ecore(DSL_name)
    
if __name__ == "__main__":
    example_method = "3shot"
    DSL_name = "HBMS"
    llm_idx = 0
    main(example_method, DSL_name, llm_idx)