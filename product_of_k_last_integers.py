"""
LeetCode 1352: Product of the Last K Numbers

Problem Description:
--------------------
Design a class that supports the following operations:

1. add(int num) - Adds the number `num` to the stream.
2. getProduct(int k) - Returns the product of the last `k` numbers in the stream.

Notes:
- If any of the last k numbers is 0, the product is 0.
- It is guaranteed that getProduct will be called with k ≤ the number of elements added so far.
- Like prefix sum algorithm adapted for multiplication

Example:
--------
Input:
    ["ProductOfNumbers","add","add","add","add","add","getProduct","getProduct","getProduct","add","getProduct"]
    [[],[3],[0],[2],[5],[4],[2],[3],[4],[8],[2]]
Output:
    [null,null,null,null,null,null,20,40,0,null,32]

Explanation:
    ProductOfNumbers productOfNumbers = new ProductOfNumbers();
    productOfNumbers.add(3);        // [3]
    productOfNumbers.add(0);        // [3,0]
    productOfNumbers.add(2);        // [3,0,2]
    productOfNumbers.add(5);        // [3,0,2,5]
    productOfNumbers.add(4);        // [3,0,2,5,4]
    productOfNumbers.getProduct(2); // 20 (5*4)
    productOfNumbers.getProduct(3); // 40 (2*5*4)
    productOfNumbers.getProduct(4); // 0 (includes zero)
    productOfNumbers.add(8);        // [3,0,2,5,4,8]
    productOfNumbers.getProduct(2); // 32 (4*8)
"""

# ---------------- Solution ----------------

class ProductOfNumbers:
    def __init__(self):
        # Store prefix products; start with 1 for easy multiplication
        self.prefix_products = [1]

    def add(self, num: int) -> None:
        if num == 0:
            # Reset prefix products if zero appears
            self.prefix_products = [1]
        else:
            # Multiply last product by current number
            self.prefix_products.append(self.prefix_products[-1] * num)

    def getProduct(self, k: int) -> int:
        if k >= len(self.prefix_products):
            # Last k numbers include a zero
            return 0
        # Divide the last prefix product by the prefix product k steps back
        return self.prefix_products[-1] // self.prefix_products[-k-1]


# ---------------- Time & Space Complexity ----------------
# add(num): O(1) per insertion
# getProduct(k): O(1) per query
# Space complexity: O(n) for storing prefix products since last zero
# ---------------------------------------------------------

# ---------------- Test Cases ----------------
if __name__ == "__main__":
    # Test Case 1: Example from problem
    p = ProductOfNumbers()
    p.add(3)
    p.add(0)
    p.add(2)
    p.add(5)
    p.add(4)
    print(p.getProduct(2))  # Expected 20 (5*4)
    print(p.getProduct(3))  # Expected 40 (2*5*4)
    print(p.getProduct(4))  # Expected 0  (includes zero)

    # Test Case 2: Additional operations
    p.add(8)
    print(p.getProduct(2))  # Expected 32 (4*8)
    print(p.getProduct(3))  # Expected 160 (5*4*8)

    # Test Case 3: Only one element
    p2 = ProductOfNumbers()
    p2.add(7)
    print(p2.getProduct(1))  # Expected 7

    # Test Case 4: Multiple zeros
    p2.add(0)
    p2.add(2)
    p2.add(3)
    print(p2.getProduct(2))  # Expected 6 (2*3)
    print(p2.getProduct(3))  # Expected 0 (includes zero)
