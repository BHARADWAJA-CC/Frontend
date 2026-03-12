import streamlit as st
import requests
import home  

# Define backend connection constant
FLASK_API_URL = "http://127.0.0.1:5000/api"

# Page configuration
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
        st.markdown("Register a new patient into the clinic system.")
        
        # --- Connected Patient UI to Flask Backend ---
        with st.form("patient_registration_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("First Name *")
                dob = st.date_input("Date of Birth *")
                
            with col2:
                last_name = st.text_input("Last Name *")
                gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
            
            contact_number = st.text_input("Contact Number")
            st.caption("* denotes mandatory fields")
            
            submit_btn = st.form_submit_button("Register Patient")
            
            if submit_btn:
                # Basic frontend validation
                if not first_name or not last_name:
                    st.error("Please fill in the required name fields.")
                else:
                    # Construct REST API payload
                    payload = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "date_of_birth": dob.strftime("%Y-%m-%d"),
                        "gender": gender,
                        "contact_number": contact_number if contact_number else None
                    }
                    
                    try:
                        # Make HTTP POST request to Flask
                        with st.spinner("Registering patient in database..."):
                            response = requests.post(f"{FLASK_API_URL}/patients", json=payload)
                            
                            if response.status_code == 201:
                                res_data = response.json()
                                st.success(f"✅ {res_data['message']} (DB_ID: {res_data['patient_id']})")
                                st.balloons()
                            else:
                                st.error(f"❌ Failed to register patient: {response.json().get('message')}")
                                
                    except requests.exceptions.ConnectionError:
                        st.error("🚨 Critical Error: Could not connect to the Flask API. Is it running?")

    elif page == "Vaccines & Immunization":
        st.title("💉 Vaccines & Immunization")
        st.warning("Vaccine tracking and logging UI is under construction.")

if __name__ == "__main__":
    main()
