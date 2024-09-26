from openai import OpenAI

def get_api_key(path):
    key_file = open(path, "r")
    api_key = key_file.read()
    key_file.close()
    return api_key

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

client = OpenAI(api_key=get_api_key("openai_key.txt"))
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