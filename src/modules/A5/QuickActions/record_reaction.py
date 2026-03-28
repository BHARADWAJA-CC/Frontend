import streamlit as st
import requests
from config import BASE_URL
import datetime

def show():
    # Defensive check
    if not st.session_state.get("patient_id"):
        st.warning("No active patient. Please select a patient from the Dashboard.")
        return

    patient_id = st.session_state.patient_id
    patient_name = st.session_state.patient_name

    st.markdown(f"""
    <h2 style='margin-bottom:4px;'>
      <i class='fa-solid fa-heart-crack' style='color:#00d2ff'></i> Record Adverse Reaction
    </h2>
    <div style='color:#a0a0b0; margin-bottom:20px;'>Link an adverse reaction to a previous immunization for <strong>{patient_name}</strong>.</div>
    """, unsafe_allow_html=True)

    # Fetch immunizations for this patient to link the reaction
    with st.spinner("Fetching immunization history..."):
        try:
            res = requests.get(f"{BASE_URL}/dashboard/{patient_id}", timeout=15)
            if res.status_code != 200:
                st.error("Could not fetch patient's immunization history.")
                return
            data = res.json()
        except Exception as e:
            st.error(f"Request failed: {e}")
            return
        
    patient_immunizations = data.get("immunizations", [])

    if not patient_immunizations:
        st.warning("No immunizations found for this patient. Reactions must be linked to an immunization.")
        return

    immu_options = {
        f"💉 {i['VaccineID']} | Administered: {i.get('AdministrationDate', 'N/A')}": i['VaccineID'] 
        for i in patient_immunizations
    }

    selected_immu_label = st.selectbox("Select Associated Immunization", options=list(immu_options.keys()), index=None)

    if not selected_immu_label:
        return

    vaccine_id = immu_options[selected_immu_label]

    with st.form("reaction_form", clear_on_submit=True):
        desc = st.text_area("Reaction Description", placeholder="Describe the adverse reaction...")
        
        c1, c2 = st.columns(2)
        with c1:
            sev = st.selectbox("Severity", ["Mild", "Moderate", "Severe"])
        with c2:
            date = st.date_input(
                "Reaction Date",
                min_value=datetime.date(1900, 1, 1),
                max_value=datetime.date.today()
            )
            
        act = st.text_input("Action Taken", placeholder="e.g. Administered Epinephrine, Observed for 30m")
        
        submit = st.form_submit_button("Record Reaction", type="primary")
        
        if submit:
            if not desc.strip():
                st.error("Reaction description is required.")
            else:
                payload = {
                    "PatientID": patient_id,
                    "VaccineID": vaccine_id,
                    "ReactionDescription": desc.strip(),
                    "ReactionDate": date.strftime("%Y-%m-%d"),
                    "SeverityLevel": sev,
                    "ActionTaken": act.strip()
                }
                
                with st.spinner("Saving..."):
                    try:
                        res = requests.post(f"{BASE_URL}/adverse_reactions", json=payload, timeout=15)
                        if res.status_code == 200:
                            st.success("✅ Adverse reaction successfully recorded.")
                        else:
                            st.error(f"❌ Error recording reaction: {res.text}")
                    except Exception as e:
                        st.error(f"❌ Request failed: {e}")
