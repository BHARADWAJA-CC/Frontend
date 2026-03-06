import streamlit as st
import home  # Importing the newly created home module

# Page config must be the very first Streamlit command
st.set_page_config(
    page_title="Clinic Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # --- Sidebar Setup ---
    st.sidebar.title("🏥 Clinic Navigation")
    st.sidebar.markdown("---")
    
    # Simple navigation structure for early development
    page = st.sidebar.radio(
        "Select a Module:",
        (
            "Home Overview", 
            "Analytics Dashboard", 
            "Patient Management", 
            "Vaccines & Immunization"
        )
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("DBMS Project - Dipesh, Bharadwaj, and Aditya")

    # --- Routing Logic ---
    if page == "Home Overview":
        home.render_home_page()
        
    elif page == "Analytics Dashboard":
        st.title("📊 System Dashboard")
        st.info("Dashboard visualizations will be implemented here by Dipesh.")
        
    elif page == "Patient Management":
        st.title("🧑‍⚕️ Patient Management")
        st.warning("Patient registration and records UI is under construction.")
        
    elif page == "Vaccines & Immunization":
        st.title("💉 Vaccines & Immunization")
        st.warning("Vaccine tracking and logging UI is under construction.")

if __name__ == "__main__":
    main()
