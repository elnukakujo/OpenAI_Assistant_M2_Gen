import antlrConversion.conversion as conversion
import common

input = common.read_file('antlrConversion/output.txt')
output = conversion.conversion(input)
common.write_file('antlrConversion/output.ecore', output)