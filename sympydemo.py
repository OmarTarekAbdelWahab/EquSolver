import sympy
from sympy import *
import math

x, y = symbols("x, y")

# expr = x**3+cos(x)

# derivative = diff(expr)
# print(derivative)
# print(derivative.subs(x, 0))
# print(solve(x**3-cos(y), x, dict=True))
# print(solve(y**3-cos(x), x, dict=True))

#expr = x**2-2*x-3
# print(solve(x**2-2*y-3, y, dict=True))
# print(solve(y**2-2*x-3, y, dict=True))
# n = 100000
# integral = 0
# a = 0
# b = math.pi
# for i in range(1,n+1):
#     integral += sin(a+i*((b-a)/(2*n)))

# integral *= ((b-a)/n)

# print(integral)

n = 1
delta = math.pi
s = 0
while(n<=9):
    next_sum = 0
    for i in range(1, 2**(n-1)+1):
        next_sum += sin((2*i-1)*delta/(2**n))
    s = 0.5*s+(delta/(2**n)) * next_sum
    n += 1

print(s)

