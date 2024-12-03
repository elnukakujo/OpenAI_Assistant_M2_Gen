from prepare_prompt import prepare_prompt
from call_llm import call_llm
from convert_ecore import convert_ecore

def main(shots, divide, DSL_name, llm_idx):
    """
    Do not edit this function.
    Main function to prepare a prompt, call a LLM API, and convert the output to Ecore format.

    Args:
        shots (str): The example method to be used in the prompt preparation corresponding to the explanations passed to the LLM, depends on the dsl_names in the data/Example folder. Example values are:
        {
            "0shot": Does not use any example,
            "1shot_<dsl>": Uses the example in the data/Example/<dsl> folder,
            "2shot_<dsl1>_<dsl2>": Uses the examples in the data/Example/<dsl1> and data/Example/<dsl2> folders,
            ...,
            "nshot": Uses all the examples in the data/Example folder
        }.
        divide (str): Whether the problem textual description is divided in smaller tasks to be passed one by one to the LLM model. Example values are:
        {
            "": Pass the full description to the LLM at once,
            "manual": Divides tasks between "/n /n" in the description,
            "auto": Uses the LLM to divide the tasks before genereating the metamodel.
        }.
        DSL_name (str): The name of the Domain-Specific Language (DSL) to be used corresponding to the directory with the domain informations.
        llm_idx (int): The index of the LLM model to be called. The four current options are:
        {
            0: "gpt-3.5-turbo",
            1: "gpt-4",
            2: "gemini-1.5-flash"
        }.

    Returns:
        None
    """
    print("Preparing the prompt...")
    prompt = prepare_prompt(shots, DSL_name)
    print("----------------------")
    print("Preparing the call to the API...")
    call_llm(prompt, divide, llm_idx, DSL_name, shots)
    print("----------------------")
    print("Converting the output to Ecore...")
    convert_ecore(DSL_name)
    print("Done!")
    
if __name__ == "__main__":
    # Edit your parameters here
    shots = "nshot"
    divide = "auto"
    DSL_name = "HBMS"
    llm_idx = 2
    # Edit your parameters here
    main(shots, divide, DSL_name, llm_idx)