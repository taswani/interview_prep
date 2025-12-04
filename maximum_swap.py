"""
💎 LeetCode 670 — Maximum Swap

📘 Problem:
Given a non-negative integer `num`, you may swap two digits at most once 
to get the maximum possible number. Return the maximum number.

🧩 Examples:
    Input:  num = 2736
    Output: 7236
    Explanation: Swap the 2 and the 7.

    Input:  num = 9973
    Output: 9973
    Explanation: No swap can make it larger.

------------------------------------------------------

💡 Intuition:
We want the largest number possible after at most one swap.
To achieve this:
    1. Traverse digits from left to right.
    2. For each digit, check if a larger digit appears later.
    3. If so, swap it with the **rightmost** occurrence of the largest digit.
    4. Return immediately after one swap.

------------------------------------------------------

🧠 Example Walkthrough:
    num = 2736
    digits = [2, 7, 3, 6]

    i = 0 → digit = 2
      Largest digit to the right = 7 (index 1)
      ✅ Swap → [7, 2, 3, 6] → 7236

    Return 7236

------------------------------------------------------

⚙️ Algorithm:
1️⃣ Convert num → list of digits.
2️⃣ Create a map of the last index of each digit (0–9).
3️⃣ Iterate digits:
      For each digit, check if any higher digit exists later.
      If found, swap and return result.
4️⃣ If no swap possible, return original number.

------------------------------------------------------

⏱️ Complexity:
    Time:  O(n) — traverse digits + constant-range checks (0–9)
    Space: O(1) — only a 10-element dictionary

------------------------------------------------------
"""

class Solution:
    def maximumSwap(self, num: int) -> int:
        digits = list(str(num))
        last = {int(d): i for i, d in enumerate(digits)}  # Last index of each digit
        
        for i, d in enumerate(digits):
            curr = int(d)
            # Check for a larger digit appearing later
            for higher in range(9, curr, -1):
                if higher in last and last[higher] > i:
                    # Swap with the rightmost larger digit
                    j = last[higher]
                    digits[i], digits[j] = digits[j], digits[i]
                    return int("".join(digits))
        
        return num  # Already maxed out number


# ------------------------------------------------------
# 🧪 Test Cases
# ------------------------------------------------------
if __name__ == "__main__":
    sol = Solution()

    tests = [
        (2736, 7236),
        (9973, 9973),
        (98368, 98863),
        (109090, 909010),
        (12345, 52341),
        (321, 321),
        (1993, 9913),
    ]

    for i, (num, expected) in enumerate(tests, 1):
        result = sol.maximumSwap(num)
        print(f"Test {i}: num={num} → {result} {'✅' if result == expected else f'❌ (expected {expected})'}")
