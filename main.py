from generateDsls import generateDsls
from antlrConversion.conversion import csv_convertion
from exportEcore import export_ecore

print("Generating DSLs in the csv...")
generateDsls()
print("Converting Outputs and Solutions in XMI in the csv...")
csv_convertion()
print("Extracting xmi elements from the csv to data/extracted...")
export_ecore()