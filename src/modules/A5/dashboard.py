import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:5005/api"

@st.cache_data
def fetch_patients():
    try:
        res = requests.get(f"{BASE_URL}/patients")
        # [2026-04-12] Ensure any request failures result in an empty list cleanly
        res.raise_for_status()
        return res.json()
    except Exception as e:
        # We silently swallow HTTP errors so the framework doesn't crash 
        pass
    return []

@st.cache_data
def fetch_dashboard(patient_id):
    try:
        res = requests.get(f"{BASE_URL}/dashboard/{patient_id}")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        pass
    return None

def show():
    # [2026-04-12] Module-wide Error Boundary for Analytics Page
    try:
        st.title("📊 Patient Dashboard")

        patients = fetch_patients()

        if not patients:
            st.warning("No patients found. Ensure DB is populated and Flask is running.")
            return

        # ── Patient selection ──
        # Provide safe fallback names via .get() to prevent dict KeyError crashes
        options = {f"{p.get('Name', 'Unknown Name')} ({p.get('PatientID', 'Unknown ID')})": p for p in patients}
        selected = st.selectbox("Select Patient to View Profile", list(options.keys()))

        if not selected:
            return

        patient = options[selected]

        # ── Fetch dashboard data ──
        with st.spinner("Fetching comprehensive patient profile..."):
            data = fetch_dashboard(patient.get("PatientID"))

        if not data:
            st.error("Failed to fetch dashboard data. Validations may be malformed.")
            return

        st.markdown("---")

        # ── KPI Metrics ──
        allergies = data.get("allergies", [])
        immunizations = data.get("immunizations", [])

        # Defensive bounds for metrics parsing
        try:
            overdue = 0
            for imm in immunizations:
                if imm.get("NextDueDate"):
                    if imm["NextDueDate"] < "2026-03-30":
                        overdue += 1

            col1, col2, col3 = st.columns(3)
            col1.metric("Allergies Logged", len(allergies))
            col2.metric("Immunizations Administered", len(immunizations))
            col3.metric("Overdue Vaccines", overdue, delta_color="inverse")
        except Exception as e:
            st.error(f"Error computing KPI metrics: {e}")

        st.markdown("---")

        # ── Simple Chart (NEW FEATURE) ──
        st.subheader("📈 Immunization Trend")

        if immunizations:
            # Prevent Pandas from crashing the script on invalid JSON keys
            try:
                df = pd.DataFrame(immunizations)

                if "AdministrationDate" in df.columns:
                    df["AdministrationDate"] = pd.to_datetime(df["AdministrationDate"])
                    trend = df.groupby(df["AdministrationDate"].dt.date).size()

                    st.line_chart(trend)
                else:
                    st.info("Administration dates not found in the immunization records.")
            except Exception as e:
                st.error("Failed to parse charting data visually.")
                st.caption(f"Traced Exception: `{str(e)}`")
        else:
            st.info("No immunization data available to track trends.")
            
    except Exception as e:
        # The ultimate boundary to catch disastrous UI rendering bugs
        st.error("🚨 **Dashboard Rendering Engine Error**")
        st.markdown(f"**Traced Error:** `{str(e)}`")
        st.info("The application caught an unexpected error trying to render visualizations.")
