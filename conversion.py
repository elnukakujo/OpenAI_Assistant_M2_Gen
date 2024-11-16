import json
from common import *
import xml.etree.ElementTree as ET
from xml.dom import minidom
import io

def convert_json2ecore(data, dsl_name, file_name):
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
    if "class" in data:
        for cls in data["class"]:
            e_class = ET.SubElement(ecore_model, "eClassifiers")
            e_class.set("xsi:type", "ecore:EClass")
            e_class.set("name", cls["name"])

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
    tree.write(f"data/DSL2Gen/{dsl_name}/ecore/{file_name}.ecore")

def convert_json2nl(data):
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
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
    if "class" in data:
        nl_output.append("Classes:")
        for cls in data["class"]:
            contains = ", ".join(
                [f"contain ({item['mul']}) {item['to']}" for item in cls.get("contains", [])]
            )
            attributes = ", ".join(
                [f"{attr['type']} {attr['name']}" for attr in cls.get("attributes", [])]
            )
            inherits = ", ".join(cls.get("inherit", []))
            associates = ", ".join(
                [f"associate ({item['mul']}) {item['to']}" for item in cls.get("associate", [])]
            )

            # Combine class declaration
            declaration = f"{cls['name']}("
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
    prompt_str = ""
    for shot in prompt["prompt_ex"]:
        prompt_str += "Example domain description: \n"+shot[0]+ "Example solution: \n" + convert_json2nl(shot[1]) + "\n###\n"
    prompt_str += "User prompt: \n"+prompt["user_prompt"]
    return prompt_str