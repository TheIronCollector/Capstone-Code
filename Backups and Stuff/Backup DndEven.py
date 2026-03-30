import math

n = int(input("n="))
terms = []

#Proper Rotations (C)

def proper_top_function(x):
    return int(2*math.gcd(n,x))

def calculate_proper_top_values(start, end):
    values_list = []
    for x in range(start, end + 1):
        value = proper_top_function(x)
        values_list.append(value)
    return values_list

def proper_bottom_function(x):
    return int(n/math.gcd(n,x))

def calculate_proper_bottom_values(start, end):
    values_list = []
    for x in range(start, end + 1):
        value = proper_bottom_function(x)
        values_list.append(value)
    return values_list

#Improper Rotations (S)

def improper_top_function(x):
    if int(x) % 2 == 1:
        return int(math.gcd(2*n,x))
    else:
        return 0

def calculate_improper_top_values(start, end):
    values_list = []
    for x in range(start, end + 1):
        value = improper_top_function(x)
        values_list.append(value)
    return values_list

def improper_bottom_function(x):
    if int(x) % 2 == 1:
        return int(2*n/math.gcd(2*n,x))
    else:
        return 0

def calculate_improper_bottom_values(start, end):
    values_list = []
    for x in range(start, end + 1):
        value = improper_bottom_function(x)
        values_list.append(value)
    return values_list

#Everything else

terms.append(f"1x^{2*n}_{1}")
terms.append(f"{int(n+1)}x^{n}_{2}")

start_range = 1
end_range = int((n/2)-1)
term_2_range = int(((3*n)/2)+3)
improper_top_values = calculate_improper_top_values(start_range, int(n-1))
proper_top_values = calculate_proper_top_values(start_range, end_range)
improper_bottom_values = calculate_improper_bottom_values(start_range, int(n-1))
proper_bottom_values = calculate_proper_bottom_values(start_range, end_range)

ST=improper_top_values
SB=improper_bottom_values
CT=proper_top_values
CB=proper_bottom_values

#Combines all like terms

for CTi,CBi in zip(CT, CB):
    terms.append(f"2x^{CTi}_{CBi}")

for STi,SBi in zip(ST,SB):
    terms.append(f"2x^{STi}_{SBi}")

term_dict = {}  # Dictionary to store terms with the same variable

for term in terms:
    coefficient, variable_exponent = term.split('x^')
    coefficient = int(coefficient)
    if variable_exponent in term_dict:
        term_dict[variable_exponent] += coefficient
    else:
        term_dict[variable_exponent] = coefficient

combined_terms = []
for variable_exponent, coefficient in term_dict.items():
    combined_terms.append(f"{coefficient}x^{variable_exponent}")

def remove_terms_with_0_0(terms):
    filtered_terms = [term for term in terms if "0_0" not in term]
    return filtered_terms

filtered_terms = remove_terms_with_0_0(combined_terms)
print(filtered_terms, f"{int(n)}x^{2}_{1} x^{n-1}_{2}")