import streamlit as st

def render_home_page():
    """Renders the main landing page for the application."""
    
    st.title("Welcome to the Clinic Management System 🏥")
    st.markdown("---")
    
    # Standardized layout for the welcome page
    col_main, col_status = st.columns([2, 1])
    
    with col_main:
        st.markdown("""
        ### Project Overview
        Welcome to the team DBMS Group Project. This interactive portal is designed to safely handle patient records, track intricate vaccine inventory, and flag contraindications during immunization events.
        
        Navigate using the sidebar to explore the different database interactions and functional modules.
        """)
        
        # Checking Session State on the Home Page
        if 'current_patient_id' in st.session_state and st.session_state.current_patient_id:
            st.success(f"📌 **Active Session Data:** Currently tracking Patient ID: `{st.session_state.current_patient_id}`")
        
    with col_status:
        st.markdown("### Development Status")
        st.markdown(
            """
            <div style="background-color: #f0f2f6; border-radius: 8px; padding: 15px;">
                <ul style="list-style-type: none; padding-left: 0;">
                    <li>✅ <b>Database Core:</b> Deployed</li>
                    <li>✅ <b>REST API:</b> Online</li>
                    <li>✅ <b>Patient/Vaccine Forms:</b> Active</li>
                    <li>✅ <b>Form Layouts:</b> Standardized</li>
                    <li>⏳ <b>Dashboard:</b> Pending Data Hookup</li>
                </ul>
            </div>
            """, unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Status check row
    c1, c2 = st.columns(2)
    with c1:
        st.info("💡 **Tip:** Use the sidebar to add a patient and check how session state persists the Patient ID.")
        
    with c2:
        st.warning("⚠️ **Backend Check:** Ensure the Flask app is currently running on `localhost:5005`")
