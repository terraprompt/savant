import openai
from clorm import Predicate, ConstantField, IntegerField
from clorm.clingo import Control

# Set up your OpenAI API key
openai.api_key = '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'

def query_gpt4(prompt):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps parse optimization problems and generate Python code."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def parse_problem(description):
    prompt = f"""
    Parse the following optimization problem description and extract the relevant information:
    {description}

    Return a Python dictionary with the following structure, do not add anything else to the reply generated including markup:
    {{
        "predicates": [list of predicates with their fields(name and type)],
        "facts": [list of facts],
        "constraints": [list of constraints],
        "optimize": "maximize or minimize statement"
    }}
    """
    llm_result = query_gpt4(prompt)
    result = eval(llm_result)
    return result

def generate_clorm_predicates(predicates):
    predicate_code = ""
    for pred in predicates:
        fields = ", ".join([f"{field} = {type}" for field, type in pred['fields'].items()])
        predicate_code += f"""
class {pred['name']}(Predicate):
    {fields}
"""
    return predicate_code

def generate_asp_program(problem_info):
    constraints = "\n".join(problem_info['constraints'])
    optimize = problem_info['optimize']
    
    return f"""
{constraints}

{optimize}

#show.
"""

def solve_optimization_problem(problem_description):
    # Step 1: Parse the problem using GPT-4
    problem_info = parse_problem(problem_description)
    
    # Step 2: Generate Clorm predicates
    predicate_code = generate_clorm_predicates(problem_info['predicates'])
    exec(predicate_code, globals())
    
    # Step 3: Construct the ASP program
    asp_program = generate_asp_program(problem_info)
    
    # Step 4: Solve the optimization problem
    ctrl = Control(unifier=[globals()[pred['name']] for pred in problem_info['predicates']])
    
    # Add facts
    for fact in problem_info['facts']:
        predicate_name, *args = fact.split('(')
        args = args[0].rstrip(')').split(',')
        predicate_class = globals()[predicate_name]
        ctrl.add_fact(predicate_class(*args))
    
    ctrl.add_program(asp_program)
    
    solution = None
    with ctrl.solve(yield_=True) as sh:
        for model in sh:
            solution = model.facts(atoms=True)
    
    return solution

if __name__ == '__main__':
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
    
    solution = solve_optimization_problem(problem_description)
    
    if solution:
        print("Optimal schedule:")
        for fact in solution:
            print(fact)
    else:
        print("No solution found")