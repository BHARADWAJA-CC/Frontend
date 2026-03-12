import logging
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get("MONGO_URI")

if not uri:
    logging.error("MONGO_URI not provided in environment variables.")
    raise RuntimeError("MONGO_URI not provided")


from pymongo import MongoClient

# Use a server selection timeout so operations fail fast if DB is unreachable
client = MongoClient(uri, serverSelectionTimeoutMS=5000)

try:
    # Force a connection check on startup — will raise if DB unreachable within timeout
    client.server_info()
    db = client["ClinicalCDS_A5"]

    patients = db["patients"]
    allergies = db["allergies"]
    vaccines = db["vaccines"]
    immunizations = db["immunizations"]
    adverse_reactions = db["adverse_reactions"]
    contraindications = db["contraindications"]

    logging.info("Connected to MongoDB successfully")
except Exception as e:
    logging.exception("Failed to connect to MongoDB: %s", e)
    # Fail fast: raise so backend startup is aware. This avoids requests hanging later.
    raise

def get_db():
    return db
