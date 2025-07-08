# Code Genie

Code Genie is a Streamlit-based web application that provides AI-powered code workflows, semantic search, and code comment generation. It leverages Groq and Blackbox AI APIs to deliver code explanations, refactoring, reviews, bug detection, and test generation for multiple programming languages.

## Features

- **Full Code Workflow:**
  - Code explanation tailored to skill level and user role
  - Automated code refactoring
  - Code review and error detection
  - Test case generation
  - Downloadable workflow report
- **Semantic Search:**
  - Ask natural language questions about your code
  - Get intelligent, context-aware answers
- **Code Comment Generator:**
  - Add clear, helpful comments to your code
  - Download commented code

## Supported Languages
- Python
- JavaScript
- TypeScript
- Java
- C++
- C#

## Prerequisites
- Python 3.8+
- [Streamlit](https://streamlit.io/)
- API keys for [Groq](https://groq.com/) and [Blackbox AI](https://www.blackbox.ai/)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   If `requirements.txt` is missing, install manually:
   ```bash
   pip install streamlit requests
   ```

3. **Set up API keys:**
   - Create a `.streamlit/secrets.toml` file in your project root:
     ```toml
     GROQ_API_KEY = "your_groq_api_key"
     BLACKBOX_API_KEY = "your_blackbox_api_key"
     ```

## Running the App

```bash
streamlit run app.py
```

The app will open in your browser. Use the sidebar to navigate between features.

## Usage

### 1. Full Code Workflows
- Paste or upload your code.
- Select language, skill level, user role, and explanation language.
- Click **Run Workflow** to get explanations, refactoring, review, bug detection, and tests.
- Download the full workflow report.

### 2. Semantic Search
- Paste or upload your code.
- Ask a natural language question about your code.
- Get an AI-generated answer.

### 3. Code Comment Generator
- Paste or upload your code.
- Select the programming language.
- Click **Generate Comments** to get code with helpful comments.
- Download the commented code.

## Using Blackbox AI Agents in VS Code

Code Genie also use Blackbox AI agent directly in Visual Studio Code for code completion, chat, and code generation.

### Steps:
1. **Install the Blackbox AI VS Code Extension:**
   - Open VS Code.
   - Go to Extensions (`Ctrl+Shift+X`).
   - Search for `Blackbox AI` and install it.
   - [Blackbox AI Extension on Marketplace](https://marketplace.visualstudio.com/items?itemName=Blackboxapp.blackbox)

2. **Authenticate:**
   - Click on the Blackbox icon in the sidebar or use the command palette (`Ctrl+Shift+P` > `Blackbox: Login`).
   - Log in with your Blackbox account and enter your API key if prompted.

3. **Usage:**
   - Use inline code completions as you type.
   - Highlight code and use the context menu for explanations, refactoring, or comments.
   - Open the Blackbox chat panel for conversational AI assistance.

For more details, see the [official Blackbox AI documentation](https://www.blackbox.ai/).

## Notes
- Ensure your API keys are kept secure and **never** commit them to version control.
- The app uses external APIs; usage may be subject to rate limits or costs.

