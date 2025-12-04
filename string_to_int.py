"""
LeetCode 8 — String to Integer (atoi)
-------------------------------------

🧩 Problem:
Implement the function myAtoi(string s), which converts a string to a 32-bit signed integer.

Rules:
  1. Ignore leading whitespace.
  2. Detect an optional '+' or '-' sign.
  3. Parse consecutive digits and convert them to an integer.
  4. Stop parsing when encountering a non-digit.
  5. Clamp the result within the 32-bit signed integer range:
        [-2^31, 2^31 - 1] → [-2147483648, 2147483647]
  6. If no valid digits are found, return 0.

🧠 Intuition:
This problem is about simulating a state machine:
  - Skip whitespace
  - Handle sign
  - Parse digits
  - Stop at invalid characters
  - Clamp result if overflow occurs

Instead of using complex parsing logic, we can solve this in a single linear pass.

⏱️ Time Complexity: O(n)
🧮 Space Complexity: O(1)
Where n = length of the input string.
"""

class Solution:
    def myAtoi(self, s: str) -> int:
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31

        i, n = 0, len(s)
        res, sign = 0, 1

        # 1️⃣ Skip leading whitespace
        while i < n and s[i] == ' ':
            i += 1

        # 2️⃣ Handle sign
        if i < n and (s[i] == '+' or s[i] == '-'):
            sign = -1 if s[i] == '-' else 1
            i += 1

        # 3️⃣ Parse digits and build the integer
        while i < n and s[i].isdigit():
            digit = int(s[i])

            # 4️⃣ Check for overflow before it happens
            if res > (INT_MAX - digit) // 10:
                return INT_MAX if sign == 1 else INT_MIN

            res = res * 10 + digit
            i += 1

        # 5️⃣ Apply sign and return
        return res * sign


# 🧪 Test Cases
if __name__ == "__main__":
    s = Solution()

    tests = [
        ("42", 42),
        ("   -42", -42),
        ("4193 with words", 4193),
        ("words and 987", 0),
        ("-91283472332", -2147483648),
        ("+1", 1),
        ("00000-42a1234", 0),
        ("", 0),
        ("   +0 123", 0),
        ("21474836460", 2147483647)
    ]

    for i, (input_str, expected) in enumerate(tests, 1):
        result = s.myAtoi(input_str)
        print(f"Test {i}: Input='{input_str}' | Expected={expected} | Got={result}")
