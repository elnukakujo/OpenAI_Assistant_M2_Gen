# OpenAI_Assistant_M2_Gen

## General Informations
This project aims at designing a Model assistant to design metamodels for Domain Specific Languages, using OpenAI API and prompt engineering.

Based on the findings of the article called [Automated Domain Modeling with Large Language Models: A Comparative Study](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10344012), and with the supervision of my IFT6253 professor.

Using poetry for package management

## The data folder
- The folder **DSL2Gen** contains the problem descriptions and the outputs of the DSLs. 
    - **description.txt** is the domain description for the LLM to build from. It is mandatory for the assistant to work.
    - **pre_model.txt** is, in the case the user has an existing version of a model related to the domain he wants the LLM to complete/upgrade, made to contain this *pre* model.
    - **solution.txt** is for evaluation of the output purpose, comparing the LLM output with the product of a domain expert with the same domain description.

- The folder **Example** contains the prompt methods for the domain description/solution examples to pass to the LLM.
    - **3shot.txt** gives the problem description followed by the solution of 3 DSLs found in the article.

## How to use

1. Go to DSL2Gen: `cd data/DSL2Gen`
2. Create a new folder with the name of your DSL: `mkdir <your_dsl>`
3. Create the DSL files:
    1. Create **description.txt** and add the domain description
    2. (If you have a *pre* model, create **pre_model.txt** and put the model inside. **Note**: Try to define it using the ANTLR grammar defined in the root directory in **/antlrConversion/ClassDiagram.g4**)
    3. (If you have a solution you want the parser to also transform in ecore, create **solution.txt** and put the solution model there defined using the ANTLR grammar, see previous point)
4. In the root directory, open **main.py**
    1. **example_method**: The example prompt you want, the name correspond to the .txt file in data/Example/ with the prompt explanation you give
    2. **DSL_name**: The name of your DSL corresponding to the folder in **data/DSL2Gen**
    3. **llm_idx**: Which LLM model you want to use, the number corresponds to the index in the list of possible model names (see main() documentation for more info)
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

## TODO
- [ ] Add LLama 3.2 lightweight (and multimodal if free)
- [ ] Add new prompt methods for the examples (maybe 3shots CoT)
- [ ] Add docu
- [ ] Add support for situation with no solution.txt
- [ ] (Finish implementing evaluation sys in eclispe java)