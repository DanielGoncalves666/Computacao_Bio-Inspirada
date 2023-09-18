import numpy as np
import re
import time

def knapsack(size, value, weight, capacity, dp):
    if size == 0 or capacity == 0:
        return 0
    if dp[size - 1][capacity] != -1:
        return dp[size - 1][capacity]
    if weight[size - 1] > capacity:
        dp[size - 1][capacity] = knapsack(size - 1, value, weight, capacity, dp)
        return dp[size - 1][capacity]
    a = value[size - 1] + knapsack(size - 1, value, weight, capacity - weight[size - 1], dp)
    b = knapsack(size - 1, value, weight, capacity, dp)
    dp[size - 1][capacity] = max(a, b)
    return dp[size - 1][capacity]

def solve_knapsack_problem(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    n = int(lines[0].strip())
    capacity = int(lines[-1].strip())
    
    id, value, weight = [], [], []
    for line in lines[1:-1]:
        numbers = re.findall(r"[0-9]+", line)
        id.append(int(numbers[0]) - 1)
        value.append(int(numbers[1]))
        weight.append(int(numbers[2]))
    
    dp = np.full((n, capacity + 1), -1, dtype=int)
    max_value = knapsack(n, value, weight, capacity, dp)
    return max_value

def main():
    output_max_values = []

    vet = [5 for i in range(10)]

    for iterator in vet:
        start_time = time.time()
        input_file_path = f"input/input{iterator}.in"
        max_value = solve_knapsack_problem(input_file_path)
        execution_time = time.time() - start_time
        output_max_values.append(max_value)
        output_line = f"{max_value} {execution_time}\n"
        
        with open("output/dynamic.out", "a+") as output_file:
            output_file.write(output_line)

if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print(f"Execution time: {execution_time} seconds")
