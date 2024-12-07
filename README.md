# OpenAI_Assistant_M2_Gen

## General Informations
This project aims at designing a Model assistant to design metamodels for Domain Specific Languages, using OpenAI API and prompt engineering.

Based on the findings of the article called [Automated Domain Modeling with Large Language Models: A Comparative Study](https://ieeexplore.ieee.org/document/10344012), and with the supervision of my IFT6253 professor.

Currently supports gpt-3-turbo, gpt-4, and gemini-1.5-flash models:
- gemini-1.5-flash: free,
- gpt-3-turbo: cheap,
- gpt-4: expensive, around 0,80$ with divide=auto and 3shots.

## The data folder
- The folder **DSL2Gen** contains the problem descriptions and the outputs of the DSLs. 
    - **description.txt** is the domain description for the LLM to build from. It is mandatory for the assistant to work.
    - **json/solution.json** is for evaluation of the output purpose, comparing the LLM output with the product of a domain expert with the same domain description.
    - **json/pre_model.json** is if the user wants the assistant to work on an existing version of the model.

- The folder **Example** contains the domain description/solution examples to pass to the LLM. The folder requires:
    - **description.txt** the problem description
    - **solution.json** The solution model defined using the json format you want

## How to use
1. Go to DSL2Gen: `cd data/DSL2Gen`
2. Create a new folder with the name of your DSL: `mkdir <your_dsl>`
3. Create the DSL files:
    1. Create **description.txt** and add the domain description
    2. Create two directories named json, for the model and prompts before ecore conversion, and ecore, for output and solution ecore files
    3. (If you have a solution you want the parser to also transform in ecore, create **json/solution.json** and put the solution model there defined using the same json format, see previous point)
    4. (If you have an existing model you want the model to work on, create a **json/pre_model.json** and put the existing model there defined using the same json format, see previous point)
4. In the root directory, open **main.py**, define the dsl you want the model as well as the type of LLM model and prompting method you want:
    1. **shots**: The example prompt you want, defining how many dsl example you want, and specifying the names corresponding to the dsl folders in data/Example/. Note: Need to add a description.txt and a solution.json
    2. **divide**: If the textual problem description needs to be divided for a better LLM understanding, and if yes, how. Available options: "", "manual", "auto". Manual separates the description.txt for each `\n\n`, and auto passes the full description to the LLM to generate tasks he should follow later.
    3. **DSL_name**: The name of your DSL corresponding to the folder in **data/DSL2Gen**. You need a **description.txt** and json and ecore folders
    4. **llm_idx**: Which LLM model you want to use, the number corresponds to the index in the list of possible model names (see main() documentation for more info). There are options for gpt3-turbo and gpt4.
5. In the root directory, create a **.env** file and place your api keys as follow:
```
OPENAI_API_KEY = <your_key>
GEMINI_API_KEY = <your_key>
```
6. With the terminal inside the root directory, enter:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
7. Still with a terminal in the root directory, run the program by entering: `python3 main.py`. Be wary that:
    1. LLM models might have varying costs and delays
    2. LLM might not always return valid outputs you might need to restart the program more than 2 time if unlucky.
8. After the program ran, open the **generated.csv** file located in your DSL directory to see the inputs, outputs and ecore outputs for each llm model and parameters you tried.

### How to use with OpenAI API
As described earlier you need to create a .env file in the root of the repository and define your OpenAI api key as the variable **OPENAI_API_KEY**

### How to use with Gemini Api
As described earlier you need to create a .env file in the root of the repository and define your Gemini api key as the variable **GEMINI_API_KEY**

## How the system works
![SystemStateDiagram](https://github.com/user-attachments/assets/a04ef724-86ce-480f-94ed-0f3253015d23)


## Evaluation process
Done manually by comparing each outputted ecore model with the solution ecore model using EMF Compare in Epsilon Eclipse.
I compute the precision, recall and F1 score using the same categories as in the article above.
