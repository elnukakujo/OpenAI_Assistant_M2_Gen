import json
from common import *
import xml.etree.ElementTree as ET

def convert_json2ecore(data, dsl_name, file_name):
    """
    Converts a JSON representation of a class diagram into an Ecore model and saves it as an .ecore file.
    Args:
        data (str or dict): The JSON data representing the class diagram. Can be a JSON string or a dictionary.
        dsl_name (str): The name of the DSL (Domain-Specific Language) to be used in the file path.
        file_name (str): The name of the output .ecore file (without extension).
    Raises:
        Exception: If the input data is a string and cannot be parsed as valid JSON.
    The JSON data should have the following structure:
    {
        "enum": [
            {
                "name": "EnumName",
                "values": ["Value1", "Value2", ...]
            },
            ...
        ],
        "class_": [
            {
                "name": "ClassName",
                "abstract": true | false,
                "attributes": [
                    {
                        "name": "attributeName",
                        "type": "string" | "int" | "boolean" | "float" | "double" | "time" | "date" | "array" | "customType"
                    },
                    ...
                ],
                "contains": [
                    {
                        "to": "ContainedClassName",
                        "mul": "0..1" | "1" | "*"
                    },
                    ...
                ],
                "associate": [
                    {
                        "to": "AssociatedClassName",
                        "mul": "0..1" | "1" | "*"
                    },
                    ...
                ],
                "inherit": ["SuperClassName", ...]
            },
            ...
        ]
    }
    The function creates an Ecore model with the following elements:
    - EPackage: The root element of the Ecore model.
    - EEnum: Enumeration types defined in the JSON data.
    - EClass: Classes defined in the JSON data, with attributes, containment relationships, association relationships, and inheritance.
    The resulting Ecore model is saved to the specified file path.
    """
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            print(data)
            raise Exception("The LLM output data is not a valid JSON string.")
    # Create the root EPackage element
    ecore_model = ET.Element("ecore:EPackage", {
        "xmi:version": "2.0",
        "xmlns:xmi": "http://www.omg.org/XMI",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xmlns:ecore": "http://www.eclipse.org/emf/2002/Ecore",
        "name": "ClassDiagram",
        "nsURI": "http://www.example.org/ClassDiagram",
        "nsPrefix": "ClassDiagram"
    })
    
    # Add enumerations
    if "enum" in data:
        for enum in data["enum"]:
            enum_class = ET.SubElement(ecore_model, "eClassifiers")
            enum_class.set("xsi:type", "ecore:EEnum")
            enum_class.set("name", enum["name"])
            for value in enum["values"]:
                enum_value = ET.SubElement(enum_class, "eLiterals", name=value)
    
    # Add classes
    if "class_" in data:
        for cls in data["class_"]:
            e_class = ET.SubElement(ecore_model, "eClassifiers")
            e_class.set("xsi:type", "ecore:EClass")
            e_class.set("name", cls["name"])
            e_class.set("abstract", "true" if cls["abstract"] else "false")

            # Add attributes
            if "attributes" in cls:
                for attr in cls["attributes"]:
                    e_attr = ET.SubElement(e_class, "eStructuralFeatures")
                    e_attr.set("xsi:type", "ecore:EAttribute")
                    e_attr.set("name", attr["name"])
                    
                    ecore_types = ["string", "int", "boolean", "float", "double", "time", "date", "array"]
                    if attr["type"].lower() in ecore_types:
                        e_attr.set("eType", f"ecore:EDataType http://www.eclipse.org/emf/2002/Ecore#//E{attr['type'].capitalize()}")
                    else:
                        e_attr.set("eType", f"#//{attr['type'].capitalize() if attr['type'].lower()==attr['type'] else attr['type']}")
            
            # Add containment relationships
            if "contains" in cls:
                for contain in cls["contains"]:
                    e_ref = ET.SubElement(e_class, "eStructuralFeatures")
                    e_ref.set("xsi:type", "ecore:EReference")
                    e_ref.set("name", contain["to"])
                    e_ref.set("eType", f"#//{contain['to']}")
                    e_ref.set("containment", "true")
                    if contain["mul"] == "*":
                        e_ref.set("upperBound", "-1")
            
            # Add association relationships
            if "associate" in cls:
                for associate in cls["associate"]:
                    e_ref = ET.SubElement(e_class, "eStructuralFeatures")
                    e_ref.set("xsi:type", "ecore:EReference")
                    e_ref.set("name", associate["to"])
                    e_ref.set("eType", f"#//{associate['to']}")
                    if associate["mul"] == "*":
                        e_ref.set("upperBound", "-1")
            
            # Add inheritance if present
            if "inherit" in cls and len(cls["inherit"])>0:
                e_inherit = ET.SubElement(e_class, "eSuperTypes")
                for super_type in cls["inherit"]:
                    e_inherit.set("href", f"#//{super_type}")
                    
    tree = ET.ElementTree(ecore_model)
    if not os.path.exists(f"data/DSL2Gen/{dsl_name}/ecore/"):
        os.makedirs(f"data/DSL2Gen/{dsl_name}/ecore/")
    tree.write(f"data/DSL2Gen/{dsl_name}/ecore/{file_name}.ecore")

