import subprocess
import requests
import os

CPP_SOURCE = "library_system.cpp"
CPP_EXECUTABLE = "./library_system"

if os.name == 'nt':
    CPP_EXECUTABLE = "library_system.exe"

def compile_cpp_if_missing():
    # Automatically compiles the C++ file if it hasn't been built yet
    if not os.path.exists(CPP_EXECUTABLE):
        try:
            if os.name == 'nt':
                subprocess.run(["g++", "-O3", CPP_SOURCE, "-o", "library_system"], check=True)
            else:
                subprocess.run(["g++", "-O3", CPP_SOURCE, "-o", "library_system"], check=True)
                subprocess.run(["chmod", "+x", "library_system"], check=True)
        except Exception as e:
            print(f"COMPILATION ERROR: {str(e)}")

# Force compilation evaluation on initialization
compile_cpp_if_missing()

def call_cpp_engine(args):
    compile_cpp_if_missing() # Safety check toggle
    try:
        result = subprocess.run([CPP_EXECUTABLE] + args, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        return f"ERROR: Backend communication failed: {str(e)}"

# --- Mapping Endpoints ---
def verify_login(user, password):
    clean_user = user.strip()
    clean_pass = password.strip()
    res = call_cpp_engine(["auth", clean_user, clean_pass])
    return "SUCCESS" in res

def add_book(book_id, title, author):
    return call_cpp_engine(["add_book", book_id, title, author])

def view_books():
    raw_out = call_cpp_engine(["view_books"])
    if not raw_out or "No books" in raw_out or raw_out.startswith("ERROR"): 
        return []
    books = []
    for line in raw_out.split("\n"):
        if "|" in line:
            parts = line.split("|")
            books.append({"id": parts[0], "title": parts[1], "author": parts[2], "status": parts[3]})
    return books

def add_student(student_id, name, department):
    return call_cpp_engine(["add_student", student_id, name, department])

def view_students():
    raw_out = call_cpp_engine(["view_students"])
    if not raw_out or "No students" in raw_out or raw_out.startswith("ERROR"): 
        return []
    students = []
    for line in raw_out.split("\n"):
        if "|" in line:
            parts = line.split("|")
            students.append({"id": parts[0], "name": parts[1], "dept": parts[2]})
    return students

def issue_book(student_id, book_id):
    return call_cpp_engine(["issue_book", student_id, book_id])

def return_book(book_id):
    return call_cpp_engine(["return_book", book_id])

def get_reports():
    return call_cpp_engine(["reports"])

# --- API Integration Endpoints ---
def search_open_library(title):
    # If the user input is empty, return a blank list immediately
    if not title or not title.strip():
        return []
        
    try:
        # Standardized web encoding for URL string paths
        clean_title = title.strip().replace(" ", "+")
        url = f"https://openlibrary.org/search.json?title={clean_title}"
        
        # 🟢 THE FIX: Explicitly tell the global server who we are so it clears the firewall
        headers = {
            "User-Agent": "SmartLibrarySystem/1.0 (mabdullah17; university_project)"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            docs = data.get("docs", [])
            
            # Form clean structured dictionary objects for the UI
            results = []
            for d in docs[:5]:  # Capture the top 5 book matches
                author_list = d.get("author_name", ["Unknown"])
                results.append({
                    "Title": d.get("title", "N/A"),
                    "Author": author_list[0] if author_list else "Unknown",
                    "First Publish Year": d.get("first_publish_year", "N/A")
                })
            return results
        else:
            return [{"Error": f"Global server rejected connection. Code: {response.status_code}"}]
            
    except Exception as e:
        return [{"Error": f"Network sync sequence failure: {str(e)}"}]

def get_ai_summary(book_title, api_key=None):
    # Automatically pulls the hidden key from Streamlit Secrets if no key is typed
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets["OPENAI_API_KEY"]
        except Exception:
            return "Error: Secure API Key token not found in Cloud Secrets Configuration."

    try:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": f"Provide 1 line summary for: {book_title}"}]}
        return requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers, timeout=12).json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        return str(e)
      
