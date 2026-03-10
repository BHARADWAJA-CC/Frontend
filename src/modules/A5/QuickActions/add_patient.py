import streamlit as st
import requests
import time
from requests.exceptions import Timeout, RequestException
from config import BASE_URL
import datetime

def safe_post(url, json_data, timeout=30):
    try:
        res = requests.post(url, json=json_data, timeout=timeout)
        if res.status_code in (200, 201):
            try:
                return {"success": True, "data": res.json()}
            except Exception:
                return {"success": True, "data": None}
        else:
            try:
                return {"success": False, "error": res.json()}
            except Exception:
                return {"success": False, "error": res.text}
    except Timeout:
        return {"success": False, "error": "Request timed out"}
    except RequestException as e:
        return {"success": False, "error": str(e)}

def show():
    st.markdown("""
    <h2 style='margin-bottom:4px;'>
      <i class='fa-solid fa-user-plus' style='color:#00d2ff'></i> Add Patient
    </h2>
    <div style='color:#a0a0b0; margin-bottom:20px;'>Register a new patient into the system.</div>
    """, unsafe_allow_html=True)

    with st.form("add_patient_form", clear_on_submit=True):
        name = st.text_input("Full Name", placeholder="e.g. John Doe")
        
        c1, c2 = st.columns(2)
        with c1:
            dob = st.date_input(
                "Date of Birth",
                min_value=datetime.date(1900, 1, 1),
                max_value=datetime.date.today()
            )
        with c2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        submit = st.form_submit_button("Register Patient", type="primary")

        if submit:
            if not name.strip():
                st.error("❌ Patient Name is required.")
            else:
                with st.spinner("Registering..."):
                    resp = safe_post(f"{BASE_URL}/patients", json_data={
                        "Name": name.strip(),
                        "DateOfBirth": str(dob),
                        "Gender": gender
                    }, timeout=30)

                if resp.get("success"):
                    pid = None
                    try:
                        pid = resp.get("data", {}).get("PatientID")
                    except Exception:
                        pass
                    st.success(f"✅ Patient added{f' with ID: {pid}' if pid else ''}")
                else:
                    st.error(f"❌ Failed to add patient: {resp.get('error')}")