import streamlit as st

def render_home_page():
    """
    Renders the main landing page for the application.
    """
    st.title("Welcome to the Clinic Management System 🏥")
    st.markdown("---")
    
    st.markdown("""
    ### Project Overview
    This is our DBMS Group Project designed to handle patient records, 
    manage vaccine inventory, and track immunization history securely.
    
    ##### Current Development Status:
    * ✅ Database Schema Initialized (Bharadwaj)
    * ✅ Flask Backend Stubbed (Dipesh)
    * ✅ Streamlit Application Configured (Aditya)
    * ⏳ Core API Endpoints in Progress
    """)
    
    # Use columns to mock up a starting layout
    c1, c2 = st.columns(2)
    
    with c1:
        st.success("Frontend UI framework successfully connected.")
        
    with c2:
        st.info("Note: Please ensure the Flask app is currently running on `localhost:5000`")
