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
    try:
        url = f"https://openlibrary.org/search.json?title={title}"
        response = requests.get(url, timeout=10).json()
        return [{"title": d.get("title", "N/A"), "author": d.get("author_name", ["Unknown"])[0], "year": d.get("first_publish_year", "N/A")} for d in response.get("docs", [])[:5]]
    except Exception:
        return []

def get_ai_summary(book_title, api_key):
    if not api_key: return "Provide valid access token key credentials."
    try:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": f"Provide 1 line summary for: {book_title}"}]}
        return requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers, timeout=12).json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        return str(e)
