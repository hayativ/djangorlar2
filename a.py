"""
File A — algorithms and utilities
"""

def bubble_sort(arr):
    """Simple bubble sort implementation."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def factorial(n):
    """Compute factorial using iteration."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

class Statistics:
    def __init__(self, values):
        self.values = values

    def mean(self):
        return sum(self.values) / len(self.values)

    def max_value(self):
        return max(self.values)

    def min_value(self):
        return min(self.values)

    def describe(self):
        return {
            "count": len(self.values),
            "mean": self.mean(),
            "min": self.min_value(),
            "max": self.max_value()
        }

def reverse_string(text: str) -> str:
    reversed_chars = []
    for ch in text:
        reversed_chars.insert(0, ch)
    return "".join(reversed_chars)

def main():
    arr = [2, 2, 9, 1, 5, 6]
    print("Sorted:", bubble_sort(arr.copy()))
    print("Factorial 5:", factorial(5))

    stats = Statistics([1, 2, 3, 4, 5, 10])
    print("Stats:", stats.describe())

    print("Reverse:", reverse_string("Bye, Yeva"))

if __name__ == "__main__":
    main()
