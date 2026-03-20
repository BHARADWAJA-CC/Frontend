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
    st.markdown("""
    <h2 style='margin-bottom:4px;'>
      <i class='fa-solid fa-ban' style='color:#00d2ff'></i> Add Contraindication
    </h2>
    <div style='color:#a0a0b0; margin-bottom:20px;'>Link a vaccine to an allergy type to define clinical conflicts.</div>
    """, unsafe_allow_html=True)

    vaccines = fetch_vaccines()
    if not vaccines:
        st.warning("No vaccines found. Please add a vaccine first.")
        return

    vaccine_options = {f"💉 {v['VaccineName']} (ID: {v['VaccineID']})": v['VaccineID'] for v in vaccines}

    with st.form("add_contraindication_form", clear_on_submit=True):
        selected_vaccine_label = st.selectbox("Select Vaccine", options=list(vaccine_options.keys()), index=None)
        allergy_type = st.selectbox("Conflict Allergy Type", ["Drug", "Food", "Latex", "Environmental", "Other"])
        obs = st.text_area("Clinical Observation / Reason", placeholder="E.g. Vaccine contains traces of latex.")

        submit = st.form_submit_button("Log Contraindication Rule", type="primary")

        if submit:
            if not selected_vaccine_label:
                st.error("❌ Please select a vaccine.")
            elif not obs.strip():
                st.error("❌ Clinical Observation is required.")
            else:
                payload = {
                    "VaccineID": vaccine_options[selected_vaccine_label],
                    "AllergyType": allergy_type,
                    "Observation": obs.strip()
                }
                
                with st.spinner("Saving rule..."):
                    try:
                        res = requests.post(f"{BASE_URL}/contraindications", json=payload, timeout=15)
                        if res.status_code == 200:
                            c_id = res.json().get("ContraindicationID", "Unknown ID")
                            st.success(f"✅ Safety rule successfully added! (ID: {c_id})")
                        else:
                            st.error(f"❌ Failed to add rule: {res.text}")
                    except Exception as e:
                        st.error(f"❌ API Request failed: {e}")