"""Tests for the CLI interface."""

import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from savanty.cli import main
from savanty.solver import ProblemSolverResult


def test_cli_help():
    """Test that the CLI provides help text."""
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'Usage:' in result.output
    assert 'Savanty CLI' in result.output


def test_cli_without_args():
    """Test that the CLI shows basic info when run without args."""
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    assert 'Savanty:' in result.output


@patch('savanty.cli.solve_optimization_problem')
def test_cli_with_problem(mock_solve):
    """Test that the CLI can solve a problem."""
    # Mock the solver to return a successful result
    mock_result = ProblemSolverResult(solution="Solution found")
    mock_solve.return_value = mock_result
    
    runner = CliRunner()
    result = runner.invoke(main, ['-p', 'Minimize x+y subject to x>=0, y>=0'])
    
    assert result.exit_code == 0
    assert 'Solution found' in result.output
    mock_solve.assert_called_once_with('Minimize x+y subject to x>=0, y>=0', '')


@patch('savanty.cli.solve_optimization_problem')
def test_cli_with_invalid_problem(mock_solve):
    """Test that the CLI handles invalid problems gracefully."""
    # Mock the solver to return an error result
    mock_result = ProblemSolverResult(error="Invalid problem")
    mock_solve.return_value = mock_result
    
    runner = CliRunner()
    result = runner.invoke(main, ['-p', 'This is not a valid optimization problem'])
    
    assert result.exit_code == 1
    assert 'Error:' in result.output


@patch('savanty.cli.solve_optimization_problem')\ndef test_cli_with_needs_info_problem(mock_solve):\n    \"\"\"Test that the CLI handles problems that need more info.\"\"\"\n    # Mock the solver to first return needs more info, then a solution\n    mock_result1 = ProblemSolverResult(needs_more_info=True, questions=[\"What is the objective?\"])\n    mock_result2 = ProblemSolverResult(solution=\"Solution found\")\n    \n    mock_solve.side_effect = [mock_result1, mock_result2]\n    \n    runner = CliRunner()\n    result = runner.invoke(main, ['-p', 'Solve something'], input='Minimize x\\n')\n    \n    assert result.exit_code == 0\n    assert 'I need more information' in result.output\n    assert 'Solution found' in result.output\n    assert mock_solve.call_count == 2