# Savant AI: Optimization Problem Solver Dashboard

Savant AI is an intelligent web application that leverages the power of Large Language Models (LLMs) to parse, solve, and visualize optimization problems. It provides an intuitive interface for users to input problem descriptions in natural language, generates the corresponding code, and solves the optimization problems using Answer Set Programming (ASP).

## Features

- **Natural Language Processing**: Utilizes GPT-4 to parse optimization problem descriptions.
- **Code Generation**: Automatically generates Clorm predicates and ASP programs.
- **Problem Solving**: Implements optimization problem solving using Clingo.
- **User Authentication**: Supports multiple users with individual workspaces.
- **Problem Management**: Allows saving, loading, and updating of problem descriptions.
- **Syntax Highlighting**: Uses Prism.js for better code readability.
- **Real-time Updates**: Leverages HTMX for seamless user interactions.
- **Responsive Design**: Utilizes Tailwind CSS for a clean, responsive interface.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- pip (Python package manager)
- An OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/savant-ai.git
   cd savant-ai
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   - Create a `.env` file in the root directory
   - Add the following lines:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     FLASK_SECRET_KEY=your_secret_key_here
     ```

## Usage

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Register for a new account or log in if you already have one.

4. On the dashboard:
   - Input your optimization problem description in natural language.
   - View the generated Clorm predicates and ASP program.
   - Solve the problem and view the results.
   - Save and load problem descriptions as needed.

## Project Structure

```
savant-ai/
├── app.py
├── requirements.txt
├── .env
├── README.md
└── templates/
    ├── index.html
    ├── login.html
    └── register.html
```

## Contributing

Contributions to Savant AI are welcome! Please follow these steps:

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

Your Name - your.email@example.com

Project Link: [https://github.com/your-username/savant-ai](https://github.com/your-username/savant-ai)

## Acknowledgements

- [OpenAI](https://openai.com/) for providing the GPT-4 API
- [Clingo](https://potassco.org/clingo/) for the ASP solver
- [Clorm](https://github.com/potassco/clorm) for Object-Relational Mapping with Clingo
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [HTMX](https://htmx.org/) for dynamic HTML capabilities
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [Prism.js](https://prismjs.com/) for syntax highlighting