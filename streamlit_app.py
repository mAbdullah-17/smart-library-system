import streamlit as st
import api

# 1. PAGE CONFIGURATION & THEME INJECTION
st.set_page_config(
    page_title="Smart Library System", 
    page_icon="📚", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS injection to match the dark slate navigation and clean grid cards
st.markdown("""
    <style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1e293b !important;
    }
    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }
    /* Metric block card layouts */
    div[data-testid="stMetricSimpleValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    .metric-card {
        background-color: #f8fafc;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    /* Buttons customization */
    .stButton>button {
        background-color: #2563eb !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
    }
    /* Text alignment helper */
    .centered-text {
        text-align: center !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SYSTEM SESSION CONTROLS ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- DEPLOYMENT SECURITY ACCESS PORTAL ---
if not st.session_state.logged_in:
    # 🟢 CENTERED FIX: Creating a 3-column structural layout wrapper grid matrix
    left_spacer, center_card, right_spacer = st.columns([1, 1.5, 1])
    
    # Push all login input elements strictly inside the center column grid focus area
    with center_card:
        st.markdown("<h1 class='centered-text'>🔐 Admin Login Page</h1>", unsafe_allow_html=True)
        st.markdown("<p class='centered-text'>Authentication verified via C++ in Backend.</p>", unsafe_allow_html=True)
        st.write("") # Structural padding gap space spacer
        
        # Injected interactive login field panels
        user = st.text_input("Admin ID")
        password = st.text_input("Password", type="password")
        st.write("") # Structural padding gap space spacer
        
        if st.button("Login", use_container_width=True):
            if api.verify_login(user, password):
                st.session_state.logged_in = True
                st.success("Welcome Admin!")
                st.rerun()
            else:
                st.error("Access validation handshake failure in C++ execution scope.")

else:
    # --- ENTERPRISE SIDEBAR NAVIGATION DESK ---
    with st.sidebar:
        st.markdown("## 📚 Smart Library")
        st.markdown(f"**Logged in as:** `Admin` 🟢")
        st.divider()
        
        # Simple navigation tracks matching the visual reference asset panel layout exactly
        page = st.radio("Navigation Tracks", [
            "Dashboard", 
            "Add Book", 
            "View Books", 
            "Add Student", 
            "View Students", 
            "Issue Book", 
            "Return Book", 
            "Reports",
            "Online Search", 
            "AI Book Advisor"
        ], label_visibility="collapsed")
        
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # --- ACTION EXECUTIVE LOGIC ROUTERS ---
    
    # PAGE 1: MAIN METRICS DASHBOARD
    if page == "Dashboard":
        st.title("Dashboard")
        st.markdown("Welcome back, Admin!")
        
        # Pulling active real-time data from your C++ core database layers
        c_books = api.view_books()
        c_studs = api.view_students()
        
        # Calculate total count dynamically
        total_books_count = len(c_books)
        total_students_count = len(c_studs)
        
        # Count how many books have a status of "Issued" in your system
        issued_books_count = sum(1 for book in c_books if book.get("status") == "Issued")
        available_books_count = total_books_count - issued_books_count
        
        # 4-Column Metric Counter Layout Configuration
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric(label="Total Books", value=total_books_count, delta="All books in library")
        with m2:
            st.metric(label="Total Students", value=total_students_count, delta="Registered profiles")
        with m3:
            st.metric(label="Issued Books", value=issued_books_count, delta="Currently outstanding")
        with m4:
            st.metric(label="Available Books", value=available_books_count, delta="On shelves")
            
        st.divider()
        st.subheader("Recent Transactions")
        
        # Render clean system logs summary dataframe matrix directly below metrics
        raw_reports = api.get_reports()
        if raw_reports and not raw_reports.startswith("ERROR"):
            st.text_area("Live System Transaction Operations Log Monitor", value=raw_reports, height=250)
        else:
            st.info("System execution framework stable. No transactional log frames committed inside this buffer scope yet.")

    # PAGE 2: ASSET REGISTRY MANAGEMENT INGESTION FORM
    elif page == "Add Book":
        st.title("Add New Book")
        with st.form("add_book_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                b_id = st.text_input("Book ID")
                title = st.text_input("Title")
                author = st.text_input("Author")
            with col2:
                category = st.selectbox("Category", ["Programming", "Computer Science", "Database Systems", "Software Engineering", "Mathematics"])
                publisher = st.text_input("Publisher")
                quantity = st.number_input("Quantity", min_value=1, value=5, step=1)
                
            if st.form_submit_button("Add Book", use_container_width=True):
                if b_id and title and author:
                    output = api.add_book(b_id, title, author)
                    st.success("Book added successfully!")
                else:
                    st.warning("Please fill in all required fields (Book ID, Title, Author).")

    # PAGE 3: VISUAL DATABASE REPOSITORY TABLES
    elif page == "View Books":
        st.title("View Books")
        books_data = api.view_books()
        if books_data:
            st.dataframe(books_data, use_container_width=True, hide_index=True)
            st.metric(label="Total Books", value=len(books_data))
        else:
            st.warning("No books found in the database.")

    # PAGE 4: SCHOLAR IDENTITY BLOCK REGISTRY INGESTION FORM
    elif page == "Add Student":
        st.title("Add Student")
        with st.form("add_student_form", clear_on_submit=True):
            s_id = st.text_input("Student ID")
            name = st.text_input("Name")
            dept = st.text_input("Department")
            
            if st.form_submit_button("Add New Student", use_container_width=True):
                if s_id and name and dept:
                    output = api.add_student(s_id, name, dept)
                    st.success("Student added successfully!")
                else:
                    st.warning("All fields are required to register a student.")

    # PAGE 5: SCHOLAR INDEX DATABASE VISUAL CHANNELS
    elif page == "View Students":
        st.title("View Students")
        students_data = api.view_students()
        if students_data:
            st.dataframe(students_data, use_container_width=True, hide_index=True)
            st.metric(label="Total Students", value=len(students_data))
        else:
            st.warning("No students found in the database.")

    # PAGE 6: CIRCULATION DESK LEND INTERFACES
    elif page == "Issue Book":
        st.title("Issue Book")
        with st.form("issue_form"):
            sid = st.text_input("Student ID")
            bid = st.text_input("Book ID")
            if st.form_submit_button("Issue Book", use_container_width=True):
                if sid and bid:
                    st.info(api.issue_book(sid, bid))
                else:
                    st.error("Please enter both Student ID and Book ID.")

    # PAGE 7: CIRCULATION DESK RETURN INTERFACES
    elif page == "Return Book":
        st.title("Return Book")
        with st.form("return_form"):
            rbid = st.text_input("Book ID")
            if st.form_submit_button("Return Book", use_container_width=True):
                if rbid:
                    st.info(api.return_book(rbid))
                else:
                    st.error("Please enter a Book ID.")

    # PAGE 8: COMPREHENSIVE RECONCILIATION REPORTS
    elif page == "Reports":
        st.title("Reports")
        logs = api.get_reports()
        st.text_area("System Logs & Audit History", value=logs, height=500)

    # PAGE 9: GLOBAL HTTPS OPEN LIBRARY SYNC CHANNELS
    elif page == "Online Search":
        st.title("Online Search (Open Library)")
        query = st.text_input("Search Book")
        if st.button("Search", use_container_width=True):
            if query:
                with st.spinner("Searching Open Library..."):
                    web_results = api.search_open_library(query)
                    if web_results and "Error" not in web_results[0]:
                        st.success("Book found on Open Library!")
                        st.dataframe(web_results, use_container_width=True, hide_index=True)
                    elif web_results and "Error" in web_results[0]:
                        st.error(web_results[0]["Error"])
                    else:
                        st.warning("No book found matching that title.")

    # PAGE 10: CONTEXT SYNTHESIS PIPELINE CHANNELS (GROQ LLAMA FREE API TIER)
    elif page == "AI Book Advisor":
        st.title("AI Book Advisor (Groq)")
        target_b = st.text_input("Enter Book Title")
        if st.button("Get AI Recommendation", use_container_width=True):
            if target_b:
                with st.spinner("Getting recommendation..."):
                    summary = api.get_ai_summary(target_b)
                    if "ERROR" in summary:
                        st.error(summary)
                    else:
                        st.success("AI Recommendation:")
                        st.info(summary)
            else:
                st.warning("Please type a book title first.")

    # SOLID STEADY FOOTER INTERFACE DISPLAY
    st.markdown("---")
    st.caption("Smart Library Management System | C++ OOP Project Backend")
