import os

from prepare_prompt import prepare_prompt
from call_llm import call_llm
from convert_ecore import convert_ecore

print("Preparing the prompt...")
prompt = prepare_prompt("3shot", "HBMS")
print("----------------------")
print("Preparing the call to the API...")
call_llm(prompt, 0, "HBMS")
print("----------------------")
print("Converting the output to Ecore...")
convert_ecore("HBMS")