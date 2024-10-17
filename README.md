# OpenAI_Assistant_M2_Gen

## General Informations
This project aims at designing a Model assistant to design metamodels for Domain Specific Languages, using OpenAI API and prompt engineering.

Based on the findings of the article called [Automated Domain Modeling with Large Language Models: A Comparative Study](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10344012), and with the supervision of my IFT6253 professor.

Using poetry for package management

The folder data contains the problems descriptions, the analysis of the result and their evaluation from the article cited above ([downloaded here](https://zenodo.org/records/8105098))

## The data folder
- M2_ebnf_format.txt contains the format given used to define the metamodels.
- The folder DSL2Gen contains the problem descriptions and the solutions for the DSLs to try and generate with GPT.
- The folder Example contains the 3shot.txt that is to be passed as example to GPT. In an attempt for better result than the article with GPT4, I use their best method and try to add one more example for maybe a better recall and F1 score.
- input_output_GPT.csv has 4 columns, the DSL name, the description, the prompt passed to the GPT using 3shot method, the output obtained. It contains the data for all the DSL defined in DSL2Gen

## The uniqueDslTest folder
generateDsl.py is the python script to load one of the DSL description in the DSL2Gen folder, add the 3shot example, format the prompt and save it in prompt.txt, send the generation request to gpt4 and save it in output.txt

## generateDsls.py
Have the same purpose as generateDsl.py but do all the folder DSL descriptions in data/DSL2Gen, preprocess the prompt, get the output and save everything in data/input_output_GPT.csv .