from datetime import datetime, timedelta

# ---------------- PATIENT ----------------
def insert_patient(db, data):
    count = db.patients.count_documents({})
    if "PatientID" not in data:
        data["PatientID"] = f"P{101 + count}"
    db.patients.insert_one(data)


# ---------------- VACCINE ----------------
def insert_vaccine(db, data):
    count = db.vaccines.count_documents({})
    if "VaccineID" not in data:
        data["VaccineID"] = f"V{101 + count}"
    db.vaccines.insert_one(data)
