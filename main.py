from prepare_prompt import prepare_prompt
from api_calls.call_llm import call_llm
from convert_ecore import convert_ecore

def main(example_method, DSL_name, llm_idx):
    """
    Do not edit this function.
    Main function to prepare a prompt, call a LLM API, and convert the output to Ecore format.

    Args:
        example_method (str): The example method to be used in the prompt preparation corresponding to the explanations passed to the LLM in data/Example/<>.txt.
        DSL_name (str): The name of the Domain-Specific Language (DSL) to be used corresponding to the directory with the domain informations.
        llm_idx (int): The index of the LLM model to be called. The two current options are:
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
    example_method = "1shot_labtracker"
    DSL_name = "HBMS"
    llm_idx = 2
    # Edit your parameters here
    main(example_method, DSL_name, llm_idx)