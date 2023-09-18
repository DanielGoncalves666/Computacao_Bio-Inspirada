import numpy as np
import re
import time
import random

def knapsack_greedy(solution, value, weight, capacity):
    remaining_capacity = capacity
    total_value = 0
    
    for item in solution:
        if weight[item] <= remaining_capacity:
            total_value += value[item]
            remaining_capacity -= weight[item]
    
    return total_value

def construct_greedy_solution(value, weight, capacity, alpha):
    n = len(value)
    sorted_items = sorted(range(n), key=lambda x: value[x] / weight[x], reverse=True)
    
    solution = []
    remaining_capacity = capacity
    
    for item in sorted_items:
        if weight[item] <= remaining_capacity:
            if random.random() <= alpha:
                solution.append(item)
                remaining_capacity -= weight[item]
    
    return solution

def grasp_knapsack(value, weight, capacity, max_iterations, alpha):
    best_solution = []
    best_value = 0
    
    for _ in range(max_iterations):
        candidate_solution = construct_greedy_solution(value, weight, capacity, alpha)
        candidate_value = knapsack_greedy(candidate_solution, value, weight, capacity)
        
        if candidate_value > best_value:
            best_solution = candidate_solution
            best_value = candidate_value
    
    return best_solution, best_value

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
    
    return n, value, weight, capacity

def main():
    #random.seed(42)
    max_iterations = 100
    alpha = 0.3
    
    output_max_values = []

    vet = [5 for i in range(10)]

    for iterator in vet:
        start_time = time.time()
        input_file_path = f"input/input{iterator}.in"
        n, value, weight, capacity = solve_knapsack_problem(input_file_path)
        solution, max_value = grasp_knapsack(value, weight, capacity, max_iterations, alpha)
        output_max_values.append(max_value)
        execution_time = time.time() - start_time
        output_line = f"{max_value} {execution_time}\n"
        
        with open("output/grasp.out", "a+") as output_file:
            output_file.write(output_line)

if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print(f"Execution time: {execution_time} seconds")
