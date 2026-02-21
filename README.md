🚀 AI Code Reviewer & Quality Assistant

An AI-powered tool that analyzes Python code, detects quality issues, and provides structured feedback using static analysis and Large Language Models (LLMs).

It supports both CLI usage and an interactive Streamlit web interface.

📌 Overview

The AI Code Reviewer & Quality Assistant helps developers:

🔍 Detect code quality issues

📄 Identify missing docstrings and type hints

🧠 Get AI-generated improvement suggestions

📊 View severity-based structured reports

🖥️ Use either CLI or Web UI

It combines rule-based static analysis with optional AI-powered contextual review.

🏗️ Project Structure
ai_code_reviewer/
│
├── cli/
│   └── main.py
│
├── core/
│   ├── analyzer.py
│   ├── ai_reviewer.py
│   ├── rules.py
│   ├── reporter.py
│   └── utils.py
│
├── ui/
│   └── streamlit_app.py
│
├── demo.py
├── requirements.txt
└── README.md
⚙️ Features
🔎 Static Code Analysis

Missing docstrings detection

Missing type hints

Naming convention checks

Basic code smell detection

Function complexity checks

Severity categorization (Critical, Warning, Info)

🤖 AI Review Mode

Context-aware improvement suggestions

Refactoring recommendations

Readability improvements

Logical improvement suggestions

📊 Structured Reporting

Findings grouped by:

❌ Critical

⚠️ Warning

ℹ️ Info

🖥️ CLI Usage
Static Review
python -m ai_code_reviewer.cli.main review demo.py
AI-Enhanced Review
python -m ai_code_reviewer.cli.main review demo.py --ai
Example Output
Summary:
Critical: 0
Warnings: 1
Info: 4

[WARNING] demo.py:17 → Invoice lacks a docstring.
[INFO] demo.py:1 → price in process_order lacks type hint.
🌐 Streamlit Web UI

Run:

streamlit run ai_code_reviewer/ui/streamlit_app.py

Features:

File upload support

Enable/Disable AI review

Severity filtering

Structured findings display

Summary metrics dashboard

📦 Installation
1. Clone the Repository
git clone <your-repo-url>
cd ai_code_reviewer
2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
3. Install Dependencies
pip install -r requirements.txt
🔑 AI Setup (Optional)

If using OpenAI or any LLM provider:

Create a .env file:

OPENAI_API_KEY=your_api_key_here

Ensure your ai_reviewer.py loads environment variables correctly.

🧪 Sample Demo File
def process_order(price, quantity):
    total = price * quantity
    return total

Running with --ai will provide additional improvement suggestions.

🛠️ Tech Stack

Python 3.10+

AST (Abstract Syntax Tree)

OpenAI API (or compatible LLM)

Streamlit

Argparse / Typer

dotenv

📈 Future Enhancements

Multi-language support

GitHub PR integration

Code diff viewer

Auto-fix suggestions

CI/CD integration

Docker support

Unit test coverage analysis

🏆 Why This Project?

This project demonstrates:

Modular architecture design

CLI tool development

AI integration

Static code analysis implementation

Streamlit UI development

Clean software engineering practices

Ideal for:

Internship portfolios

Campus placements

Resume projects

Open-source contributions

📜 License

MIT License
