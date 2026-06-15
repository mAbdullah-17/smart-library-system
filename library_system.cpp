#include <iostream>
#include <fstream>
#include <string>
#include <sstream> // Used for simple space-splitting

using namespace std;

const int MAX = 50;

// ==========================================
// PILLAR 1: ENCAPSULATION 
// We bundle properties inside classes.
// ==========================================
class Book {
public:
    string id;
    string title;
    string author;
    int issued; // 0 = Available, 1 = Issued

    Book() {
        id = "";
        title = "";
        author = "";
        issued = 0;
    }
};

// ==========================================
// PILLAR 2: INHERITANCE
// 'Student' automatically gets 'id' and 'name' from 'Person'
// ==========================================
class Person {
public:
    string id;
    string name;

    // PILLAR 3: POLYMORPHISM
    // 'virtual' allows sub-classes to override this message later
    virtual void show_type() {
        cout << "Type: General Person" << endl;
    }
};

class Student : public Person {
public:
    string dept;

    // Overriding the base function to show custom student type
    void show_type() override {
        cout << "Type: Registered Student" << endl;
    }
};

// ==========================================
// PILLAR 4: ABSTRACTION
// The main system hides complex file management loops inside
// clean, easy-to-use function names.
// ==========================================
class LibrarySystem {
private:
    Book books[MAX];
    Student students[MAX];
    int book_count;
    int student_count;

public:
    LibrarySystem() {
        book_count = 0;
        student_count = 0;
        load_files();
    }

    // Abstracted function: Hidden details of reading data
    void load_files() {
        ifstream b_file("./books.txt");
        if (b_file) {
            string line;
            while (getline(b_file, line) && book_count < MAX) {
                if (line.empty()) continue;
                stringstream ss(line);
                ss >> books[book_count].id >> books[book_count].title >> books[book_count].author >> books[book_count].issued;
                book_count++;
            }
            b_file.close();
        }

        ifstream s_file("./students.txt");
        if (s_file) {
            string line;
            while (getline(s_file, line) && student_count < MAX) {
                if (line.empty()) continue;
                stringstream ss(line);
                ss >> students[student_count].id >> students[student_count].name >> students[student_count].dept;
                student_count++;
            }
            s_file.close();
        }
    }

    // Abstracted function: Hidden details of saving data
    void save_files() {
        ofstream b_file("./books.txt");
        for (int i = 0; i < book_count; i++) {
            b_file << books[i].id << " " << books[i].title << " " << books[i].author << " " << books[i].issued << "\n";
        }
        b_file.close();

        ofstream s_file("./students.txt");
        for (int i = 0; i < student_count; i++) {
            s_file << students[i].id << " " << students[i].name << " " << students[i].dept << "\n";
        }
        s_file.close();
    }

    void check_login(string user, string pass) {
        if (user == "Abdullah" && pass == "12345678") {
            cout << "SUCCESS: Authenticated" << endl;
        } else {
            cout << "ERROR: Invalid credentials" << endl;
        }
    }

    void add_book(string id, string title, string author) {
        if (book_count >= MAX) {
            cout << "ERROR: Full" << endl;
            return;
        }
        for (int i = 0; i < book_count; i++) {
            if (books[i].id == id) {
                cout << "ERROR: ID exists" << endl;
                return;
            }
        }

        books[book_count].id = id;
        books[book_count].title = title;
        books[book_count].author = author;
        books[book_count].issued = 0;
        book_count++;

        save_files();
        cout << "SUCCESS: Book added" << endl;
    }

    void show_books() {
        if (book_count == 0) {
            cout << "No books found." << endl;
            return;
        }
        for (int i = 0; i < book_count; i++) {
            cout << books[i].id << "|" << books[i].title << "|" << books[i].author << "|";
            if (books[i].issued == 1) cout << "Issued" << endl;
            else cout << "Available" << endl;
        }
    }

    void add_student(string id, string name, string dept) {
        if (student_count >= MAX) {
            cout << "ERROR: Full" << endl;
            return;
        }
        for (int i = 0; i < student_count; i++) {
            if (students[i].id == id) {
                cout << "ERROR: ID exists" << endl;
                return;
            }
        }

        students[student_count].id = id;
        students[student_count].name = name;
        students[student_count].dept = dept;
        student_count++;

        save_files();
        cout << "SUCCESS: Student registered" << endl;
    }

    void show_students() {
        if (student_count == 0) {
            cout << "No students found." << endl;
            return;
        }
        for (int i = 0; i < student_count; i++) {
            cout << students[i].id << "|" << students[i].name << "|" << students[i].dept << endl;
        }
    }

    void issue_book(string s_id, string b_id) {
        int b_idx = -1;
        int s_idx = -1;

        for (int i = 0; i < book_count; i++) {
            if (books[i].id == b_id) b_idx = i;
        }
        for (int i = 0; i < student_count; i++) {
            if (students[i].id == s_id) s_idx = i;
        }

        if (b_idx == -1 || s_idx == -1) {
            cout << "ERROR: Not found" << endl;
            return;
        }
        if (books[b_idx].issued == 1) {
            cout << "ERROR: Already issued" << endl;
            return;
        }

        books[b_idx].issued = 1;
        save_files();

        ofstream log("./transactions.txt", ios::app);
        if (log) {
            log << "ISSUED: " << books[b_idx].title << " to " << students[s_idx].name << "\n";
            log.close();
        }
        cout << "SUCCESS: Book issued" << endl;
    }

    void return_book(string b_id) {
        int b_idx = -1;
        for (int i = 0; i < book_count; i++) {
            if (books[i].id == b_id) b_idx = i;
        }

        if (b_idx == -1) {
            cout << "ERROR: Not found" << endl;
            return;
        }
        if (books[b_idx].issued == 0) {
            cout << "ERROR: Not issued" << endl;
            return;
        }

        books[b_idx].issued = 0;
        save_files();

        ofstream log("./transactions.txt", ios::app);
        if (log) {
            log << "RETURNED: Book " << b_id << " returned.\n";
            log.close();
        }
        cout << "SUCCESS: Book returned" << endl;
    }

    void show_reports() {
        cout << "Total Books in Catalog: " << book_count << endl;
        cout << "Total Registered Scholars: " << student_count << endl;
        cout << "---------------------------------------" << endl;
        
        ifstream log("./transactions.txt");
        if (log) {
            string line;
            while (getline(log, line)) {
                cout << line << endl;
            }
            log.close();
        }
    }
};

// ==========================================
// 5. COMMAND-LINE ROUTER
// ==========================================
int main(int argc, char* argv[]) {
    if (argc < 2) return 1;

    LibrarySystem lib;
    string action = argv[1];

    if (action == "auth" && argc == 4) {
        lib.check_login(argv[2], argv[3]);
    }
    else if (action == "add_book" && argc == 5) {
        lib.add_book(argv[2], argv[3], argv[4]);
    } 
    else if (action == "view_books") {
        lib.show_books();
    } 
    else if (action == "add_student" && argc == 5) {
        lib.add_student(argv[2], argv[3], argv[4]);
    } 
    else if (action == "view_students") {
        lib.show_students();
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
