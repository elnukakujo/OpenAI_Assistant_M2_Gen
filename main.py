from prepare_prompt import prepare_prompt
from call_llm import call_llm
from convert_ecore import convert_ecore

def main(example_method, DSL_name, llm_idx):
    """
    Do not edit this function.
    Main function to prepare a prompt, call a LLM API, and convert the output to Ecore format.

    Args:
        example_method (str): The example method to be used in the prompt preparation corresponding to the explanations passed to the LLM, depends on the dsl_names in the data/Example folder. Example values are:
        {
            "1shot_<dsl>": Uses the example in the data/Example/<dsl> folder,
            "2shot_<dsl1>_<dsl2>": Uses the examples in the data/Example/<dsl1> and data/Example/<dsl2> folders,
            ...,
            "nshot": Uses all the examples in the data/Example folder
        }.
        
        DSL_name (str): The name of the Domain-Specific Language (DSL) to be used corresponding to the directory with the domain informations.
        llm_idx (int): The index of the LLM model to be called. The four current options are:
        {
            0: "gpt-3.5-turbo",
            1: "gpt-4"
        }.

    Returns:
        None
    """
    print("Preparing the prompt...")
    prompt = prepare_prompt(example_method, DSL_name)
    print("----------------------")
    print("Preparing the call to the API...")
    call_llm(prompt, llm_idx, DSL_name)
    print("----------------------")
    print("Converting the output to Ecore...")
    convert_ecore(DSL_name)
    
if __name__ == "__main__":
    # Edit your parameters here
    example_method = "1shot_btms"
    DSL_name = "Tile-O"
    llm_idx = 0
    # Edit your parameters here
    main(example_method, DSL_name, llm_idx)