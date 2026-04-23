import os

# During deployment, the runner script will set this environment variable.
# For standard local development, it defaults to the 5005 port.
FLASK_URL = os.environ.get("FLASK_URL", "http://127.0.0.1:5005")
BASE_URL = f"{FLASK_URL}/api"