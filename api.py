import subprocess
import requests
import os
import base64

CPP_SOURCE = "library_system.cpp"
CPP_EXECUTABLE = "./library_system"

if os.name == 'nt':
    CPP_EXECUTABLE = "library_system.exe"

def compile_cpp_if_missing():
    """
    Automatically compiles your simple C++ file if it doesn't exist.
    This ensures the engine runs smoothly on Streamlit Cloud servers.
    """
    if not os.path.exists(CPP_EXECUTABLE):
        try:
            if os.name == 'nt':
                subprocess.run(["g++", "-O3", CPP_SOURCE, "-o", "library_system"], check=True)
            else:
                subprocess.run(["g++", "-O3", CPP_SOURCE, "-o", "library_system"], check=True)
                subprocess.run(["chmod", "+x", "library_system"], check=True)
        except Exception as e:
            print(f"COMPILATION ERROR: {str(e)}")

# Build the C++ binary right when the server starts up
compile_cpp_if_missing()

def push_to_github(filename):
    """
    AUTOMATED GITHUB SYNC ENGINE: Takes your local text file changes
    and pushes them straight back to GitHub so data is never wiped out.
    """
    try:
        import streamlit as st
        token = st.secrets["GITHUB_TOKEN"]
        repo = "mabdullah17/smart-library-system"
        url = f"https://api.github.com/repos/{repo}/contents/{filename}"
        
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Look for the file in the absolute root directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, filename)
        
        if not os.path.exists(file_path):
            return
            
        # 1. Fetch current file code from GitHub to find its matching SHA tag
        response = requests.get(url, headers=headers)
        sha = response.json().get("sha") if response.status_code == 200 else None
        
        # 2. Convert the local file data into a safe Base64 string
        with open(file_path, "rb") as f:
            encoded_content = base64.b64encode(f.read()).decode("utf-8")
            
        payload = {
            "message": f"Library system auto-sync: updating {filename}",
            "content": encoded_content
        }
        if sha:
            payload["sha"] = sha
            
        # 3. Securely update the file inside your repository tree
        requests.put(url, headers=headers, json=payload)
    except Exception as e:
        print(f"GITHUB STORAGE SYNC ERROR: {str(e)}")

def call_cpp_engine(args):
    """Communicates directly with your compiled C++ program."""
    compile_cpp_if_missing()
    try:
        result = subprocess.run([CPP_EXECUTABLE] + args, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        return f"ERROR: Backend communication failed: {str(e)}"

# --- 1. LOGIN VERIFICATION ---
def verify_login(user, password):
    res = call_cpp_engine(["auth", user.strip(), password.strip()])
    return "SUCCESS" in res

# --- 2. BOOK MANAGEMENT ---
def add_book(book_id, title, author):
    # Strip spaces from inputs to avoid file parsing issues
    clean_id = book_id.strip().replace(" ", "_")
    clean_title = title.strip().replace(" ", "_")
    clean_author = author.strip().replace(" ", "_")
    
    res = call_cpp_engine(["add_book", clean_id, clean_title, clean_author])
    push_to_github("books.txt")
    return res

def view_books():
    raw_out = call_cpp_engine(["view_books"])
    if not raw_out or "No books" in raw_out or raw_out.startswith("ERROR"): 
        return []
        
    books_list = []
    for line in raw_out.split("\n"):
        clean_line = line.strip()
        if not clean_line or "|" not in clean_line:
            continue
        parts = clean_line.split("|")
        if len(parts) >= 4:
            # Replaces underscores back into spaces for clean display on the web page
            books_list.append({
                "id": parts[0], 
                "title": parts[1].replace("_", " "), 
                "author": parts[2].replace("_", " "), 
                "status": parts[3]
            })
    return books_list

# --- 3. STUDENT REGISTRATION ---
def add_student(student_id, name, department):
    clean_id = student_id.strip().replace(" ", "_")
    clean_name = name.strip().replace(" ", "_")
    clean_dept = department.strip().replace(" ", "_")
    
    res = call_cpp_engine(["add_student", clean_id, clean_name, clean_dept])
    push_to_github("students.txt")
    return res

def view_students():
    raw_out = call_cpp_engine(["view_students"])
    if not raw_out or "No students" in raw_out or raw_out.startswith("ERROR"): 
        return []
        
    students_list = []
    for line in raw_out.split("\n"):
        clean_line = line.strip()
        if not clean_line or "|" not in clean_line:
            continue
        parts = clean_line.split("|")
        if len(parts) >= 3:
            students_list.append({
                "id": parts[0], 
                "name": parts[1].replace("_", " "), 
                "dept": parts[2].replace("_", " ")
            })
    return students_list

# --- 4. CIRCULATION (ISSUE & RETURN) ---
def issue_book(student_id, book_id):
    res = call_cpp_engine(["issue_book", student_id.strip(), book_id.strip()])
    push_to_github("books.txt")
    push_to_github("transactions.txt")
    return res

def return_book(book_id):
    res = call_cpp_engine(["return_book", book_id.strip()])
    push_to_github("books.txt")
    push_to_github("transactions.txt")
    return res

def get_reports():
    return call_cpp_engine(["reports"])

# --- 5. SYSTEM DATA CLEANUP / EXTENSIONS ---
# These sync with standard operations if you choose to activate them in the UI later
def delete_book(book_id):
    res = call_cpp_engine(["delete_book", book_id.strip()])
    push_to_github("books.txt")
    return res

def delete_student(student_id):
    res = call_cpp_engine(["delete_student", student_id.strip()])
    push_to_github("students.txt")
    return res

# --- 6. EXTERNAL NETWORK APIS (OPEN LIBRARY SYNC) ---
def search_open_library(title):
    if not title or not title.strip():
        return []
    try:
        clean_title = title.strip().replace(" ", "+")
        url = f"https://openlibrary.org/search.json?title={clean_title}"
        headers = {"User-Agent": "SmartLibrarySystem/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            docs = response.json().get("docs", [])
            results = []
            for d in docs[:5]:
                authors = d.get("author_name", ["Unknown"])
                results.append({
                    "Title": d.get("title", "N/A"),
                    "Author": authors[0] if authors else "Unknown",
                    "First Publish Year": d.get("first_publish_year", "N/A")
                })
            return results
        return []
    except Exception:
        return []

# --- 7. SECURE AI ADVOCACY COMPONENT (GROQ API) ---
def get_ai_summary(book_title):
    try:
        import streamlit as st
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        return "ERROR: Missing Groq API Key credential in Streamlit Secrets."

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": f"Provide a single 1-line summary for the book: {book_title}"}]
        }
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=data, headers=headers, timeout=12)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        return "AI analysis engine offline at the moment."
    except Exception as e:
        return f"ERROR: Synthesis failed: {str(e)}"
