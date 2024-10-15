from openai import OpenAI
from dotenv import load_dotenv
import os

def get_prompt(path):
    key_file = open(path, "r")
    prompt = key_file.read()
    key_file.close()
    return prompt

def write_output(path, output):
    key_file = open(path, "w")
    key_file.write(output)
    key_file.close()
    return True

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": get_prompt("prompt.txt")}
])

assistant_message = response.choices[0].message.content
print(assistant_message)
print("")
print("----------------------------------------------------------------------------")
print("")
if write_output("output.txt", assistant_message):
    print("Output written to output.txt")
else:
    print("Error writing output")