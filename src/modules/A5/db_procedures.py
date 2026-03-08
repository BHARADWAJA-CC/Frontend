import os
import mysql.connector
from mysql.connector import pooling
from datetime import datetime, timedelta

# ================== CONFIG ==================
# You can later move this to config.py
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "clinic_db"
}

# ================== CONNECTION POOL ==================

class DatabaseConnectionPool:
    """
    Singleton wrapper class for managing a MySQL Connection Pool.
    """
    _instance = None
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnectionPool, cls).__new__(cls)
            cls._instance._initialize_pool()
        return cls._instance

    def _initialize_pool(self):
        pool_name = "clinic_app_pool"
        pool_size = int(os.environ.get("DB_POOL_SIZE", 5))

        try:
            print(f"Initializing DB Connection Pool (Size: {pool_size})...")
            self._pool = pooling.MySQLConnectionPool(
                pool_name=pool_name,
                pool_size=pool_size,
                pool_reset_session=True,
                **DB_CONFIG
            )
            print("✅ Database Connection Pool initialized.")
        except mysql.connector.Error as err:
            print(f"🛑 Failed to create connection pool: {err}")
            raise

    def get_connection(self):
        try:
            return self._pool.get_connection()
        except mysql.connector.PoolError as err:
            print(f"⚠️ Pool exhausted: {err}")
            return None
        except mysql.connector.Error as err:
            print(f"⚠️ Database error: {err}")
            return None


# Global instance
db_pool = DatabaseConnectionPool()

def get_db_connection():
    return db_pool.get_connection()


# ================== SCHEMA CREATION ==================

def create_core_tables(cursor):
    """
    Creates core tables for the clinic system.
    """
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

    # Immunizations Table
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

    print("✅ Core schema initialized.")


def initialize_schema():
    """
    Uses connection pool to initialize schema.
    """
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("No DB connection available")

        cursor = conn.cursor()

        create_core_tables(cursor)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"❌ Schema Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()  # returns connection to pool


# ================== ENTRY POINT ==================

if __name__ == "__main__":
    print("🚀 Running initial database setup...")
    initialize_schema()