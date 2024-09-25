from openai import OpenAI

def get_api_key(path):
    key_file = open(path, "r")
    api_key = key_file.read()
    key_file.close()
    return api_key

client = OpenAI(api_key=get_api_key("openai_key.txt"))

prompt = "How to find an internship in Montreal in Computer Science?"

response = client.chat.completions.create(model="gpt-3.5-turbo",
messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
])

assistant_message = response.choices[0].message.content
print("AI says:", assistant_message)