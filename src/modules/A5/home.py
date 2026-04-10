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
            
        # Dynamically detecting the .streamlit/secrets.toml file implementation
        try:
            # Assuming you mapped variables like ENV or DB_HOST in your secrets file
            app_env = st.secrets.get("ENV", "Development")
            st.caption(f"🔧 **System Environment:** `{app_env}` Mode (Managed via `.streamlit/secrets.toml`)")
        except Exception:
            # Safe fallback just in case the secrets file is empty locally
            st.caption("🔧 **System Environment:** `Development` Mode")
        
    with col_status:
        st.markdown("### Development Status")
        # Refined UI Styling using custom CSS injected borders and shadows
        st.markdown(
            """
            <div style="border: 1px solid #e0e4eb; background-color: #fafbfc; border-radius: 8px; padding: 20px; box-shadow: 0px 4px 6px rgba(0,0,0,0.04);">
                <ul style="list-style-type: none; padding-left: 0; line-height: 1.8;">
                    <li>✅ <b>Database Core:</b> Deployed</li>
                    <li>✅ <b>REST API:</b> Online</li>
                    <li>✅ <b>Forms & Layouts:</b> Standardized</li>
                    <li>✅ <b>Secure Config:</b> <code>.streamlit</code> Active</li>
                    <li>⏳ <b>Dashboard:</b> Final Validations</li>
                </ul>
            </div>
            """, unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Status check row
    c1, c2 = st.columns(2)
    with c1:
        st.info("💡 **Tip:** Use the sidebar to navigate to Patient Management and see how Session State persists data.")
        
    with c2:
        st.warning("⚠️ **System Check:** Ensure the Flask backend is actively running on port `5005`")
