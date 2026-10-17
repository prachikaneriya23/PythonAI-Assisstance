# 🤖 Python Learning Assistant

> An interactive desktop application that helps you **learn Python, explore programming concepts, run and debug code, and understand Python errors** — all from one place.

The **Python Learning Assistant** is a Python-based educational desktop application built with **CustomTkinter**. It combines a structured programming knowledge base with **machine-learning-powered topic matching** to provide relevant explanations and code examples.

Whether you're learning Python fundamentals, exploring OOP, working with NumPy or Pandas, or trying to understand a frustrating traceback, this application provides an interactive environment to help you learn and debug more effectively.

---

## ✨ Features

### 💬 1. Ask / Learn

Ask questions about Python concepts using natural language.

The assistant searches its knowledge base and provides:

- 📚 Topic explanations
- 🏷️ Topic categories
- 💻 Practical code examples
- 🔎 Intelligent topic matching
- 💬 Interactive chat-style responses

Example questions:

```text
How do decorators work?

Explain Python classes

What is regex?

How do I use Pandas?

Explain NumPy arrays
```

The application uses a machine-learning-based matcher to identify the most relevant category for a user's question.

---

### ▶️ 2. Run & Debug

The **Run & Debug** tab allows users to write or paste Python code and execute it directly from the application.

It provides:

- ▶️ Code execution
- 📤 Program output
- ❌ Error output
- 🐛 Automatic error explanations
- ⏱️ Execution timeout protection
- 🧹 Clear/reset functionality

The application executes submitted code in a temporary Python file and captures both standard output and errors. Code execution is limited to 10 seconds to help prevent infinite loops from running indefinitely.

---

### 🧩 3. Error Solver

Have a Python traceback you don't understand?

Paste the error into the **Error Solver** and the application attempts to explain what went wrong and suggest possible fixes.

It recognizes common Python errors including:

- `SyntaxError`
- `IndentationError`
- `NameError`
- `TypeError`
- `IndexError`
- `KeyError`
- `AttributeError`
- `ZeroDivisionError`
- `ValueError`
- `ModuleNotFoundError`
- `ImportError`
- `RecursionError`
- `FileNotFoundError`
- `UnboundLocalError`

For recognized errors, the application provides:

1. Error type
2. Human-readable explanation
3. Suggested fixes

Unknown errors receive a generic troubleshooting explanation instead.

---

### 📖 4. Browse Topics

The **Browse Topics** section allows users to explore the complete programming knowledge base.

Topics can be filtered by category, and each topic provides:

- Topic title
- Category
- Explanation
- Code example

The application currently targets topics including areas such as:

- Python fundamentals
- Object-Oriented Programming
- Regular Expressions
- NumPy
- Pandas
- Django
- And other programming concepts available in the knowledge base.

---

## 🧠 Machine Learning

One of the key components of this project is its **machine-learning-based knowledge matcher**.

The `KnowledgeMatcher` class uses:

### TF-IDF Vectorization

User queries and knowledge-base documents are transformed into numerical vectors using **TF-IDF (Term Frequency–Inverse Document Frequency)**.

### Logistic Regression

A **Logistic Regression** classifier is trained using the categories in the knowledge base.

The matching process is approximately:

```text
User Question
      │
      ▼
Text Preprocessing
      │
      ▼
TF-IDF Vectorization
      │
      ▼
Logistic Regression
      │
      ▼
Predicted Category
      │
      ▼
Similarity Scoring
      │
      ▼
Best Matching Topics
      │
      ▼
Explanation + Code Example
```

The matcher combines the predicted category with document similarity to rank relevant knowledge-base entries.

---

## 🏗️ Project Architecture

```text
                         ┌──────────────────────┐
                         │   Python Learning    │
                         │      Assistant       │
                         └──────────┬───────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
       Ask / Learn            Run & Debug            Error Solver
             │                      │                      │
             ▼                      ▼                      ▼
     KnowledgeMatcher         Python Execution       Error Patterns
             │                      │                      │
             ▼                      ▼                      ▼
        TF-IDF +              Output/Error          Explanation +
      Logistic Regression        Capture              Fixes
             │
             ▼
      Knowledge Base
             │
             ▼
       knowledge_base.csv
```

---

## 🛠️ Tech Stack

| Technology        | Purpose                                      |
| ----------------- | -------------------------------------------- |
| **Python**        | Core programming language                    |
| **CustomTkinter** | Modern desktop graphical interface           |
| **Pandas**        | Knowledge-base data processing               |
| **NumPy**         | Numerical operations                         |
| **Scikit-learn**  | TF-IDF vectorization and Logistic Regression |
| **Regex**         | Error-pattern detection                      |
| **CSV**           | Structured knowledge-base storage            |

The project's declared requirements currently include CustomTkinter, Pandas, and NumPy; the source code also uses scikit-learn for the machine-learning matcher.

---

## 📁 Project Structure

