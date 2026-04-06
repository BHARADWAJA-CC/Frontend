import streamlit as st

def show():
    st.markdown("""
    <h2 style='margin-bottom:4px;'>
      <i class='fa-solid fa-database' style='color:#00d2ff'></i> SQL Query Showcase
    </h2>
    <div style='color:#a0a0b0; margin-bottom:20px;'>Demonstrating the SQL equivalents of our backend logic. Since we are using MongoDB, these represent what the operations would look like in a standard Relational DB.</div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧍 Fetch Patient Details")
    st.code("""
        SELECT * 
        FROM patients 
        WHERE PatientID = 'P101';
    """, language="sql")

    st.markdown("### ⚠️ Fetch Patient Allergies")
    st.code("""
        SELECT * 
        FROM allergies 
        WHERE PatientID = 'P101';
    """, language="sql")

    st.markdown("### 💉 Fetch Immunization History")
    st.code("""
        SELECT * 
        FROM immunizations 
        WHERE PatientID = 'P101';
    """, language="sql")

    st.markdown("### 🛡️ Check Contraindications")
    st.code("""
        SELECT c.*
        FROM contraindications c
        JOIN allergies a 
        ON c.AllergenName = a.AllergyName
        WHERE a.PatientID = 'P101'
        AND c.VaccineID = 'V101';
    """, language="sql")

    st.markdown("### 📅 Calculate Next Due Date")
    st.code("""
        SELECT DATE_ADD(AdministrationDate, INTERVAL IntervalMonths MONTH)
        FROM vaccines
        WHERE VaccineID = 'V101';
    """, language="sql")

    st.markdown("### 📊 Herd Immunity Calculation")
    st.code("""
        SELECT 
            COUNT(DISTINCT PatientID) * 100.0 / 
            (SELECT COUNT(*) FROM patients) AS HerdImmunityPercentage
        FROM immunizations;
    """, language="sql")
