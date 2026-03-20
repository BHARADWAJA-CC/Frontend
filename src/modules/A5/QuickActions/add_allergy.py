import streamlit as st
import requests
from config import BASE_URL

def show():
    # Defensive check
    if not st.session_state.get("patient_id"):
        st.warning("No active patient. Please select a patient from the Dashboard.")
        return

    patient_id = st.session_state.patient_id
    patient_name = st.session_state.patient_name

    st.markdown(f"""
    <h2 style='margin-bottom:4px;'>
      <i class='fa-solid fa-triangle-exclamation' style='color:#00d2ff'></i> Add Allergy
    </h2>
    <div style='color:#a0a0b0; margin-bottom:20px;'>Record a new allergy for <strong>{patient_name}</strong> (ID: {patient_id}).</div>
    """, unsafe_allow_html=True)

    with st.form("add_allergy_form", clear_on_submit=True):
        name = st.text_input("Allergy Name", placeholder="e.g. Penicillin, Peanut, Latex")
        c1, c2 = st.columns(2)
        with c1:
            allergy_type = st.selectbox("Allergy Type", ["Drug", "Food", "Environmental", "Latex", "Other"])
        with c2:
            severity = st.selectbox("Severity", ["Mild", "Moderate", "Severe", "Anaphylaxis"])
        
        submitted = st.form_submit_button("Record Allergy", type="primary")
        
        if submitted:
            if not name.strip():
                st.error("Allergy Name is required.")
            else:
                payload = {
                    "PatientID": patient_id,
                    "AllergyName": name.strip(),
                    "AllergyType": allergy_type,
                    "SeverityLevel": severity,
                    "Status": "Active" # default
                }
                
                with st.spinner("Saving allergy..."):
                    try:
                        res = requests.post(f"{BASE_URL}/allergies", json=payload, timeout=15)
                        if res.status_code == 200:
                            st.success("✅ Allergy successfully recorded.")
                        else:
                            st.error(f"❌ Error adding allergy: {res.text}")
                    except Exception as e:
                        st.error(f"❌ Request failed: {e}")
