import streamlit as st
import requests
import home  

# Define backend connection constant
FLASK_API_URL = "http://127.0.0.1:5005/api"

# Page configuration
st.set_page_config(
    page_title="Clinic Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initializes global session variables to prevent data loss on page switches."""
    if 'current_patient_id' not in st.session_state:
        st.session_state.current_patient_id = None
    if 'last_action_status' not in st.session_state:
        st.session_state.last_action_status = ""

def apply_standard_custom_css():
    """Injects custom CSS to standardize form layouts and buttons across the app."""
    st.markdown("""
        <style>
        /* Standardize Form Borders and Padding */
        div[data-testid="stForm"] {
            border: 1px solid #e0e4eb;
            border-radius: 8px;
            padding: 25px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
        }
        /* Make submit buttons full width and uniform */
        .stButton>button {
            width: 100%;
            border-radius: 6px;
            font-weight: 600;
            background-color: #0068c9;
            color: white;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #0052a3;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    # Setup state and UI layout rules
    initialize_session_state()
    apply_standard_custom_css()
    
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
        st.info("Interactive dashboard visualizations are currently being integrated by Dipesh.")
        
    elif page == "Patient Management":
        st.title("🧑‍⚕️ Patient Management")
        st.markdown("Register a new patient into the clinic system.")
        
        # --- Standardized Patient Form ---
        with st.form("patient_registration_form"):
            st.subheader("Patient Details")
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("First Name *")
                dob = st.date_input("Date of Birth *")
                
            with col2:
                last_name = st.text_input("Last Name *")
                gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
            
            contact_number = st.text_input("Contact Number", placeholder="e.g., +1 555-0100")
            st.caption("* denotes mandatory fields")
            
            # Standardized submit button
            submit_btn = st.form_submit_button("🩺 Register Patient Record")
            
            if submit_btn:
                if not first_name or not last_name:
                    st.error("Please fill in the required name fields.")
                else:
                    payload = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "date_of_birth": dob.strftime("%Y-%m-%d"),
                        "gender": gender,
                        "contact_number": contact_number if contact_number else None
                    }
                    
                    try:
                        with st.spinner("Connecting to database..."):
                            response = requests.post(f"{FLASK_API_URL}/patients", json=payload)
                            
                            if response.status_code in [200, 201]:
                                res_data = response.json()
                                st.success(f"✅ Patient Registered Successfully!")
                                
                                # Store newly created ID in session state so it can be used on other pages
                                st.session_state.current_patient_id = res_data.get('PatientID')
                                st.balloons()
                            else:
                                st.error(f"❌ Failed to register patient: {response.json().get('error', 'Unknown Error')}")
                                
                    except requests.exceptions.ConnectionError:
                        st.error("🚨 Critical Error: Could not connect to the Flask API. Ensure the backend is running on port 5005.")

    elif page == "Vaccines & Immunization":
        st.title("💉 Vaccines & Immunization")
        st.markdown("Log immunizations and manage clinical vaccine inventory.")
        # We can implement the standardized form for vaccines here later
        st.info("Vaccine tracking UI is mapped to backend but pending final UI styling.")

if __name__ == "__main__":
    main()
