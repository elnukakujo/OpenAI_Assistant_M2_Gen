from openai import OpenAI
from dotenv import load_dotenv
import json
import os
from conversion import convert_json2nl

def gpt_prepare_shots_prompt(shots, user_prompt, sys_role):
    """
    Prepares a list of shot messages for a GPT model prompt.

    Args:
        shots (list of tuples): A list of (user_input, assistant_response) pairs to be used as examples.
        user_prompt (str): The main user prompt to be sent to the GPT model.
        sys_role (str): The system role message to set the context for the GPT model.

    Returns:
        list of dict: A list of message dictionaries formatted for the GPT model.
    """
    messages =[{"role": "system", "content": sys_role}]
    if shots is not None:
        for shot in shots:
            messages.append({"role": "user", "content": shot[0]})
            messages.append({"role": "assistant", "content": json.dumps(shot[1])})
    messages.append({"role": "user", "content": user_prompt})
    return messages

def gpt_unique_call(client, prompt, llm_name):
    """
    Generates a unique GPT call to create a class diagram from a textual description.

    Args:
        client: The client object used to interact with the GPT model.
        prompt: A dictionary containing 'prompt_ex' and 'user_prompt' keys with their respective prompts.
        llm_name: The name of the language model to be used for the GPT call.

    Returns:
        str: The content of the GPT model's response message.

    The function prepares the prompt messages by combining example prompts and user prompts with a system role description.
    It then makes a call to the GPT model to generate a response based on the provided prompts.
    """
    sys_role = "You are an expert in designing and validating models from a textual description for domain models returning only valid Json files with only components from the description. Ensure all referenced classes are explicitly defined within the input."
    if prompt["pre_model"] is not None:
        sys_role += f"\n To design the model, you use the following model as a base: \n {json.dumps(prompt['pre_model'])}"
    messages = gpt_prepare_shots_prompt(prompt['prompt_ex'], prompt['user_prompt'], sys_role)
    return client.chat.completions.create(model=llm_name, messages=messages).choices[0].message.content

def gpt_task_call(client, prompt, divide, llm_name):
    """
    Executes a GPT task call to generate tasks to build a model, and then apply them incrementaly.
    Args:
        client: The client object used to interact with the GPT model.
        prompt (dict): A dictionary containing the prepared example prompt and user prompt.
        divide (str): The method to divide tasks, either "auto" or "manual".
        llm_name (str): The name of the language model to use for generating completions.
    Returns:
        tuple: A tuple containing the final response and the list of tasks.
    Raises:
        Exception: If the divide method is invalid or if task parsing fails.
    """
    if divide == "auto":
        sys_role = "You are an expert in designing CRUD operation tasks for another LLM to build a model. A model is composed of enumerations and classes. Classes are composed of attributes with types (int, double, boolean, Date, string, and enumerations custom types) and relationships which have multiplicities and can be inherit, associate or contain. However, models don't have methods. You receive a textual description of a problem domain and return a list of 5 very detailed and precise tasks containing CRUD operations in a 1D json array containing only str of what the other LLM should do to create a correct model. Do not talk about CRUD operations in the tasks. The other LLM won't have access to this description so always specify everything to him."
        if prompt["pre_model"] is not None:
            sys_role += f"\n To design those tasks, you use the following model as a base: \n {json.dumps(prompt['pre_model'])}"
        messages =[{"role": "system", "content": sys_role}]
        messages.append({"role": "user", "content": prompt["user_prompt"]})
        response = client.chat.completions.create(model=llm_name, messages=messages).choices[0].message.content
        try:
            tasks = json.loads(response.strip("```json\n").strip("```"))
        except:
            print(tasks)
            raise Exception("Failed to parse tasks from GPT response: Restart the process manually")
    elif divide == "manual":
        tasks = prompt["user_prompt"].split('\n\n')
    else:
        raise Exception("Invalid divide method")
    
    response = {}
    
    sys_role = "You are an expert in designing and validating models for domain models returning only valid Json files. You receive tasks with the format of CRUD operations as well as a model from previous tasks and return a valid json object using the same format as the shots above. A model is composed of enumerations and classes. Classes are composed of attributes with types (int, double, boolean, Date, string, and enumerations custom types) and relationships which have mul and can be inherit, associate or contain. Return only valid Json files as shown in the shots, and USE THE PREVIOUS model AS BASE! USE THE PREVIOUS model AS BASE! USE THE PREVIOUS model AS BASE!"
    if prompt["pre_model"] is not None:
            sys_role += f"\n To design the model, you use the following model as a base: \n {json.dumps(prompt['pre_model'])}"
    
    i=0
    for task in tasks:
        print("----------------------")
        print(f"Task {i}: {task}")
        messages = gpt_prepare_shots_prompt(prompt['prompt_ex'], task +"\n Previous model: \n"+json.dumps(response), sys_role)
        response = client.chat.completions.create(model=llm_name, messages=messages).choices[0].message.content
        print(convert_json2nl(response))
        i+=1
    return response, tasks

def gpt_call(prompt, divide, llm_name):
    """
    Makes a call to the GPT model using the provided prompt and parameters.

    Args:
        prompt (dict): A dictionary containing the prepared example prompt and user prompt.
        divide (str): A string indicating whether to divide the task into subtasks.
        llm_name (str): The name of the language model to be used.

    Returns:
        tuple: A tuple containing the response from the GPT model and the tasks (if any).
    """

    load_dotenv()
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    if divide != "":
        response, tasks = gpt_task_call(client, prompt, divide, llm_name)
    else:
        response = gpt_unique_call(client, prompt, llm_name)
        tasks = ""
    return response, tasks