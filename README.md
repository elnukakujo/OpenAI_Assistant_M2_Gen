# OpenAI_Assistant_M2_Gen

## General Informations
This project aims at designing a Model assistant to design metamodels for Domain Specific Languages, using OpenAI API and prompt engineering.

Based on the findings of the article called [Automated Domain Modeling with Large Language Models: A Comparative Study](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10344012), and with the supervision of my IFT6253 professor.

Currently supports gpt-3-turbo and gpt-4 models

## The data folder
- The folder **DSL2Gen** contains the problem descriptions and the outputs of the DSLs. 
    - **description.txt** is the domain description for the LLM to build from. It is mandatory for the assistant to work.
    - **pre_model.json** is, in the case the user has an existing version of a model related to the domain he wants the LLM to complete/upgrade, made to contain this *pre* model.
    - **solution.json** is for evaluation of the output purpose, comparing the LLM output with the product of a domain expert with the same domain description.

- The folder **Example** contains the domain description/solution examples to pass to the LLM. The folder requires:
    - **description.txt** the problem description
    - **solution.json** The solution model defined using the json format you want

## How to use
1. Go to DSL2Gen: `cd data/DSL2Gen`
2. Create a new folder with the name of your DSL: `mkdir <your_dsl>`
3. Create the DSL files:
    1. Create **description.txt** and add the domain description
    2. Create two directories named json, for the model and prompts before ecore conversion, and ecore, for output and solution ecore files
    2. (If you have a *pre* model, create **pre_model.json** and put the model inside /json. **Note**: Try to define it using the same json format as json files you pass as examples)
    3. (If you have a solution you want the parser to also transform in ecore, create **solution.json** and put the solution model there defined using the same json format, see previous point)
4. In the root directory, open **main.py**, define the dsl you want the model as well as the type of LLM model and prompting method you want:
    1. **example_method**: The example prompt you want, defining how many dsl example you want, and specifying the names corresponding to the dsl folders in data/Example/. Note: Need to add a description.txt and a solution.json
    2. **DSL_name**: The name of your DSL corresponding to the folder in **data/DSL2Gen**. You need a **description.txt** and json and ecore folders
    3. **llm_idx**: Which LLM model you want to use, the number corresponds to the index in the list of possible model names (see main() documentation for more info). There are options for gpt3-turbo and gpt4.
5. In the root directory, create a **.env** file and place your OpenAI Api key as follow:`OPENAI_API_KEY = <your_key>`
6. With the terminal inside the root directory, enter:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
7. Still with a terminal in the root directory, run the program by entering: `python3 main.py`. Be wary that:
    1. LLM models might have varying costs and delays
    2. LLM might not always return a valid outputs for ANTLR, meaning you might need to run the program a second or third time.
7. After the program ran, open the **input_output_GPT.csv** file located in your DSL directory to see the inputs, outputs and ecore outputs for each llm model you tried.

### How to use with OpenAI API
As described earlier you need to create a .env file in the root of the repository and define your OpenAI api key as the variable **OPENAI_API_KEY**

## How the system works
![SystemStateDiagram drawio](https://github.com/user-attachments/assets/70e3bc16-8e50-4e74-b2da-cc49bf760036)

## TODO
- [ ] Try automatic prompt engineering to divide generated tasks and then do the tasks to generate the model
- [ ] Try adding free gemini option
- [ ] (Do the evaluation for 1 shots of 3 distinct ex of DSL on 3 DSL2Gen on turbo and gpt4)
