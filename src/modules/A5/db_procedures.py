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
    # [2026-04-11 Bharadwaj] Simulated Foreign Key Constraint
    patient_id = str(data.get("PatientID", "")).strip()
    if not db.patients.find_one({"PatientID": patient_id}):
        raise ValueError(f"Foreign key constraint failed: PatientID '{patient_id}' does not exist.")
        
    data["PatientID"] = patient_id
    db.allergies.insert_one(data)

# ---------------- CONTRAINDICATION (Added Mar 20)----------------
def insert_contraindication(db, data):
    # [2026-04-11 Bharadwaj] Simulated Foreign Key Constraint
    patient_id = str(data.get("PatientID", "")).strip()
    vaccine_id = str(data.get("VaccineID", "")).strip()
    
    if not db.patients.find_one({"PatientID": patient_id}):
        raise ValueError(f"Foreign key constraint failed: PatientID '{patient_id}' does not exist.")
    if not db.vaccines.find_one({"VaccineID": vaccine_id}):
        raise ValueError(f"Foreign key constraint failed: VaccineID '{vaccine_id}' does not exist.")
    
    count = db.contraindications.count_documents({})
    if "ContraindicationID" not in data:
        data["ContraindicationID"] = f"C{101 + count}"
        
    data["PatientID"] = patient_id
    data["VaccineID"] = vaccine_id
    db.contraindications.insert_one(data)

def check_contraindication(db, patient_id, vaccine_id):
    # Fixed parameter binding issues here to ensure clean lookups
    patient_id = str(patient_id).strip()
    vaccine_id = str(vaccine_id).strip()
    
    contra = db.contraindications.find_one({
        "PatientID": patient_id, 
        "VaccineID": vaccine_id
    })
    
    if contra:
        return {"blocked": True, "reason": contra.get("Reason", "Unknown Reason")}
    return {"blocked": False}

# ---------------- IMMUNIZATION (Added Mar 23) ----------------
def insert_immunization(db, data):
    # [2026-04-11 Bharadwaj] Simulated Foreign Key Constraint
    patient_id = str(data.get("PatientID", "")).strip()
    vaccine_id = str(data.get("VaccineID", "")).strip()
    
    if not db.patients.find_one({"PatientID": patient_id}):
        raise ValueError(f"Foreign key constraint failed: PatientID '{patient_id}' does not exist.")
    if not db.vaccines.find_one({"VaccineID": vaccine_id}):
        raise ValueError(f"Foreign key constraint failed: VaccineID '{vaccine_id}' does not exist.")
        
    data["PatientID"] = patient_id
    data["VaccineID"] = vaccine_id
    db.immunizations.insert_one(data)

# ---------------- ADVERSE REACTION (Added Mar 28) ----------------
def insert_adverse_reaction(db, data):
    # [2026-04-11 Bharadwaj] Simulated Foreign Key Constraint
    patient_id = str(data.get("PatientID", "")).strip()
    if not db.patients.find_one({"PatientID": patient_id}):
        raise ValueError(f"Foreign key constraint failed: PatientID '{patient_id}' does not exist.")
        
    data["PatientID"] = patient_id
    db.adverse_reactions.insert_one(data)

# =====================================================================
# ⭐ SHOWCASE & DASHBOARD OPTIMIZATIONS (April 6 Commit)
# =====================================================================

def get_vaccination_stats(db):
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
    patient_id = str(patient_id).strip()
    patient = db.patients.find_one({"PatientID": patient_id}, {"_id": 0})
    if not patient: return None
    
    patient["immunizations"] = list(db.immunizations.find({"PatientID": patient_id}, {"_id": 0}))
    patient["allergies"] = list(db.allergies.find({"PatientID": patient_id}, {"_id": 0}))
    patient["reactions"] = list(db.adverse_reactions.find({"PatientID": patient_id}, {"_id": 0}))
    return patient
