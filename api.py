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
    Automatically compiles the C++ file if it hasn't been built yet.
    This guarantees your C++ engine runs perfectly on Streamlit Cloud servers.
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

# Force compilation evaluation on server initialization
compile_cpp_if_missing()

def push_to_github(filename):
    """
    AUTOMATED STATE SYNC ENGINE: Forces local C++ text updates 
    to write directly back into your permanent GitHub repository 
    to prevent any data loss on Streamlit Cloud.
    """
    try:
        import streamlit as st
        # Reads your secure developer token from Streamlit Secrets cloud environment
        token = st.secrets["GITHUB_TOKEN"]
        repo = "mabdullah17/smart-library-system"
        url = f"https://api.github.com/repos/{repo}/contents/{filename}"
        
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # 1. Fetch current file metadata from GitHub to acquire the required SHA blob hash
        response = requests.get(url, headers=headers)
        sha = response.json().get("sha") if response.status_code == 200 else None
        
        # Check if local file exists before trying to read it
        if not os.path.exists(filename):
            return
            
        # 2. Convert the local file contents into a Base64 string payload
        with open(filename, "rb") as f:
            encoded_content = base64.b64encode(f.read()).decode("utf-8")
            
        payload = {
            "message": f"System state sync auto-commit: updating {filename}",
            "content": encoded_content
        }
        if sha:
            payload["sha"] = sha
            
        # 3. Securely overwrite the target file inside your active GitHub repository tree
        requests.put(url, headers=headers, json=payload)
    except Exception as e:
        print(f"GITHUB DATA PERSISTENCE LINK FAILURE: {str(e)}")

def call_cpp_engine(args):
    """Handles communication between Python and the compiled C++ executable."""
    compile_cpp_if_missing()
    try:
        result = subprocess.run([CPP_EXECUTABLE] + args, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        return f"ERROR: Backend communication failed: {str(e)}"

# --- 1. CORE C++ AUTHENTICATION MAPPING ---
def verify_login(user, password):
    clean_user = user.strip()
    clean_pass = password.strip()
    res = call_cpp_engine(["auth", clean_user, clean_pass])
    return "SUCCESS" in res

# --- 2. C++ ASSET MANAGEMENT MAPPINGS ---
def add_book(book_id, title, author):
    res = call_cpp_engine(["add_book", book_id.strip(), title.strip(), author.strip()])
    push_to_github("books.txt")
    return res

def view_books():
    raw_out = call_cpp_engine(["view_books"])
    if not raw_out or "No books" in raw_out or raw_out.startswith("ERROR"): 
        return []
    books = []
    for line in raw_out.split("\n"):
        clean_line = line.strip()
        if not clean_line:
            continue
        if "|" in clean_line:
            parts = clean_line.split("|")
            if len(parts) < 4:
                continue
            books.append({"id": parts[0], "title": parts[1], "author": parts[2], "status": parts[3]})
    return books

# --- 3. C++ SCHOLAR NODE REGISTRY MAPPINGS ---
def add_student(student_id, name, department):
    res = call_cpp_engine(["add_student", student_id.strip(), name.strip(), department.strip()])
    push_to_github("students.txt")
    return res

def view_students():
    raw_out = call_cpp_engine(["view_students"])
    if not raw_out or "No students" in raw_out or raw_out.startswith("ERROR"): 
        return []
    students = []
    for line in raw_out.split("\n"):
        clean_line = line.strip()
        if not clean_line:
            continue
        if "|" in clean_line:
            parts = clean_line.split("|")
            if len(parts) < 3:
                continue
            students.append({"id": parts[0], "name": parts[1], "dept": parts[2]})
    return students

# --- 4. C++ CIRCULATION LOGIC MAPPINGS ---
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

# --- 4.5 ADMINISTRATIVE MANAGEMENT EXTENSIONS (EDIT & DELETE CONTROL) ---
def delete_book(book_id):
    res = call_cpp_engine(["delete_book", book_id.strip()])
    push_to_github("books.txt")
    return res

def edit_book(book_id, new_title, new_author):
    res = call_cpp_engine(["edit_book", book_id.strip(), new_title.strip(), new_author.strip()])
    push_to_github("books.txt")
    return res

def delete_student(student_id):
    res = call_cpp_engine(["delete_student", student_id.strip()])
    push_to_github("students.txt")
    return res

def edit_student(student_id, new_name, new_dept):
    res = call_cpp_engine(["edit_student", student_id.strip(), new_name.strip(), new_dept.strip()])
    push_to_github("students.txt")
    return res

# --- 5. GLOBAL OPEN LIBRARY REPOSITORY SYNC (HTTPS API) ---
def search_open_library(title):
    if not title or not title.strip():
        return []
    try:
        clean_title = title.strip().replace(" ", "+")
        url = f"https://openlibrary.org/search.json?title={clean_title}"
        headers = {
            "User-Agent": "SmartLibrarySystem/1.0 (mabdullah17; university_project)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            docs = data.get("docs", [])
            results = []
            for d in docs[:5]:
                author_list = d.get("author_name", ["Unknown"])
                results.append({
                    "Title": d.get("title", "N/A"),
                    "Author": author_list[0] if author_list else "Unknown",
                    "First Publish Year": d.get("first_publish_year", "N/A")
                })
            return results
        else:
            return [{"Error": f"Global server sync rejected. Code: {response.status_code}"}]
    except Exception as e:
        return [{"Error": f"Network sync matrix failure: {str(e)}"}]

# --- 6. SECURE AI ADVOCACY SYNTHESIS PIPELINE (GROQ CLOUD API) ---
def get_ai_summary(book_title):
    try:
        import streamlit as st
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        return "ERROR: Secure Groq API Key token not found in Cloud Secrets."

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
        else:
            return f"ERROR: Groq Engine rejected request. Code: {response.status_code}"
    except Exception as e:
        return f"ERROR: Synthesis Pipeline crashed: {str(e)}"
