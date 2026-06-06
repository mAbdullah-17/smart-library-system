#include <iostream>
#include <fstream>
#include <string>

using namespace std;

const int MAX = 50;

// Helper function to convert text to lowercase for case-insensitive matching
string to_lowercase(string text) {
    for (int i = 0; i < text.length(); i++) {
        text[i] = tolower(text[i]);
    }
    return text;
}

// ==========================================
// 1. BOOK CLASS
// ==========================================
class Book {
public:
    string id;
    string title;
    string author;
    int is_issued; 

    Book() {
        id = "";
        title = "";
        author = "";
        is_issued = 0;
    }
};

// ==========================================
// 2. PERSON BASE CLASS (For Inheritance)
// ==========================================
class Person {
public:
    string id;
    string name;

    virtual void show_type() {
        cout << "Person Type: General" << endl;
    }
};

// ==========================================
// 3. STUDENT CLASS (Inherits Person)
// ==========================================
class Student : public Person {
public:
    string department;

    void show_type() {
        cout << "Person Type: Student" << endl;
    }
};

// ==========================================
// 4. MAIN LIBRARY SYSTEM CLASS
// ==========================================
class LibrarySystem {
private:
    Book book_list[MAX];
    Student student_list[MAX];
    int total_books;
    int total_students;

public:
    LibrarySystem() {
        total_books = 0;
        total_students = 0;
        load_files();
    }

    void load_files() {
        ifstream book_file("books.txt");
        if (book_file) {
            while (book_file >> book_list[total_books].id) {
                book_file.ignore();
                getline(book_file, book_list[total_books].title);
                getline(book_file, book_list[total_books].author);
                book_file >> book_list[total_books].is_issued;
                total_books++;
            }
            book_file.close();
        }

        ifstream student_file("students.txt");
        if (student_file) {
            while (student_file >> student_list[total_students].id) {
                student_file.ignore();
                getline(student_file, student_list[total_students].name);
                getline(student_file, student_list[total_students].department);
                total_students++;
            }
            student_file.close();
        }
    }

    void save_files() {
        ofstream book_file("books.txt");
        for (int i = 0; i < total_books; i++) {
            book_file << book_list[i].id << "\n"
                      << book_list[i].title << "\n"
                      << book_list[i].author << "\n"
                      << book_list[i].is_issued << "\n";
        }
        book_file.close();

        ofstream student_file("students.txt");
        for (int i = 0; i < total_students; i++) {
            //  CORRECTED LINE
student_file << student_list[i].id << "\n"
             << student_list[i].name << "\n"
             << student_list[i].department << "\n";
        }
        student_file.close();
    }

    void authenticate_user(string username, string password) {
    // Trim potential invisible server characters from the web inputs
    if (!username.empty() && (username[username.length()-1] == '\r' || username[username.length()-1] == '\n')) {
        username.erase(username.length() - 1);
    }
    if (!password.empty() && (password[password.length()-1] == '\r' || password[password.length()-1] == '\n')) {
        password.erase(password.length() - 1);
    }

    // Evaluate the cleaned strings using your exact custom credentials
    if (username == "Abdullah" && password == "12345678") {
        cout << "SUCCESS: Authenticated" << endl;
    } else {
        cout << "ERROR: Invalid username or password" << endl;
    }
}
    void add_book(string b_id, string b_title, string b_author) {
        if (total_books >= MAX) {
            cout << "ERROR: No space left for books!" << endl;
            return;
        }
        for (int i = 0; i < total_books; i++) {
            if (to_lowercase(book_list[i].id) == to_lowercase(b_id)) {
                cout << "ERROR: Book ID already exists!" << endl;
                return;
            }
        }

        book_list[total_books].id = b_id;
        book_list[total_books].title = b_title;
        book_list[total_books].author = b_author;
        book_list[total_books].is_issued = 0;
        total_books++;

        save_files();
        cout << "SUCCESS: Book added successfully!" << endl;
    }

    void view_books() {
        if (total_books == 0) {
            cout << "No books found." << endl;
            return;
        }
        for (int i = 0; i < total_books; i++) {
            cout << book_list[i].id << "|" 
                 << book_list[i].title << "|" 
                 << book_list[i].author << "|";
            if (book_list[i].is_issued == 1) {
                cout << "Issued" << endl;
            } else {
                cout << "Available" << endl;
            }
        }
    }

