from typing import List

def min_roundtrip_cost(D: List[int], R: List[int]) -> int:
    if not D or not R or len(D) != len(R):
        raise ValueError("Arrays must be non-empty and same length")
    
    min_departure = float('inf')
    min_round_trip = float('inf')

    for idx in range(len(D)):
        min_departure = min(D[idx], min_departure)

        min_round_trip = min(min_departure + R[idx], min_round_trip)
    
    return min_round_trip

# ----------------------------
# Test Cases
# ----------------------------
if __name__ == "__main__":
    D = [10, 8, 9, 11, 7]
    R = [8, 8, 10, 7, 9]
    print(min_roundtrip_cost(D, R))  # Expected: 15 (8+7)

    D = [5, 3, 4]
    R = [4, 5, 2]
    print(min_roundtrip_cost(D, R))  # Expected: 5 (3+2)

    D = [10]
    R = [10]
    print(min_roundtrip_cost(D, R))  # Expected: 20
