from flask import Flask, jsonify, request
import db_connection  # Imports the database pool logic

app = Flask(__name__)

@app.route('/')
def home():
    """Root endpoint to verify the API is running."""
    return jsonify({
        "status": "success",
        "message": "Flask backend API initialized successfully"
    })

@app.route('/api/health')
def health_check():
    """Basic health check endpoint."""
    return jsonify({
        "status": "healthy"
    })

# ================== PATIENT ENDPOINTS ==================

@app.route('/api/patients', methods=['POST'])
def add_patient():
    """API endpoint to insert a new patient into MySQL Database."""
    data = request.json
    
    # Extract data from request payload
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    dob = data.get('date_of_birth')
    gender = data.get('gender')
    contact = data.get('contact_number')

    # Data validation
    if not all([first_name, last_name, dob, gender]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    # Fetch connection from the pool
    conn = db_connection.get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        # Secure parameterized query to avoid SQL Injection
        query = """
            INSERT INTO Patients (first_name, last_name, date_of_birth, gender, contact_number)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (first_name, last_name, dob, gender, contact))
        
        # Commit the transaction to disk
        conn.commit()
        
        # Grab the auto-incremented primary key
        patient_id = cursor.lastrowid
        
        return jsonify({
            "status": "success", 
            "message": "Patient added successfully", 
            "patient_id": patient_id
        }), 201

    except Exception as e:
        # Rollback in case of failure
        if 'conn' in locals() and conn:
            conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
        
    finally:
        # Safely close cursors and return connection back to pool map
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close() 


if __name__ == '__main__':
    # Run the app in debug mode on port 5000
    app.run(debug=True, port=5000)
