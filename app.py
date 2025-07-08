import streamlit as st
import difflib
import requests
import datetime
import streamlit.components.v1 as components

# --- CONFIG ---
# Place your API keys here
GROQ_API_KEY = st.secrets.get('GROQ_API_KEY', 'YOUR_GROQ_API_KEY')
BLACKBOX_API_KEY = st.secrets.get('BLACKBOX_API_KEY', 'YOUR_BLACKBOX_API_KEY')

PROGRAMMING_LANGUAGES = ["Python", "JavaScript", "TypeScript", "Java", "C++", "C#"]
SKILL_LEVELS = ["Beginner", "Intermediate", "Expert"]
USER_ROLES = ["Student", "Frontend Developer", "Backend Developer", "Data Scientist"]
EXPLANATION_LANGUAGES = ["English", "Spanish", "Chinese", "Urdu"]
EXAMPLE_QUESTIONS = [
    "What does this function do?",
    "How can I optimize this code?",
    "What are the potential bugs in this code?",
    "How does this algorithm work?",
    "What design patterns are used here?",
    "How can I make this code more readable?"
]

LANGUAGE_KEYWORDS = {
    "Python": ["def ", "import ", "self", "print(", "lambda", "None"],
    "JavaScript": ["function ", "console.log", "var ", "let ", "const ", "=>"],
    "TypeScript": ["interface ", "type ", ": string", ": number", "export ", "import "],
    "Java": ["public class", "System.out.println", "void main", "import java.", "new "],
    "C++": ["#include", "std::", "cout <<", "cin >>", "int main(", "using namespace"],
    "C#": ["using System;", "namespace ", "public class", "Console.WriteLine", "static void Main"]
}

# --- API STUBS ---
def call_groq_api(prompt, model="llama3-70b-8192"):
    # Replace with actual Groq API call
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"[Groq API Error] {response.text}"