    void add_student(string s_id, string s_name, string s_dept) {
        if (total_students >= MAX) {
            cout << "ERROR: No space left for students!" << endl;
            return;
        }
        for (int i = 0; i < total_students; i++) {
            if (to_lowercase(student_list[i].id) == to_lowercase(s_id)) {
                cout << "ERROR: Student ID already exists!" << endl;
                return;
            }
        }

        student_list[total_students].id = s_id;
        student_list[total_students].name = s_name;
        student_list[total_students].department = s_dept;
        total_students++;

        save_files();
        cout << "SUCCESS: Student registered successfully!" << endl;
    }

    void view_students() {
        if (total_students == 0) {
            cout << "No students found." << endl;
            return;
        }
        for (int i = 0; i < total_students; i++) {
            cout << student_list[i].id << "|" 
                 << student_list[i].name << "|" 
                 << student_list[i].department << endl;
        }
    }

    void issue_book(string s_id, string b_id) {
        int book_index = -1;
        int student_index = -1;

        for (int i = 0; i < total_books; i++) {
            if (to_lowercase(book_list[i].id) == to_lowercase(b_id)) book_index = i;
        }
        for (int i = 0; i < total_students; i++) {
            if (to_lowercase(student_list[i].id) == to_lowercase(s_id)) student_index = i;
        }

        if (book_index == -1) {
            cout << "ERROR: Book not found!" << endl;
            return;
        }
        if (student_index == -1) {
            cout << "ERROR: Student not registered!" << endl;
            return;
        }
        if (book_list[book_index].is_issued == 1) {
            cout << "ERROR: Book is already with someone else!" << endl;
            return;
        }

        book_list[book_index].is_issued = 1;
        save_files();

        ofstream history("transactions.txt", ios::app);
        history << "ISSUED: '" << book_list[book_index].title << "' lent to " << student_list[student_index].name << "\n";
        history.close();

        cout << "SUCCESS: Book issued to " << student_list[student_index].name << "!" << endl;
    }

    void return_book(string b_id) {
        int book_index = -1;
        for (int i = 0; i < total_books; i++) {
            if (to_lowercase(book_list[i].id) == to_lowercase(b_id)) book_index = i;
        }

        if (book_index == -1) {
            cout << "ERROR: Book not found!" << endl;
            return;
        }
        if (book_list[book_index].is_issued == 0) {
            cout << "ERROR: This book was never issued!" << endl;
            return;
        }

        book_list[book_index].is_issued = 0;
        save_files();

        ofstream history("transactions.txt", ios::app);
        history << "RETURNED: Book ID [" << b_id << "] brought back to physical inventory.\n";
        history.close();

        cout << "SUCCESS: Book returned to shelves!" << endl;
    }

    void show_reports() {
        cout << "Total Books in Catalog: " << total_books << endl;
        cout << "Total Registered Scholars: " << total_students << endl;
        cout << "---------------------------------------" << endl;
        
        ifstream history("transactions.txt");
        if (!history) {
            cout << "No history logs found." << endl;
            return;
        }
        
        string record_line;
        while (getline(history, record_line)) {
            cout << record_line << endl;
        }
        history.close();
    }
};

// ==========================================
// 5. STABLE COMMAND-LINE BRIDGE INTERFACE
// ==========================================
// ==========================================
// 5. STABLE COMMAND-LINE BRIDGE INTERFACE
// ==========================================
int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "ERROR: No action specified." << endl;
        return 1;
    }

    LibrarySystem lib;
    string action = argv[1];

    if (action == "auth" && argc == 4) {
        lib.authenticate_user(argv[2], argv[3]);
    }
    else if (action == "add_book" && argc == 5) {
        lib.add_book(argv[2], argv[3], argv[4]);
    } 
    else if (action == "view_books") {
        lib.view_books();
    } 
    else if (action == "add_student" && argc == 5) {
        lib.add_student(argv[2], argv[3], argv[4]);
    } 
    else if (action == "view_students") {
        lib.view_students();
    } 
    else if (action == "issue_book" && argc == 4) {
        lib.issue_book(argv[2], argv[3]);
    } 
    else if (action == "return_book" && argc == 3) {
        lib.return_book(argv[2]);
    } 
    else if (action == "reports") {
        lib.show_reports();
    }

    return 0;
}
