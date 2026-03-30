from sympy.functions.combinatorial.numbers import totient
from sympy import divisors

# Making sure I understand divisors() and totient() from SymPy

# n = 30
# n2 = n * 2

# for d in divisors(n2):
#     if d % 4 == 0 and 2 * n/d % 2 == 1: 
#         print(f"{d}: {totient(d)}")

# --------------------------------------------------

# Maybe finding how to get generator functions quicker

n = 15
out = 2 * n * [0]

if n % 2 == 1:
    for d in divisors(2 * n):
        out[int(2*n/d) - 1] = totient(d)

    out[n - 1], out[n] = n + 1, n

print(out)

# --------------------------------------------------

# Messing around

# def getDigit1(num: int) -> int:
#     return int(num % 10 + (num / 10 % 10))

# def getDigit2(num: int) -> int:
#     numString: str = f'{num}'
#     return len(numString)

# print(f"{getDigit1(1043) = }")
# # getDigit1(1043) = 7

# print(f'{getDigit2(1043) = }')
# # getDigit2(1043) = 4

