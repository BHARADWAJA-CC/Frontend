# ================== 1. SCHEMA CREATION (March 3) ==================

def create_core_tables(cursor):
    """
    Executes raw SQL to create the core tables. 
    The execution is managed externally by db_connection or flask_app.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Patients (
            patient_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            date_of_birth DATE NOT NULL,
            gender ENUM('Male', 'Female', 'Other') NOT NULL,
            contact_number VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Vaccines (
            vaccine_id INT AUTO_INCREMENT PRIMARY KEY,
            vaccine_name VARCHAR(100) NOT NULL UNIQUE,
            manufacturer VARCHAR(100) NOT NULL,
            recommended_doses INT DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Immunizations (
            record_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            vaccine_id INT NOT NULL,
            administered_date DATE NOT NULL,
            dose_number INT DEFAULT 1,
            provider_name VARCHAR(100),
            FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
            FOREIGN KEY (vaccine_id) REFERENCES Vaccines(vaccine_id) ON DELETE RESTRICT
        );
    """)

# ================== 2. STORED PROCEDURES (March 8) ==================

def setup_stored_procedures(cursor):
    """
    Deploys the Stored Procedures to the MySQL database.
    """
    
    # --- Register Patient Procedure ---
    cursor.execute("DROP PROCEDURE IF EXISTS RegisterPatient;")
    cursor.execute("""
        CREATE PROCEDURE RegisterPatient(
            IN p_first_name VARCHAR(100),
            IN p_last_name VARCHAR(100),
            IN p_dob DATE,
            IN p_gender VARCHAR(10),
            IN p_contact VARCHAR(20),
            OUT p_new_patient_id INT
        )
        BEGIN
            INSERT INTO Patients (first_name, last_name, date_of_birth, gender, contact_number)
            VALUES (p_first_name, p_last_name, p_dob, p_gender, p_contact);
            
            -- Capture the auto-incremented ID to return to Flask
            SET p_new_patient_id = LAST_INSERT_ID();
        END;
    """)

    # --- Register Vaccine Procedure ---
    cursor.execute("DROP PROCEDURE IF EXISTS RegisterVaccine;")
    cursor.execute("""
        CREATE PROCEDURE RegisterVaccine(
            IN p_vaccine_name VARCHAR(100),
            IN p_manufacturer VARCHAR(100),
            IN p_doses INT,
            OUT p_new_vaccine_id INT
        )
        BEGIN
            INSERT INTO Vaccines (vaccine_name, manufacturer, recommended_doses)
            VALUES (p_vaccine_name, p_manufacturer, p_doses);
            
            SET p_new_vaccine_id = LAST_INSERT_ID();
        END;
    """)
