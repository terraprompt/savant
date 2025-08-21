# Savant: Intelligent Optimization Problem Solver

Savant is an intelligent Python library that leverages the power of Large Language Models (LLMs) and DSPy to parse, solve, and visualize optimization problems. It provides both a command-line interface and a web interface for users to input problem descriptions in natural language and automatically generates solutions using Answer Set Programming (ASP).

## Features

- **Natural Language Processing**: Utilizes GPT-4 and DSPy for robust optimization problem parsing.
- **Code Generation**: Automatically generates Clorm predicates and ASP programs.
- **Problem Validation**: Validates if a problem can be solved with ASP before attempting to solve it.
- **Interactive Gap Filling**: Asks for additional information when problem descriptions are incomplete.
- **Problem Solving**: Implements optimization problem solving using Clingo.
- **Dual Interface**: Command-line interface for direct usage and web interface for interactive solving.
- **Modern Python Package**: Installable via pip with proper CLI integration.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8+
- An OpenAI API key

## Installation

Install Savant directly from PyPI:

```bash
pip install savant
```

Or install from source:

```bash
git clone https://github.com/your-username/savant.git
cd savant
pip install .
```

## Setup

Set up your environment variables:
- Set your OpenAI API key as an environment variable:
  ```bash
  export OPENAI_API_KEY=your_openai_api_key_here
  ```
- (Optional) Set a custom Flask secret key:
  ```bash
  export FLASK_SECRET_KEY=your_flask_secret_key_here
  ```

For temporary usage without setting environment variables:
```bash
OPENAI_API_KEY=your_openai_api_key_here savant -p "Minimize x+y subject to x>=0, y>=0"
```

## Usage

### Command Line Interface

Solve optimization problems directly from the command line:

```bash
# Solve a problem directly
savant -p "We have a task scheduling problem. Each task has a name, duration, and priority. We need to schedule tasks within a maximum time of 10 units. Tasks cannot overlap. We want to maximize the total priority of scheduled tasks. Available tasks are: Task1: duration 3, priority 5; Task2: duration 2, priority 3; Task3: duration 4, priority 7; Task4: duration 1, priority 2."

# Run the web interface
savant --web
```

### Interactive Problem Solving

When a problem description is incomplete, Savant will ask for additional information:

```bash
savant -p "Solve a scheduling problem"
# Savant will ask: "What are the tasks and their properties?"
# You can then provide: "Task1: duration 3, priority 5; Task2: duration 2, priority 3"
```

### Web Interface

Run the web interface to solve problems interactively:

```bash
savant --web --port 5000
```

Then open your browser to `http://localhost:5000` to access the web interface. The web interface also supports interactive gap filling - if your problem description is incomplete, Savant will ask for additional information directly in the web interface.

### Python API

Use Savant directly in your Python code:

```python
from savant.solver import solve_optimization_problem

problem_description = """
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

result = solve_optimization_problem(problem_description)

if result.needs_more_info:
    print("Please provide more information:")
    for question in result.questions:
        print(f"- {question}")
elif result.error:
    print(f"Error: {result.error}")
else:
    print(f"Solution: {result.solution}")
```

## Use Cases

### 1. Task Scheduling Problem

```bash
savant -p "Schedule tasks to maximize priority. TaskA (duration 3, priority 5), TaskB (duration 2, priority 4), TaskC (duration 4, priority 7). Time limit is 8 units. Tasks cannot overlap."
```

### 2. Resource Allocation

```bash
savant -p "Allocate 3 projects to 2 teams. Project1 (value 100, requires 2 team members), Project2 (value 150, requires 3 team members), Project3 (value 80, requires 1 team member). Total team members available: 4. Maximize total value."
```

### 3. Knapsack Problem

```bash
savant -p "Knapsack with capacity 10. Item1 (weight 5, value 10), Item2 (weight 4, value 7), Item3 (weight 6, value 12), Item4 (weight 2, value 3). Maximize value without exceeding capacity."
```

### 4. Graph Coloring

```bash
savant -p "Color a graph with 4 nodes and edges: (1,2), (2,3), (3,4), (1,4). Use minimum number of colors such that adjacent nodes have different colors."
```

### 5. Sudoku Solver

```bash
savant -p "Solve a 4x4 Sudoku puzzle. Given: position (1,1) = 1, position (1,3) = 2, position (2,2) = 3, position (3,1) = 4. Find values for all positions respecting Sudoku rules."
```

## Project Structure

```
savant/
├── savant/
│   ├── __init__.py
│   ├── cli.py
│   ├── solver.py
│   ├── dspy_modules.py
│   └── templates/
│       └── index.html
├── tests/
├── pyproject.toml
├── README.md
└── LICENSE
```

## Contributing

Contributions to Savant are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the original branch: `git push origin feature-branch-name`.
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, please contact the maintainer:

Dipankar Sarkar - me@dipankar.name

Project Link: [https://github.com/your-username/savant](https://github.com/your-username/savant)

## Acknowledgements

- [OpenAI](https://openai.com/) for providing the GPT-4 API
- [DSPy](https://github.com/stanfordnlp/dspy) for LLM prompting and optimization
- [Clingo](https://potassco.org/clingo/) for the ASP solver
- [Clorm](https://github.com/potassco/clorm) for Object-Relational Mapping with Clingo
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [HTMX](https://htmx.org/) for dynamic HTML capabilities
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [Click](https://click.palletsprojects.com/) for CLI creation