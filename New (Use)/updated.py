# I didn't feel like putting much effort into the docstrings, so if you have any questions,
# please email me at: jimic2006@gmail.com

from collections import defaultdict
from sympy.functions.combinatorial.numbers import totient
from sympy import divisors, symbols, expand, simplify, latex, Add, Mul
import pyperclip

# User inputs (most of them)
while True:
    try:
        groupType = input("Which point group? (Metallocene-like Dnh or Dnd): ")
        rotationOrder = int(input("What is the rotation order?: "))
        varNum = int(input("How many elements? (red and black -> 2) Please no more than 26. You'd need a good reason for a number like that: "))
    except:
        ...
    
    match groupType:
        case "Dnh":
            break
        case "Dnd":
            break

groupOrder = rotationOrder * 4

def filter_list(nums: list[tuple]) -> list[tuple]:
    """
    This function takes a formatted list of tuples and compresses it (combines like terms).

    Parameters:
        nums (list[tuples]): A formatted list of tuples.

    Returns:
        list[tuple]: An even more formatted list of tuples
    """
    # Filter list and combine elements
    combined = defaultdict(int)
    
    for term in nums:
        coeff, *key = term
        if 0 in key:
            continue  # Skip if any key element is zero
        combined[tuple(key)] += coeff

    return [(coeff, *key) for key, coeff in combined.items() if coeff != 0]

def even_Dnh(n: int) -> list[tuple]:
    """
    This function creates a formatted list of tuples.

    Parameters:
        n (int): Formatted list of values that describe the values in each term.

    Returns:
        list[tuple]: A formatted list of tuples
    """

    outList = []
    divisorsList = divisors(n)

    outList.append(((3 * n // 2) + 2, n, 2))
    outList.append((n // 2, 4, 1, n - 2, 2))

    for d in divisorsList:
        coeff = totient(d)
        subscript = d
        superscript = 2 * n // d

        impsubscript = 0
        impsuperscript = 0

        if d > 2 and d % 2 == 0:
            impsubscript = d
            impsuperscript = 2 * n // d

        elif d > 2 and d % 2 == 1:
            impsubscript = 2 * d
            impsuperscript = n // d

        outList.append((coeff, superscript, subscript))
        outList.append((coeff, impsuperscript, impsubscript))

    filteredList = filter_list(outList)
    return filteredList

def even_Dnd(n: int) -> list[tuple]:
    """
    This function creates a formatted list of tuples.

    Parameters:
        n (int): Formatted list of values that describe the values in each term.

    Returns:
        list[tuple]: A formatted list of tuples
    """

    outList = []
    divisorsList = divisors(n)
    ddivisorsList = divisors(2 * n)

    outList.append((n, n, 2))
    outList.append((n, 2, 1, n - 1, 2))

    for d in divisorsList:
        coeff = totient(d)
        subscript = d
        superscript = 2 * n // d

        outList.append((coeff, superscript, subscript))
        
    for d in ddivisorsList:
        if d % 4 == 0 and (2 * n)/d % 2 == 1:
            impcoeff = totient(d)
            impsubscript = d
            impsuperscript = 2 * n // d

        else:
            continue

        outList.append((impcoeff, impsuperscript, impsubscript))

    filteredList = filter_list(outList)
    return filteredList

def odd_Dnh_or_Dnd(n: int) -> list[tuple]:
    """
    This function creates a formatted list of tuples.

    Parameters:
        n (int): Formatted list of values that describe the values in each term.

    Returns:
        list[tuple]: A formatted list of tuples
    """

    outList = []
    divisorsList = divisors(n)

    outList.append((n + 1, n, 2))
    outList.append((n, 2, 1, n - 1, 2))

    for d in divisorsList:
        coeff = totient(d)
        subscript = d
        superscript = 2 * n // d

        impsubscript = 0
        impsuperscript = 0

        if d > 2:
            impsubscript = 2 * d
            impsuperscript = n // d

        outList.append((coeff, superscript, subscript))
        outList.append((coeff, impsuperscript, impsubscript))

    filteredList = filter_list(outList)
    return filteredList

# This is the only function made by Chat GPT-5
def substitute_and_expand(terms: list[tuple], num_vars: int, divisor: int) -> Add:
    """
    This function takes a formatted list of tuples and converts it into a simplified polynomial function.

    Parameters:
        terms (list[tuple]): Formatted list of values that describe the values in each term.
        num_vars (int): Number of variables. [(1: a) (2: a,b), ...]
        divisor (int): Value that the returned expression is divided by.
        
    Returns:
        Add: The simplified polynomial function
    """

    vars = symbols(' '.join(chr(ord('a') + i) for i in range(num_vars)))
    expr = 0

    for coeff, *var_parts in terms:
        if len(var_parts) % 2 != 0:
            raise ValueError(f"Invalid term {terms}: variable part must have even length")

        term_expr = coeff
        for exp, sub in zip(var_parts[::2], var_parts[1::2]):
            term_expr *= sum(v**sub for v in vars) ** exp
        expr += term_expr

    expr = simplify(expand(expr))

    # Always treat expression as Add
    terms = expr.as_ordered_terms()
    new_terms = []
    for term in terms:
        coeff, rest = term.as_coeff_mul()
        q, r = divmod(coeff, divisor)
        if r != 0:
            raise ValueError(f"Coefficient {coeff} not divisible by {divisor}")
        new_terms.append(Mul(q, *rest))

    return Add(*new_terms)

def get_generator(terms: list[tuple]) -> Add:
    """
    This function takes a formatted list of tuples and converts it into a generating function.

    Parameters:
        terms (list[tuple]): Formatted list of values that describe the values in each term.

    Returns:
        Add: The generating function (minus the coefficient in front)
    """

    var = symbols('n')
    expr = 0

    for coeff, *var_parts in terms:
        if len(var_parts) % 2 != 0:
            raise ValueError(f"Invalid term {terms}: variable part must have even length")
        
        term_expr = coeff
        for exp in var_parts[::2]:
            term_expr *= var ** exp
        expr += term_expr
    
    return expr

# Determining what to calculate based off of user inputs
if groupType == "Dnh" and rotationOrder % 2 == 0:
    terms = even_Dnh(rotationOrder)

elif groupType == "Dnd" and rotationOrder % 2 == 0:
    terms = even_Dnd(rotationOrder)

elif groupType == "Dnh" or groupType == "Dnd" and rotationOrder % 2 == 1:
    terms = odd_Dnh_or_Dnd(rotationOrder)

print(f"Num List: {terms}")

while True:
    option = input("Generator(g) or Detailed(d)? ")
    match option:
        case "d":
            out = f"{(latex(substitute_and_expand(terms, varNum, groupOrder)))}"
            break

        case "g":
            out = f"\\frac{{1}}{{{groupOrder}}} \\left( " + f"{latex(get_generator(terms))}" + " \\right)"
            break

        case _:
            continue

pyperclip.copy(out)
print(out)
print("Output copied to clipboard")
