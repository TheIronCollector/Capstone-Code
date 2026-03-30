import re
from sympy import symbols, expand

def convert_expression(input_str, variables):
    # Define a pattern to match each term in the input string
    pattern = r'(\d+)?x\^(\d+)_(\d+)'
    
    # Define a function to replace each matched term with the desired format
    def replace_term(match):
        coefficient = match.group(1) if match.group(1) else '1'
        exponent = match.group(2)
        variable_terms = '+'.join([f'({var}**{match.group(3)})' for var in variables])
        return f'{coefficient}*({variable_terms})**{exponent}'
    
    # Replace all matched terms in the input string
    converted_str = re.sub(pattern, replace_term, input_str)
    
    return converted_str

# Example usage
input_str = "1x^10_1 + 6x^5_2 + 4x^2_5 + 4x^1_10 + 5x^2_1 * x^4_2"
variables = ['a', 'b']
converted_str = convert_expression(input_str, variables)

# Convert to sympy symbols
a, b = symbols('a b')

# Expand the expression
converted_expr = eval(converted_str)
expanded_expression = expand(converted_expr)
print("Expanded expression:", expanded_expression)
