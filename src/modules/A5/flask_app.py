from flask import Flask, request, jsonify
from flask_cors import CORS
from db_connection import get_db
from db_procedures import *

app = Flask(__name__)
# [2026-03-25] Dipesh: Fixed CORS issues
CORS(app) 

db = get_db()

# ---------------- PATIENT (March 12) ----------------
@app.route('/api/patients', methods=['GET'])
def get_patients():
    try:
        return jsonify(list(db.patients.find({}, {"_id": 0})))
    except:
        return jsonify({"error": "Failed"}), 500


@app.route('/api/patients', methods=['POST'])
def add_patient():
    data = request.json
    if not data.get("Name"):
        return jsonify({"error": "Name required"}), 400

    try:
        insert_patient(db, data)
        return jsonify({"message": "Added", "PatientID": data.get("PatientID")})
    except Exception as e:
        return jsonify({"error": f"Database insertion failed: {str(e)}"}), 500


# ---------------- VACCINE (March 16) ----------------
@app.route('/api/vaccines', methods=['GET'])
def get_vaccines():
    return jsonify(list(db.vaccines.find({}, {"_id": 0})))


@app.route('/api/vaccines', methods=['POST'])
def add_vaccine():
    try:
        insert_vaccine(db, request.json)
        return jsonify({"message": "Added", "VaccineID": request.json.get("VaccineID")})
    except Exception as e:
        return jsonify({"error": f"Database insertion failed: {str(e)}"}), 500


# ---------------- ALLERGY (March 20) ----------------
@app.route('/api/allergies', methods=['POST'])
def add_allergy():
    try:
        insert_allergy(db, request.json)
        return jsonify({"message": "Added"})
    except Exception as e:
        return jsonify({"error": f"Database insertion failed: {str(e)}"}), 500


# ---------------- CONTRAINDICATION (March 20) ----------------
@app.route('/api/contraindications', methods=['POST'])
def add_contra():
    try:
        insert_contraindication(db, request.json)
        return jsonify({"message": "Added", "ContraindicationID": request.json.get("ContraindicationID")})
    except Exception as e:
        return jsonify({"error": f"Database insertion failed: {str(e)}"}), 500


# ⭐ CHECK
@app.route('/api/check_contraindication', methods=['POST'])
def check_contra():
    data = request.json
    result = check_contraindication(db, data["PatientID"], data["VaccineID"])
    return jsonify(result)


# ---------------- IMMUNIZATION (March 23) ----------------
@app.route('/api/immunizations', methods=['POST'])
def add_immunization():
    data = request.json

    try:
        result = check_contraindication(db, data["PatientID"], data["VaccineID"])

        if result["blocked"]:
            return jsonify({"error": "Blocked", "details": result}), 400

        insert_immunization(db, data)
        return jsonify({"message": "Added"})
    except Exception as e:
        return jsonify({"error": f"Database insertion failed: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(port=5005, debug=True)

# ---------------- ALLERGY (March 20) ----------------
@app.route('/api/allergies', methods=['GET'])
def get_allergies():
    """Fetch all allergies from the database."""
    try:
        return jsonify(list(db.allergies.find({}, {"_id": 0})))
    except Exception as e:
        return jsonify({"error": f"Failed to fetch allergies: {str(e)}"}), 500


@app.route('/api/allergies', methods=['POST'])
def add_allergy():
    try:
        insert_allergy(db, request.json)
        return jsonify({"message": "Added"})
    except Exception as e:
        return jsonify({"error": f"Database insertion failed: {str(e)}"}), 500


# ---------------- CONTRAINDICATION (March 20) ----------------
@app.route('/api/contraindications', methods=['GET'])
def get_contraindications():
    """Fetch all contraindications from the database."""
    try:
        return jsonify(list(db.contraindications.find({}, {"_id": 0})))
    except Exception as e:
        return jsonify({"error": f"Failed to fetch contraindications: {str(e)}"}), 500


@app.route('/api/contraindications', methods=['POST'])
def add_contra():
    try:
        insert_contraindication(db, request.json)
        return jsonify({"message": "Added", "ContraindicationID": request.json.get("ContraindicationID")})
    except Exception as e:
        return jsonify({"error": f"Database insertion failed: {str(e)}"}), 500
