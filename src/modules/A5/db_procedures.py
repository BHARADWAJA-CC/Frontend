import mysql.connector

# Note: In a real project, these credentials would be imported from config.py 
# or fetched via environment variables (like os.getenv)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "clinic_db"
}

def create_core_tables(cursor):
    """
    Creates the initial database schema, core tables, and basic constraints.
    """
    
    # 1. Patients Table
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
    
    # 2. Vaccines Inventory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Vaccines (
            vaccine_id INT AUTO_INCREMENT PRIMARY KEY,
            vaccine_name VARCHAR(100) NOT NULL UNIQUE,
            manufacturer VARCHAR(100) NOT NULL,
            recommended_doses INT DEFAULT 1,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 3. Immunization Records (Joining logic to test FK constraints)
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

    print("✅ Core schema initialized: Patients, Vaccines, and Immunization tables verified.")

def initialize_schema():
    """Establishes connection and runs the schema creation."""
    try:
        # Connect to MySQL Server wrapper
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Execute table creation
        create_core_tables(cursor)
        
        # Commit the transaction
        conn.commit()
        
    except mysql.connector.Error as err:
        print(f"❌ Database Schema Error: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    print("Running initial database setup...")
    initialize_schema()
import mysql.connector

# Note: In a real project, these credentials would be imported from config.py 
# or fetched via environment variables (like os.getenv)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "clinic_db"
}

def create_core_tables(cursor):
    """
    Creates the initial database schema, core tables, and basic constraints.
    """
    
    # 1. Patients Table
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
    
    # 2. Vaccines Inventory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Vaccines (
            vaccine_id INT AUTO_INCREMENT PRIMARY KEY,
            vaccine_name VARCHAR(100) NOT NULL UNIQUE,
            manufacturer VARCHAR(100) NOT NULL,
            recommended_doses INT DEFAULT 1,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 3. Immunization Records (Joining logic to test FK constraints)
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

    print("✅ Core schema initialized: Patients, Vaccines, and Immunization tables verified.")

def initialize_schema():
    """Establishes connection and runs the schema creation."""
    try:
        # Connect to MySQL Server wrapper
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Execute table creation
        create_core_tables(cursor)
        
        # Commit the transaction
        conn.commit()
        
    except mysql.connector.Error as err:
        print(f"❌ Database Schema Error: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    print("Running initial database setup...")
    initialize_schema()
