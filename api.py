import subprocess
import requests
import os
import sys

CPP_EXECUTABLE = "./library_system"
if os.name == 'nt':
    CPP_EXECUTABLE = "library_system.exe"

# Global persistent process variable context
_cpp_process = None

def get_cpp_engine():
    global _cpp_process
    if _cpp_process is None or _cpp_process.poll() is not None:
        try:
            _cpp_process = subprocess.Popen(
                [CPP_EXECUTABLE],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
        except Exception as e:
            print(f"FATAL: Engine boot failure: {str(e)}", file=sys.stderr)
    return _cpp_process

def query_backend(input_command_string):
    engine = get_cpp_engine()
    if not engine:
        return "ERROR: Backend application binary missing."
    
    # Write structural arguments cleanly to standard inputs stream
    engine.stdin.write(input_command_string)
    engine.stdin.flush()
    
    # Listen until target boundary marker reached
    buffer_lines = []
    while True:
        line = engine.stdout.readline().strip()
        if line == "---END_ACTION---" or not line:
            break
        buffer_lines.append(line)
        
    return "\n".join(buffer_lines)

# --- Clean Mapping Endpoints ---
def verify_login(user, password):
    res = query_backend(f"1\n{user}\n{password}\n")
    return "SUCCESS" in res

def add_book(book_id, title, author):
    return query_backend(f"2\n{book_id}\n{title}\n{author}\n")

def view_books():
    raw_out = query_backend("3\n")
    if not raw_out or "No books" in raw_out: return []
    books = []
    for line in raw_out.split("\n"):
        if "|" in line:
            parts = line.split("|")
            books.append({"id": parts[0], "title": parts[1], "author": parts[2], "status": parts[3]})
    return books

def add_student(student_id, name, department):
    return query_backend(f"4\n{student_id}\n{name}\n{department}\n")

def view_students():
    raw_out = query_backend("5\n")
    if not raw_out or "No students" in raw_out: return []
    students = []
    for line in raw_out.split("\n"):
        if "|" in line:
            parts = line.split("|")
            students.append({"id": parts[0], "name": parts[1], "dept": parts[2]})
    return students

def issue_book(student_id, book_id):
    return query_backend(f"6\n{student_id}\n{book_id}\n")

def return_book(book_id):
    return query_backend(f"7\n{book_id}\n")

def get_reports():
    return query_backend("8\n")

# --- Web Feature Routing API Integrations ---
def search_open_library(title):
    try:
        url = f"https://openlibrary.org/search.json?title={title}"
        response = requests.get(url, timeout=10).json()
        return [{"title": d.get("title", "N/A"), "author": d.get("author_name", ["Unknown"])[0], "year": d.get("first_publish_year", "N/A")} for d in response.get("docs", [])[:5]]
    except Exception:
        return []

def get_ai_summary(book_title, api_key):
    if not api_key: return "Provide valid access credentials token."
    try:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": f"Provide 1 line summary for: {book_title}"}]}
        return requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers, timeout=12).json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        return str(e)