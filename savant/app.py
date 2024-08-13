from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from clorm import Predicate, ConstantField, IntegerField
from clorm.clingo import Control
import time
import os
from solver import query_gpt4, parse_problem, generate_clorm_predicates, generate_asp_program, solve_optimization_problem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///savant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    problems = db.relationship('Problem', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
@login_required
def index():
    problems = Problem.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', problems=problems)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(username=request.form['username'])
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/update_problem', methods=['POST'])
@login_required
def update_problem():
    problem_description = request.form['problem_description']
    problem_id = request.form.get('problem_id')

    if problem_id:
        problem = Problem.query.get(problem_id)
        if problem and problem.user_id == current_user.id:
            problem.description = problem_description
    else:
        problem = Problem(description=problem_description, user_id=current_user.id)
        db.session.add(problem)
    
    db.session.commit()

    try:
        problem_info = parse_problem(problem_description)
        predicate_code = generate_clorm_predicates(problem_info['predicates'])
        asp_program = generate_asp_program(problem_info)
        return jsonify({
            'predicates': predicate_code,
            'asp_program': asp_program,
            'log': 'Problem parsed and code generated successfully.',
            'problem_id': problem.id
        })
    except Exception as e:
        print("""Error """,str(e))
        return jsonify({
            'error': str(e),
            'log': f'Error occurred: {str(e)}'
        }), 400

@app.route('/solve_problem', methods=['POST'])
@login_required
def solve_problem():
    problem_description = request.form['problem_description']
    try:
        solution = solve_optimization_problem(problem_description)
        return jsonify({
            'solution': str(solution),
            'log': 'Problem solved successfully.'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'log': f'Error occurred while solving: {str(e)}'
        }), 400

@app.route('/load_problem/<int:problem_id>')
@login_required
def load_problem(problem_id):
    problem = Problem.query.get(problem_id)
    if problem and problem.user_id == current_user.id:
        return jsonify({
            'description': problem.description
        })
    return jsonify({'error': 'Problem not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
