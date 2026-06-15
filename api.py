import subprocess
import requests
import os
import json

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
    # Passes inputs straight down to C++ execute arguments
    res = call_cpp_engine(["auth", clean_user, clean_pass])
    return "SUCCESS" in res

# --- 2. C++ ASSET MANAGEMENT MAPPINGS ---
def add_book(book_id, title, author):
    return call_cpp_engine(["add_book", book_id.strip(), title.strip(), author.strip()])

def view_books():
    raw_out = call_cpp_engine(["view_books"])
    if not raw_out or "No books" in raw_out or raw_out.startswith("ERROR"): 
        return []
    
    books = []
    for line in raw_out.split("\n"):
        clean_line = line.strip()
        if not clean_line:  # Skip raw trailing newlines cleanly
            continue
            
        if "|" in clean_line:
            parts = clean_line.split("|")
            # 🟢 DEFENSIVE GUARDRAIL: Verify the line has all 4 expected fields
            if len(parts) < 4:
                continue
            books.append({"id": parts[0], "title": parts[1], "author": parts[2], "status": parts[3]})
    return books

# --- 3. C++ SCHOLAR NODE REGISTRY MAPPINGS ---
def add_student(student_id, name, department):
    return call_cpp_engine(["add_student", student_id.strip(), name.strip(), department.strip()])

def view_students():
    raw_out = call_cpp_engine(["view_students"])
    if not raw_out or "No students" in raw_out or raw_out.startswith("ERROR"): 
        return []
    
    students = []
    for line in raw_out.split("\n"):
        clean_line = line.strip()
        if not clean_line:  # Skip blank lines safely
            continue
            
        if "|" in clean_line:
            parts = clean_line.split("|")
            # 🟢 DEFENSIVE GUARDRAIL: Verify the student line has all 3 fields
            if len(parts) < 3:
                continue
            students.append({"id": parts[0], "name": parts[1], "dept": parts[2]})
    return students

# --- 4. C++ CIRCULATION LOGIC MAPPINGS ---
def issue_book(student_id, book_id):
    return call_cpp_engine(["issue_book", student_id.strip(), book_id.strip()])

def return_book(book_id):
    return call_cpp_engine(["return_book", book_id.strip()])

def get_reports():
    return call_cpp_engine(["reports"])

# --- 4.5 NEW CRITICAL EXTENSION MAPPINGS (EDIT & DELETE FUNCTIONS) ---
def delete_book(book_id):
    """Signals C++ backend to drop a book record matching the target book_id."""
    return call_cpp_engine(["delete_book", book_id.strip()])

def edit_book(book_id, new_title, new_author):
    """Passes modified metadata values down to overwrite an existing book record."""
    return call_cpp_engine(["edit_book", book_id.strip(), new_title.strip(), new_author.strip()])

def delete_student(student_id):
    """Signals C++ backend to delete a student record matching the target student_id."""
    return call_cpp_engine(["delete_student", student_id.strip()])

def edit_student(student_id, new_name, new_dept):
    """Passes modified profile fields down to overwrite an existing student record."""
    return call_cpp_engine(["edit_student", student_id.strip(), new_name.strip(), new_dept.strip()])

# --- 5. GLOBAL OPEN LIBRARY REPOSITORY SYNC (HTTPS API) ---
def search_open_library(title):
    if not title or not title.strip():
        return []
    try:
        clean_title = title.strip().replace(" ", "+")
        url = f"https://openlibrary.org/search.json?title={clean_title}"
        
        # Security Verification Header added to satisfy Open Library firewall
        headers = {
            "User-Agent": "SmartLibrarySystem/1.0 (mabdullah17; university_project)"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            docs = data.get("docs", [])
            
            results = []
            for d in docs[:5]: # Extract top 5 matched matrix rows
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
        # Extracts your Groq key securely from the environment secrets setup
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
