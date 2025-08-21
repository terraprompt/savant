"""Main application module for Savant."""

import os
import sys
from typing import Optional
import click
from flask import Flask, render_template, request, jsonify
from savant.solver import solve_optimization_problem, ProblemSolverResult

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY') or 'your-secret-key-here'
    
    @app.route('/')
    def index():
        """Render the main dashboard page."""
        return render_template('index.html')
    
    @app.route('/solve', methods=['POST'])
    def solve():
        """Solve an optimization problem."""
        problem_description = request.form['problem_description']
        additional_info = request.form.get('additional_info', '')
        
        try:
            result = solve_optimization_problem(problem_description, additional_info)
            
            if result.needs_more_info:
                return jsonify({
                    'needs_more_info': True,
                    'questions': result.questions,
                    'log': 'Please provide more information to solve this problem.'
                })
            elif result.error:
                return jsonify({
                    'error': result.error,
                    'log': f'Error occurred while solving: {result.error}'
                }), 400
            else:
                return jsonify({
                    'solution': result.solution,
                    'log': 'Problem solved successfully.'
                })
        except Exception as e:
            return jsonify({
                'error': str(e),
                'log': f'Error occurred while solving: {str(e)}'
            }), 400
    
    return app

@click.command()
@click.option('--problem', '-p', help='Optimization problem description')
@click.option('--web', '-w', is_flag=True, help='Run web interface')
@click.option('--port', default=5000, help='Port for web interface')
def main(problem: Optional[str], web: bool, port: int):
    """Savant CLI - An intelligent optimization problem solver.
    
    Examples:
      savant -p "Minimize x+y subject to x>=0, y>=0, x+y<=10"
      savant --web
    """
    if web:
        # Run web interface
        app = create_app()
        app.run(host='0.0.0.0', port=port, debug=True)
    elif problem:
        # Solve problem from command line
        current_problem = problem
        additional_info = ""
        
        while True:
            result = solve_optimization_problem(current_problem, additional_info)
            
            if result.needs_more_info:
                click.echo("I need more information to solve this problem:")
                for i, question in enumerate(result.questions, 1):
                    click.echo(f"{i}. {question}")
                
                # Ask user for additional information
                user_input = click.prompt("Please provide the missing information", type=str)
                additional_info = user_input
                # We'll try again with the additional info
                continue
            elif result.error:
                click.echo(f"Error: {result.error}", err=True)
                sys.exit(1)
            else:
                click.echo("Solution found:")
                click.echo(result.solution)
                break
    else:
        # Show help if no options provided
        click.echo("Savant: An intelligent optimization problem solver")
        click.echo("Use --help for more information")

if __name__ == '__main__':
    main()