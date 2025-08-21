#!/usr/bin/env python3
"""
Example usage of the Savant optimization solver with proper environment variable handling.
"""

import os
from savant.solver import solve_optimization_problem

def main():
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY environment variable not set!")
        print("Set it with: export OPENAI_API_KEY=your_openai_api_key_here")
        return
    
    # Example 1: Simple linear optimization
    print("Example 1: Simple linear optimization")
    problem1 = "Minimize x+y subject to x>=0, y>=0, x+y<=10"
    result1 = solve_optimization_problem(problem1)
    
    if result1.needs_more_info:
        print("Please provide more information:")
        for question in result1.questions:
            print(f"- {question}")
    elif result1.error:
        print(f"Error: {result1.error}")
    else:
        print(f"Solution: {result1.solution}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Task scheduling problem
    print("Example 2: Task scheduling problem")
    problem2 = """
    We have a task scheduling problem. Each task has a name, duration, and priority.
    We need to schedule tasks within a maximum time of 10 units.
    Tasks cannot overlap.
    We want to maximize the total priority of scheduled tasks.

    Available tasks are:
    Task1: duration 3, priority 5
    Task2: duration 2, priority 3
    Task3: duration 4, priority 7
    Task4: duration 1, priority 2
    """
    result2 = solve_optimization_problem(problem2)
    
    if result2.needs_more_info:
        print("Please provide more information:")
        for question in result2.questions:
            print(f"- {question}")
    elif result2.error:
        print(f"Error: {result2.error}")
    else:
        print(f"Solution: {result2.solution}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Incomplete problem (should ask for more info)
    print("Example 3: Incomplete problem (should ask for more info)")
    problem3 = "Solve a scheduling problem"
    result3 = solve_optimization_problem(problem3)
    
    if result3.needs_more_info:
        print("Needs more information (this is expected):")
        for question in result3.questions:
            print(f"- {question}")
    elif result3.error:
        print(f"Error: {result3.error}")
    else:
        print(f"Solution: {result3.solution}")

if __name__ == "__main__":
    main()