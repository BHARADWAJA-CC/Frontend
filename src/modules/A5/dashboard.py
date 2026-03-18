import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:5005/api"


def fetch_patients():
    try:
        res = requests.get(f"{BASE_URL}/patients")
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return []


def show():
    st.title("Patient Dashboard")

    patients = fetch_patients()

    if not patients:
        st.warning("No patients found.")
        return

    st.subheader("System Overview")

    col1, col2 = st.columns(2)
    col1.metric("Total Patients", len(patients))
    col2.metric("System Status", "Online")

    st.markdown("---")

    st.subheader("Patient List")

    for p in patients:
        st.write(f"{p['Name']} (ID: {p['PatientID']})")