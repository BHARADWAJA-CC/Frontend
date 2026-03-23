import streamlit as st
import requests
import time
from config import BASE_URL

@st.cache_data(ttl=60)
def fetch_vaccines():
    try:
        res = requests.get(f"{BASE_URL}/vaccines", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return []

def show():
    # Defensive check
    if not st.session_state.get("patient_id"):
        st.warning("No active patient. Please select a patient from the Dashboard.")
        return

    patient_id = st.session_state.patient_id
    patient_name = st.session_state.patient_name

    st.markdown(f"""
    <h2 style='margin-bottom:4px;'>
      <i class='fa-solid fa-shield-virus' style='color:#00d2ff'></i> Add Immunization & Safety Check
    </h2>
    <div style='color:#a0a0b0; margin-bottom:20px;'>Administer a vaccine to <strong>{patient_name}</strong> (ID: {patient_id}).</div>
    """, unsafe_allow_html=True)

    vaccines = fetch_vaccines()
    if not vaccines:
        st.warning("No vaccines found in the system. Please register a vaccine first.")
        return

    vaccine_options = {f"💉 {v['VaccineName']} | ID: {v['VaccineID']}": v['VaccineID'] for v in vaccines}
    selected_vaccine_label = st.selectbox("Select Vaccine", options=list(vaccine_options.keys()), index=None)

    if not selected_vaccine_label:
        return

    vaccine_id = vaccine_options[selected_vaccine_label]

    # Use normal button for the check so we can render warnings dynamically outside form
    if st.button("Check Contraindications"):
        with st.spinner("Analyzing clinical safety..."):
            time.sleep(0.5) # Simulate deep check for UX purposes
            try:
                payload = {"PatientID": patient_id, "VaccineID": vaccine_id}
                res = requests.post(f"{BASE_URL}/check_contraindication", json=payload, timeout=15)
                if res.status_code == 200:
                    result = res.json()
                    if result.get("blocked"):
                        st.session_state.check_status = "blocked"
                        st.session_state.block_reason = result.get('reason')
                    else:
                        st.session_state.check_status = "safe"
                else:
                    st.error("Error communicating with clinical safety engine.")
                    return
            except Exception as e:
                st.error(f"Error: {e}")
                return

    if st.session_state.check_status == "blocked":
        st.error(f"### 🛑 CONTRAINDICATION DETECTED\n**Safety Alert:** {st.session_state.block_reason}\n\n*System strictly recommends against administering this vaccine.*")
        st.warning("To proceed anyway under clinical override, use the force submit option below.")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("❌ Cancel (Recommended)", use_container_width=True):
                st.session_state.check_status = "pending"
                st.rerun()

        with c2:
            if st.button("⚠️ Proceed Anyway (Override)", type="primary", use_container_width=True):
                st.session_state.check_status = "safe"
                st.rerun()

    if st.session_state.check_status == "safe":
        st.success("✅ Clinical Safety Check Passed. No contraindications detected.")
        
        st.markdown("---")
        st.markdown("### Administer Dose")
        
        with st.form("immunization_form", clear_on_submit=True):
            st.info(f"Adding dose for **{patient_name}** using **{selected_vaccine_label}**")
            
            submit = st.form_submit_button("Confirm & Record Immunization", type="primary")
            
            if submit:
                payload = {
                    "PatientID": patient_id,
                    "VaccineID": vaccine_id,
                }
                with st.spinner("Recording immunization..."):
                    try:
                        res = requests.post(f"{BASE_URL}/immunizations", json=payload, timeout=15)
                        if res.status_code == 200:
                            st.success("✅ Immunization successfully recorded!")
                            st.session_state.check_status = "pending"
                            st.balloons()
                        elif res.status_code == 400:
                            st.error(f"❌ Backend logically rejected this submission: {res.json().get('error')} - {res.json().get('details', {}).get('reason')}")
                        else:
                            st.error(f"❌ Error: {res.text}")
                    except Exception as e:
                        st.error(f"❌ Request failed: {e}")
