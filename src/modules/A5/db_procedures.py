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


# ---------------- ALLERGY ----------------
def insert_allergy(db, data):
    count = db.allergies.count_documents({})
    if "AllergyID" not in data:
        data["AllergyID"] = f"A{101 + count}"
    data["DiagnosisDate"] = datetime.now().strftime("%Y-%m-%d")
    db.allergies.insert_one(data)


# ---------------- CONTRAINDICATION ----------------
def insert_contraindication(db, data):
    count = db.contraindications.count_documents({})
    if "ContraindicationID" not in data:
        data["ContraindicationID"] = f"C{101 + count}"
    db.contraindications.insert_one(data)


# ---------------- CORE LOGIC ----------------
def check_contraindication(db, patient_id, vaccine_id):
    allergies = list(db.allergies.find({"PatientID": patient_id}, {"_id": 0}))
    contraindications = list(db.contraindications.find({"VaccineID": vaccine_id}, {"_id": 0}))

    for allergy in allergies:
        for contra in contraindications:
            if allergy["AllergyType"] == contra["AllergyType"]:
                return {
                    "blocked": True,
                    "reason": f"{allergy['AllergyType']} allergy conflict",
                    "details": contra
                }

    return {"blocked": False}


# ---------------- IMMUNIZATION ----------------
def insert_immunization(db, data):
    vaccine = db.vaccines.find_one({"VaccineID": data["VaccineID"]})
    
    # Calculate dose number
    patient_doses = list(db.immunizations.find({"PatientID": data["PatientID"], "VaccineID": data["VaccineID"]}))
    dose_number = len(patient_doses) + 1
    
    data["DoseNumber"] = dose_number
    # Basic generated ID
    data["ImmunizationID"] = f"{data['VaccineID']}_{data['PatientID']}_{dose_number}"

    next_date = None
    if vaccine:
        next_date = datetime.now() + timedelta(days=30 * vaccine["IntervalMonths"])

    data["NextDueDate"] = next_date.strftime("%Y-%m-%d") if next_date else None
    data["AdministrationDate"] = datetime.now().strftime("%Y-%m-%d")

    db.immunizations.insert_one(data)

# ---------------- ADVERSE REACTION ----------------
def insert_adverse_reaction(db, data):
    # Ensure ID generation or use provided ID
    db.adverse_reactions.insert_one(data)

# ---------------- DASHBOARD AGGREGATION ----------------
def get_patient_dashboard_data(db, patient_id):
    patient = db.patients.find_one({"PatientID": patient_id}, {"_id": 0})
    if not patient:
        return None

    allergies = list(db.allergies.find({"PatientID": patient_id}, {"_id": 0}))
    immunizations = list(db.immunizations.find({"PatientID": patient_id}, {"_id": 0}))
    reactions = list(db.adverse_reactions.find({"PatientID": patient_id}, {"_id": 0}))

    # Since datetime isn't directly serializable in basic Flask if we don't handle it
    # We will let the frontend or Flask's JSON provider handle stringification
    return {
        "patient": patient,
        "allergies": allergies,
        "immunizations": immunizations,
        "reactions": reactions
    }