```text
PythonAI-Assisstance/
│
├── README.md
│
├── main.py
│   └── Main desktop application and user interface
│
├── matcher.py
│   └── TF-IDF + Logistic Regression knowledge matcher
│
├── error_solver.py
│   └── Python error detection and explanation engine
│
├── knowledge_base.csv
│   └── Structured Python learning knowledge base
│
├── knowledge_base_gen.py
│   └── Knowledge-base generation utility
│
├── requirements.txt
│   └── Python dependencies
│
└── temporary Python files
    └── Generated during code execution when required
```

The repository currently contains the core application, matcher, error solver, knowledge-base files, dependency file, and several empty temporary Python files.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have:

- **Python 3.x**
- `pip`
- A working Python environment

You can verify Python is installed with:

```bash
python --version
```

---

## 📥 Installation

### 1. Clone the repository

```bash
git clone https://github.com/prachikaneriya23/PythonAI-Assisstance.git
```

### 2. Navigate to the project directory

```bash
cd PythonAI-Assisstance
```

### 3. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

The repository's current requirements file specifies:

```text
customtkinter>=5.2.0
pandas>=2.0.0
numpy>=1.24.0
```

The machine-learning matcher additionally relies on **scikit-learn**, so if it is not already installed in your environment, install it with:

```bash
pip install scikit-learn
```



---

## ▶️ Running the Application

Start the application with:

```bash
python main.py
```

The application opens a desktop window titled:

```text
Python Learning Assistant
```

The interface provides four tabs:

```text
┌─────────────────────────────────────────────┐
│        Python Learning Assistant             │
├─────────────────────────────────────────────┤
│ Ask / Learn │ Run & Debug │ Error Solver │ Browse Topics │
└─────────────────────────────────────────────┘
```



---

## 💡 Example Workflow

### Learn a concept

Enter:

```text
How do Python decorators work?
```

The application searches the knowledge base and returns relevant explanations and examples.

### Debug code

Enter:

```python
numbers = [1, 2, 3]
print(numbers[5])
```

Click:

```text
Run Code
```

The application captures the resulting error and displays an automatic debugging explanation.

### Solve an existing traceback

Paste:

```text
NameError: name 'username' is not defined
```

Click:

```text
Solve Error
```

The application identifies the error and provides an explanation and suggested fixes.

---

## 🐛 Error-Solving Architecture

The error solver uses predefined regular-expression patterns to identify common Python exceptions.

```text
Python Traceback
       │
       ▼
Extract Error Text
       │
       ▼
Pattern Matching
       │
       ├── SyntaxError
       ├── NameError
       ├── TypeError
       ├── IndexError
       ├── KeyError
       ├── ValueError
       ├── AttributeError
       └── Other Errors
              │
              ▼
       Explanation + Fixes
```

The implementation maintains a collection of regular-expression patterns with corresponding explanations and troubleshooting recommendations.

---

## 🔐 Code Execution Considerations

The **Run & Debug** feature executes user-provided Python code using the current Python interpreter.

For basic protection against accidentally hanging the application, execution has a **10-second timeout**.

However, this should **not be considered a secure sandbox** for running untrusted or malicious code.

Only execute code that you understand and trust.

---

## 🎯 Project Objectives

The project is designed around several educational goals:

- 📚 Make Python concepts easier to understand
- 🧠 Introduce machine-learning-based topic matching
- 💻 Provide practical programming examples
- 🐛 Make debugging easier for beginners
- 🔍 Explain common Python errors
- 🖥️ Combine learning and experimentation in one desktop application
- 🚀 Encourage hands-on Python practice

---

## 🌟 Why This Project?

Learning programming often involves two major challenges:

> **Understanding concepts** and **understanding errors**.

This project brings both together.

Instead of switching between multiple resources, learners can:

```text
Ask a Question
      ↓
Understand the Concept
      ↓
View Example Code
      ↓
Run the Code
      ↓
Encounter an Error
      ↓
Get an Explanation
      ↓
Fix the Code
      ↓
Learn
```

This creates a practical **learn → experiment → debug → improve** workflow.

---

## 🔮 Future Enhancements

Potential future improvements include:

- 🤖 More advanced AI/LLM-based responses
- 🧠 Larger and more diverse knowledge base
- 💬 Conversation memory
- 📝 Interactive Python exercises
- 🏆 Quizzes and coding challenges
- 📊 Learning progress tracking
- 🎯 Personalized learning paths
- 🔍 Improved semantic search
- 🌐 Web-based version
- 📱 Mobile version
- 🎨 Syntax highlighting
- 📂 Project/file management
- 🧪 Automated test execution
- 🔒 Stronger code sandboxing
- 📈 ML model evaluation metrics
- 🔊 Voice-based learning assistant

---

## 🤝 Contributing

Contributions are welcome!

### 1. Fork the repository

Create your own fork of the project.

### 2. Create a feature branch

```bash
git checkout -b feature/your-feature
```

### 3. Make your changes

Improve the application, knowledge base, UI, error solver, or machine-learning components.

### 4. Commit your changes

```bash
git add .
git commit -m "Add your feature"
```

### 5. Push your branch

```bash
git push origin feature/your-feature
```

### 6. Open a Pull Request

Describe your changes clearly and submit the pull request for review.

---

## 📄 License

No license is currently specified in the repository.

If you plan to distribute or accept contributions to this project, consider adding an appropriate open-source license such as the MIT License.

---

