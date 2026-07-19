"""
🏙️ Problem: Weighted Random City Picker

Given a list of city names and their corresponding populations, 
write a program that outputs a city name where the probability 
of selecting a city is proportional to its population.

Example:
    cities = ["New York", "Los Angeles", "Chicago"]
    populations = [8, 4, 2]
    Total population = 14

    Probabilities:
      - New York → 8/14
      - Los Angeles → 4/14
      - Chicago → 2/14

🧠 Intuition:
We treat each city's population as a range on a number line.
If we randomly choose an integer r ∈ [1, total_population],
the city whose cumulative population range contains r is selected.

For example:
    Prefix sums: [8, 12, 14]
    Random number r = 10 → falls in range (8, 12] → "Los Angeles".

We use binary search to efficiently find which range r falls into.
"""

import random


class WeightedRandomCityPicker:
    def __init__(self, cities, populations):
        """
        Precompute prefix sums for weighted selection.

        Args:
            cities (List[str]): List of city names
            populations (List[int]): Corresponding populations
        """
        self.cities = cities
        self.prefix = []
        self.total = 0

        for pop in populations:
            self.total += pop
            self.prefix.append(self.total)

    def pick_city(self):
        """
        Randomly pick a city proportional to its population.

        Returns:
            str: Selected city name
        """
        # Pick a random number between 1 and total population
        r = random.randint(1, self.total)

        # Manual binary search for the city index
        left, right = 0, len(self.prefix) - 1

        while left < right:
            mid = (left + right) // 2
            if self.prefix[mid] < r:
                left = mid + 1
            else:
                right = mid

        return self.cities[left]


# 🧪 Test Cases
if __name__ == "__main__":
    picker = WeightedRandomCityPicker(
        ["New York", "Los Angeles", "Chicago"],
        [8, 4, 2]
    )

    print("🎯 Random selections (expect more 'New York'):")
    for _ in range(14):
        print(picker.pick_city())

"""
⏱️ Complexity:
    • Preprocessing: O(n) for prefix sum construction
    • Pick Operation: O(log n) via binary search
    • Space: O(n)

🧩 Key Takeaways:
    - Prefix sums map probabilities to numeric intervals
    - Binary search finds which interval a random value belongs to
    - This approach scales well even for large datasets
"""
