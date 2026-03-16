import streamlit as st
import requests
import time
from config import BASE_URL

def show():
    st.markdown("""
    <h2 style='margin-bottom:4px;'>
      <i class='fa-solid fa-syringe' style='color:#00d2ff'></i> Add Vaccine Template
    </h2>
    <div style='color:#a0a0b0; margin-bottom:20px;'>Define a new vaccine type to be available for patient immunization tracking.</div>
    """, unsafe_allow_html=True)

    with st.form("add_vaccine_form", clear_on_submit=True):
        name = st.text_input("Vaccine Name", placeholder="e.g. MMR, COVID-19 mRNA, Varicella")
        
        c1, c2 = st.columns(2)
        with c1:
            doses = st.number_input("Total Required Doses", min_value=1, max_value=10, value=1)
        with c2:
            interval = st.number_input("Interval Between Doses (Months)", min_value=0, max_value=120, value=1)

        submit = st.form_submit_button("Register Vaccine", type="primary")

        if submit:
            if not name.strip():
                st.error("❌ Vaccine Name is required.")
            else:
                payload = {
                    "VaccineName": name.strip(),
                    "TotalRequiredDoses": int(doses),
                    "IntervalMonths": int(interval)
                }
                
                with st.spinner("Registering..."):
                    try:
                        res = requests.post(f"{BASE_URL}/vaccines", json=payload, timeout=15)
                        if res.status_code == 200:
                            v_id = res.json().get("VaccineID", "Unknown ID")
                            st.success(f"✅ Vaccine '{name}' successfully registered! ID: {v_id}")
                        else:
                            st.error(f"❌ Failed to add vaccine: {res.text}")
                    except Exception as e:
                        st.error(f"❌ API Request failed: {e}")