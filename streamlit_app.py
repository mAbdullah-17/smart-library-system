import streamlit as st
import api

st.set_page_config(page_title="Library Console Hub", page_icon="📚", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- SYSTEM ACCESS INTERFACE ---
if not st.session_state.logged_in:
    st.title("🔐 Secure Administration Entry Node")
    st.markdown("### Authentication verified dynamically via isolated C++ runtime layers.")
    user = st.text_input("Admin ID String")
    password = st.text_input("Security Access Key", type="password")
    
    if st.button("Transmit to Core Validation Engine"):
        if api.verify_login(user, password):
            st.session_state.logged_in = True
            st.success("Access authorized.")
            st.rerun()
        else:
            st.error("Access validation handshake failure in C++ execution scope.")
else:
    # --- PHYSICAL VIEW DESK LAYOUT ---
    st.sidebar.title("Operational Links")
    page = st.sidebar.radio("Console Tracks", [
        "Dashboard Overview", "Catalog New Book Asset", "Database Visual Inventory", 
        "Register Scholar Node", "Scholar Profile Indexes", "Circulation Desk", "Logs & Audit History",
        "Open Library Engine Sync", "AI Context Advisory"
    ])
    
    if st.sidebar.button("Terminate Session Profile"):
        st.session_state.logged_in = False
        st.rerun()

    st.title(f"📂 Operational Terminal: {page}")
    st.divider()

    if page == "Dashboard Overview":
        st.markdown("### Control Metrics Hub")
        # Visual Analytics Integration
        c_books = api.view_books()
        c_studs = api.view_students()
        
        col1, col2 = st.columns(2)
        col1.metric(label="Total Cataloged Assets Array Count", value=len(c_books))
        col2.metric(label="Total Active Scholar Node Footprints", value=len(c_studs))
        
        st.info("System execution framework functioning standard. Business operations map fully to C++ logic branches.")

    elif page == "Catalog New Book Asset":
        with st.form("b_form"):
            b_id = st.text_input("Unique Book Barcode Code")
            title = st.text_input("Asset Title Header")
            author = st.text_input("Lead Author Metadata")
            if st.form_submit_button("Commit Changes to Hardware Registers"):
                output = api.add_book(b_id, title, author)
                st.info(output)

    elif page == "Database Visual Inventory":
        books_data = api.view_books()
        if books_data: st.table(books_data)
        else: st.warning("Null context records array stack.")

    elif page == "Register Scholar Node":
        with st.form("s_form"):
            s_id = st.text_input("Scholar Identity Registry Code")
            name = st.text_input("Complete Identity Character Name")
            dept = st.text_input("Enrolled Department Major")
            if st.form_submit_button("Verify and Write Profile Block"):
                output = api.add_student(s_id, name, dept)
                st.info(output)

    elif page == "Scholar Profile Indexes":
        students_data = api.view_students()
        if students_data: st.table(students_data)
        else: st.warning("Null structural student array elements.")

    elif page == "Circulation Desk":
        tab1, tab2 = st.tabs(["Lend Allocation Linkage", "Receive Restructure Log"])
        with tab1:
            sid = st.text_input("Target Scholar ID Code", key="isid")
            bid = st.text_input("Target Book ID Barcode", key="ibid")
            if st.button("Process Dispatch Execution Log"):
                st.info(api.issue_book(sid, bid))
        with tab2:
            rbid = st.text_input("Target Book ID Barcode", key="rbid")
            if st.button("Process Return Ingestion Array"):
                st.info(api.return_book(rbid))

    elif page == "Logs & Audit History":
        logs = api.get_reports()
        st.text_area("C++ System Buffer Log Stream Stream Dump", value=logs, height=300)

    elif page == "Open Library Engine Sync":
        query = st.text_input("Query Global Web Repository Matrix")
        if query:
            st.write(api.search_open_library(query))

    elif page == "AI Context Advisory":
        key = st.text_input("OpenAI Secure Bearer Key Token Input String", type="password")
        target_b = st.text_input("Target Analytical Target Volume Name")
        if st.button("Execute Cloud Model Synthesis Pipeline"):
            st.markdown(api.get_ai_summary(target_b, key))