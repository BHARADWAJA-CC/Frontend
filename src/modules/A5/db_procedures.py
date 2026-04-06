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

# ---------------- ALLERGY (Added Mar 20) ----------------
def insert_allergy(db, data):
    db.allergies.insert_one(data)

# ---------------- CONTRAINDICATION (Added Mar 20)----------------
def insert_contraindication(db, data):
    count = db.contraindications.count_documents({})
    if "ContraindicationID" not in data:
        data["ContraindicationID"] = f"C{101 + count}"
    db.contraindications.insert_one(data)

def check_contraindication(db, patient_id, vaccine_id):
    contra = db.contraindications.find_one({
        "PatientID": patient_id, 
        "VaccineID": vaccine_id
    })
    if contra:
        return {"blocked": True, "reason": contra.get("Reason", "Unknown Reason")}
    return {"blocked": False}

# ---------------- IMMUNIZATION (Added Mar 23) ----------------
def insert_immunization(db, data):
    db.immunizations.insert_one(data)

# ---------------- ADVERSE REACTION (Added Mar 28) ----------------
def insert_adverse_reaction(db, data):
    db.adverse_reactions.insert_one(data)

# =====================================================================
# ⭐ SHOWCASE & DASHBOARD OPTIMIZATIONS (April 6 Commit)
# Equivalent to complex JOINs using MongoDB Aggregation ($lookup)
# =====================================================================

def get_vaccination_stats(db):
    """
    Aggregation: Joins Vaccines with Immunizations to count doses administered.
    """
    pipeline = [
        {
            "$lookup": {
                "from": "immunizations",
                "localField": "VaccineID",
                "foreignField": "VaccineID",
                "as": "doses"
            }
        },
        {
            "$project": {
                "VaccineID": 1,
                "VaccineName": "$Name",  
                "TotalAdministered": { "$size": "$doses" }
            }
        },
        { "$sort": { "TotalAdministered": -1 } }
    ]
    return list(db.vaccines.aggregate(pipeline))

def get_patient_reaction_history(db, patient_id):
    """
    Aggregation: Joins Patients, Immunizations, and Adverse Reactions.
    """
    pipeline = [
        { "$match": { "PatientID": patient_id } },
        {
            "$lookup": {
                "from": "adverse_reactions",
                "localField": "PatientID",
                "foreignField": "PatientID",
                "as": "reactions"
            }
        }
    ]
    return list(db.patients.aggregate(pipeline))

def get_patient_dashboard_data(db, patient_id):
    """Compiles a complete profile for the dashboard view."""
    patient = db.patients.find_one({"PatientID": patient_id}, {"_id": 0})
    if not patient: return None
    
    patient["immunizations"] = list(db.immunizations.find({"PatientID": patient_id}, {"_id": 0}))
    patient["allergies"] = list(db.allergies.find({"PatientID": patient_id}, {"_id": 0}))
    patient["reactions"] = list(db.adverse_reactions.find({"PatientID": patient_id}, {"_id": 0}))
    return patient