def call_blackbox_agent(messages):
    url = "https://api.blackbox.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BLACKBOX_API_KEY}"
    }
    data = {
        "model": "code-chat",
        "messages": messages
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return call_groq_api(messages[-1]["content"])

# --- UTILS ---
def code_matches_language(code, language):
    keywords = LANGUAGE_KEYWORDS.get(language, [])
    return any(kw in code for kw in keywords)

def calculate_code_complexity(code):
    # Dummy complexity metric
    lines = code.count('\n') + 1
    return f"{lines} lines"

def get_inline_diff(original, modified):
    diff = difflib.unified_diff(
        original.splitlines(),
        modified.splitlines(),
        lineterm='',
        fromfile='Original',
        tofile='Refactored'
    )
    return '\n'.join(diff)

def is_coding_question(question):
    """
    Uses Blackbox AI agent to check if the question is about programming/code.
    Returns True if yes, False otherwise.
    """
    messages = [
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": f"Is the following question about programming or code? Answer only 'yes' or 'no'. Question: {question}"}
    ]
    try:
        response = call_blackbox_agent(messages)
        return 'yes' in response.lower()
    except Exception:
        return False

def get_explanation_prompt(code, programming_language, skill_level, user_role, explanation_language, question=None):
    lang_instruction = ""
    if explanation_language != "English":
        lang_instruction = f" Respond in {explanation_language}."
    if question:
        return f"{question}\n\nCode:\n{code}\n{lang_instruction}"
    return (
        f"Explain this {programming_language} code for a {skill_level} {user_role}.{lang_instruction}\n{code}"
    )

# --- STREAMLIT APP ---
st.set_page_config(page_title="Code Workflows", layout="wide")
st.title("Code Genie")

# Navigation
page = st.sidebar.radio("Navigate", ["Home", "Code Workflows", "Semantic Search", "Code Comment Generator"])

if page == "Home":
    st.header("Welcome to the Code Genie!")
    st.markdown("""
    - **Full Code Workflow:** Complete code analysis pipeline with explanation, refactoring, review, and testing
    - **Semantic Search:** Ask natural language questions about your code and get intelligent answers
    - **Code Comment Generator:** Helps you add helpful comments to your code for better readability
    """)
    st.info("Select a feature from the sidebar to get started.")

elif page == "Code Workflows":
    st.header("Full Code Workflows")
    code_input = st.text_area("Paste your code here", height=200)
    uploaded_file = st.file_uploader("Or upload a code file", type=["py", "js", "ts", "java", "cpp", "cs"])
    if uploaded_file:
        code_input = uploaded_file.read().decode("utf-8")
        st.text_area("File content", code_input, height=200, key="file_content")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        programming_language = st.selectbox("Programming Language", PROGRAMMING_LANGUAGES)
    with col2:
        skill_level = st.selectbox("Skill Level", SKILL_LEVELS)
    with col3:
        user_role = st.selectbox("Your Role", USER_ROLES)
    with col4:
        explanation_language = st.selectbox("Explanation Language", EXPLANATION_LANGUAGES)
    if code_input:
        st.caption(f"Complexity: {calculate_code_complexity(code_input)}")
    if st.button("Run Workflow", type="primary"):
        if not code_input.strip():
            st.error("Please paste or upload your code.")
        elif not code_matches_language(code_input, programming_language):
            st.error(f"Language mismatch. Please check your code and language selection.")
        else:
            with st.spinner("Running AI Workflow..."):
                steps = [
                    ("Explain", call_groq_api(get_explanation_prompt(code_input, programming_language, skill_level, user_role, explanation_language))),
                    ("Refactor", call_blackbox_agent([
                        {"role": "system", "content": "You are a helpful coding assistant."},
                        {"role": "user", "content": f"Refactor this {programming_language} code: {code_input}"}
                    ])),
                    ("Review", call_groq_api(f"Review this {programming_language} code for errors and improvements: {code_input}")),
                    ("ErrorDetection", call_groq_api(f"Find bugs in this {programming_language} code: {code_input}")),
                    ("TestGeneration", call_groq_api(f"Generate tests for this {programming_language} code: {code_input}")),
                ]
                timeline = []
                for step, output in steps:
                    timeline.append({"step": step, "output": output})
                st.success("Workflow complete!")
                for t in timeline:
                    st.subheader(t["step"])
                    st.write(t["output"])
                # Show code diff (dummy for now)
                st.subheader("Code Diff (Original vs Refactored)")
                refactored_code = steps[1][1]  # Blackbox agent output
                st.code(get_inline_diff(code_input, refactored_code), language=programming_language.lower())
                # Download report
                report = f"AI Workflow Report\nGenerated on: {datetime.datetime.now()}\nLanguage: {programming_language}\nSkill Level: {skill_level}\nRole: {user_role}\n\n"
                for t in timeline:
                    report += f"## {t['step']}\n{t['output']}\n\n---\n\n"
                st.download_button("Download Report", report, file_name="ai_workflow_report.txt")

elif page == "Semantic Search":
    st.header("Semantic Search")
    code_input = st.text_area("Paste your code here", height=200, key="sem_code")
    uploaded_file = st.file_uploader("Or upload a code file", type=["py", "js", "ts", "java", "cpp", "cs"], key="sem_file")
    if uploaded_file:
        code_input = uploaded_file.read().decode("utf-8")
        st.text_area("File content", code_input, height=200, key="sem_file_content")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        programming_language = st.selectbox("Programming Language", PROGRAMMING_LANGUAGES, key="sem_lang")
    with col2:
        skill_level = st.selectbox("Skill Level", SKILL_LEVELS, key="sem_skill")
    with col3:
        user_role = st.selectbox("Your Role", USER_ROLES, key="sem_role")
    with col4:
        explanation_language = st.selectbox("Explanation Language", EXPLANATION_LANGUAGES, key="sem_expl")

    st.caption("Example questions:")
    st.write(", ".join(EXAMPLE_QUESTIONS))

    # Single input field for question (typed only)
    question = st.text_input("Ask a question about your code", key="sem_question")

    # Run Semantic Search button
    if st.button("Run Semantic Search"):
        if not code_input.strip() or not question.strip():
            st.error("Both code and question are required.")
        elif not code_matches_language(code_input, programming_language):
            st.error(f"Language mismatch. Please check your code and language selection.")
        else:
            with st.spinner("Running Semantic Search..."):
                prompt = get_explanation_prompt(code_input, programming_language, skill_level, user_role, explanation_language, question=question)
                answer = call_groq_api(prompt)
                st.success("Answer:")
                st.write(answer)

elif page == "Code Comment Generator":
    st.header("Code Comment Generator")
    code_input = st.text_area("Paste your code here", height=200, key="comment_code")
    uploaded_file = st.file_uploader("Or upload a code file", type=["py", "js", "ts", "java", "cpp", "cs"], key="comment_file")
    if uploaded_file:
        code_input = uploaded_file.read().decode("utf-8")
        st.text_area("File content", code_input, height=200, key="comment_file_content")
    programming_language = st.selectbox("Programming Language", PROGRAMMING_LANGUAGES, key="comment_lang")
    if st.button("Generate Comments"):
        if not code_input.strip():
            st.error("Please paste or upload your code.")
        elif not code_matches_language(code_input, programming_language):
            st.error(f"Language mismatch. Please check your code and language selection.")
        else:
            with st.spinner("Generating commented code..."):
                prompt = (
                    f"Add clear, helpful comments to this {programming_language} code. "
                    "Keep the code unchanged except for adding comments. "
                    "Return the full code with comments:\n\n"
                    f"{code_input}"
                )
                commented_code = call_blackbox_agent([
                    {"role": "system", "content": "You are a helpful coding assistant."},
                    {"role": "user", "content": prompt}
                ])
                st.success("Commented code generated!")
                st.code(commented_code, language=programming_language.lower())
                st.download_button("Download Commented Code", commented_code, file_name="commented_code.txt") 