def convert_json2nl(data):
    """
    Convert JSON data to a natural language representation.
    This function takes a JSON object or a JSON string and converts it into a 
    human-readable natural language format. The JSON data is expected to contain 
    information about enumerations and classes.
    Args:
        data (str or dict): The JSON data to be converted. It can be a JSON string 
                            or a dictionary.
    Returns:
        str: A string containing the natural language representation of the JSON data.
    Raises:
        Exception: If the input data is a string and cannot be parsed as JSON.
    Example:
        >>> json_data = {
        ...     "enum": [
        ...         {"name": "Color", "values": ["Red", "Green", "Blue"]}
        ...     ],
        ...     "class_": [
        ...         {
        ...             "name": "Car",
        ...             "abstract": False,
        ...             "attributes": [{"type": "string", "name": "model"}],
        ...             "contains": [{"mul": "1..*", "to": "Wheel"}],
        ...             "inherit": ["Vehicle"],
        ...             "associate": [{"mul": "0..1", "to": "Driver"}]
        ...         }
        ...     ]
        ... }
        >>> print(convert_json2nl(json_data))
        Enumerations:
        Color(Red, Green, Blue)
        Classes:
        Car(string model, inherit Vehicle contain (1..*) Wheel associate (0..1) Driver)
    """
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            print(data)
            raise Exception("The LLM output data is not a valid JSON string.")
    
    nl_output = []
    # Process Enumerations
    if "enum" in data:
        nl_output.append("Enumerations:")
        for enum in data["enum"]:
            enum_values = ", ".join(enum["values"])
            nl_output.append(f"{enum['name']}({enum_values})")
        nl_output.append("")  # Blank line for separation

    # Process Classes
    if "class_" in data:
        nl_output.append("Classes:")
        for cls in data["class_"]:
            contains = ", ".join(
                [f"contain ({item['mul']}) {item['to']}" for item in cls.get("contains", [])]
            )
            attributes = ", ".join(
                [f"{attr['type']} {attr['name']}" for attr in cls.get("attributes", [])]
            )
            inherits = "".join(cls.get("inherit", []))
            associates = ", ".join(
                [f"associate ({item['mul']}) {item['to']}" for item in cls.get("associate", [])]
            )

            # Combine class declaration
            declaration = f"{'abstract ' if cls['abstract'] else ''}{cls['name']}("
            if attributes:
                declaration += f"{attributes}, "

            # Add inheritance if present
            if inherits:
                declaration += f"inherit {inherits} "

            # Add containment relationships
            if contains:
                declaration += f"{contains} "

            # Add associations if present
            if associates:
                declaration += f"{associates} "
            if declaration.endswith(", "):
                declaration = declaration[:-2]
            elif declaration.endswith(" "):
                declaration = declaration[:-1]
                
            declaration += ")"

            nl_output.append(declaration.strip(", "))
        nl_output.append("")  # Blank line for separation

    return "\n".join(nl_output)

def prompt_list2string(prompt):
    """
    Converts a prompt dictionary into a formatted string.

    Args:
        prompt (dict): A dictionary containing the following keys:
            - "prompt_ex" (list): A list of tuples, where each tuple contains:
                - A string representing the example domain description.
                - A JSON object representing the example solution.
            - "user_prompt" (str): A string representing the user's prompt.

    Returns:
        str: A formatted string combining the example domain descriptions, 
             example solutions, and the user prompt.
    """
    prompt_str = ""
    for shot in prompt["prompt_ex"]:
        prompt_str += "Example domain description: \n"+shot[0]+ "Example solution: \n" + convert_json2nl(shot[1]) + "\n###\n"
    prompt_str += "User prompt: \n"+prompt["user_prompt"]
    return prompt_str