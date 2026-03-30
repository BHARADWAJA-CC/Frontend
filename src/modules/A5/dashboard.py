import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:5005/api"


@st.cache_data
def fetch_patients():
    try:
        res = requests.get(f"{BASE_URL}/patients")
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return []


@st.cache_data
def fetch_dashboard(patient_id):
    try:
        res = requests.get(f"{BASE_URL}/dashboard/{patient_id}")
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return None


def show():
    st.title("Patient Dashboard")

    patients = fetch_patients()

    if not patients:
        st.warning("No patients found.")
        return

    # ── Patient selection ──
    options = {f"{p['Name']} ({p['PatientID']})": p for p in patients}
    selected = st.selectbox("Select Patient", list(options.keys()))

    if not selected:
        return

    patient = options[selected]

    # ── Fetch dashboard data ──
    data = fetch_dashboard(patient["PatientID"])

    if not data:
        st.error("Failed to fetch dashboard data.")
        return

    st.markdown("---")

    # ── KPI Metrics ──
    allergies = data.get("allergies", [])
    immunizations = data.get("immunizations", [])

    overdue = 0
    for imm in immunizations:
        if imm.get("NextDueDate"):
            if imm["NextDueDate"] < "2026-03-30":
                overdue += 1

    col1, col2, col3 = st.columns(3)
    col1.metric("Allergies", len(allergies))
    col2.metric("Immunizations", len(immunizations))
    col3.metric("Overdue Vaccines", overdue)

    st.markdown("---")

    # ── Simple Chart (NEW FEATURE) ──
    st.subheader("Immunization Trend")

    if immunizations:
        df = pd.DataFrame(immunizations)

        if "AdministrationDate" in df.columns:
            df["AdministrationDate"] = pd.to_datetime(df["AdministrationDate"])
            trend = df.groupby(df["AdministrationDate"].dt.date).size()

            st.line_chart(trend)
    else:
        st.info("No immunization data available.")