"""
Problem: Basic Calculator II (LeetCode 227)

Evaluate a string expression s containing:
- Non-negative integers
- Operators: '+', '-', '*', '/'
- No parentheses
- Spaces may appear

Rules:
- Multiplication (*) and division (/) have higher precedence than addition (+) and subtraction (-)
- Division should truncate toward zero

Example:
    "3+2*2" => 7
    " 3/2 " => 1
    " 3+5 / 2 " => 5
"""

# ----------------------------
# Intuition:
# ----------------------------
# Use a two-variable approach (O(1) space) instead of a stack.
# 1. Maintain 'last' to store the last number that may be multiplied or divided.
# 2. Maintain 'result' as the sum of numbers fixed by addition/subtraction.
# 3. Iterate through the string, building numbers and applying the previous operator:
#    - '+' or '-' commits 'last' to 'result' and starts a new 'last' number
#    - '*' or '/' updates 'last' immediately
# 4. At the end, add the last pending number to 'result'.

# ----------------------------
# Time & Space Complexity:
# ----------------------------
# Time: O(n), single pass through the string
# Space: O(1), constant space (no stack needed)

from typing import List

def calculate(s: str) -> int:
    s = s.replace(" ", "")  # remove spaces
    n = len(s)
    if n == 0:
        return 0

    result = 0
    last = 0
    num = 0
    sign = '+'

    for i, c in enumerate(s):
        if c.isdigit():
            num = num * 10 + int(c)
        if c in "+-*/" or i == n - 1:
            if sign == '+':
                result += last
                last = num
            elif sign == '-':
                result += last
                last = -num
            elif sign == '*':
                last = last * num
            elif sign == '/':
                last = int(last / num)  # truncate toward zero
            sign = c
            num = 0

    result += last
    return result

# ----------------------------
# Test Cases
# ----------------------------
if __name__ == "__main__":
    test_cases = [
        ("3+2*2", 7),
        (" 3/2 ", 1),
        (" 3+5 / 2 ", 5),
        ("14-3/2", 13),
        ("100", 100),
        ("0-2147483647", -2147483647),
        ("2*3+4", 10),
        ("2+3*4", 14),
        ("10+2*6", 22),
        ("100/10*2+3", 23),
    ]

    for i, (expr, expected) in enumerate(test_cases):
        result = calculate(expr)
        print(f"Test case {i+1}: '{expr}' = {result} | Expected: {expected} | {'PASS' if result == expected else 'FAIL'}")
