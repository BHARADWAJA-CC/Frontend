from flask import Flask, jsonify

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

if __name__ == '__main__':
    # Run the app in debug mode on port 5000
    app.run(debug=True, port=5000)
