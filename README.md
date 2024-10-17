# OpenAI_Assistant_M2_Gen

This project aims at designing a Model assistant to design metamodels for Domain Specific Languages, using OpenAI API and prompt engineering.


Based on the findings of the article called [Automated Domain Modeling with Large Language Models: A Comparative Study](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10344012), and with the supervision of my IFT6253 professor.

Using poetry for package management

The folder data contains the problems descriptions, the analysis of the result and their evaluation from the article cited above ([downloaded here](https://zenodo.org/records/8105098))

## The data folder
M2_ebnf_format.txt contains the format given used to define the metamodels.
The folder DSL2Gen contains the problem descriptions and the solutions for the DSLs to try and generate with GPT.
The folder Example contains the 3shot.txt that is to be passed as example to GPT. In an attempt for better result than the article with GPT4, I use their best method and try to add one more example for maybe a better recall and F1 score.