from flask_cors import CORS
CORS(app, origins="https://your-shopify-store.myshopify.com")

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from any origin (for testing)

@app.route("/run-script", methods=["POST"])
def run_script():
    print("Script triggered")
    # Add your logic here
    return jsonify({"status": "done", "output": "Script completed!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


used_submissions = set()

@app.route("/run-script", methods=["POST"])
@limiter.limit("5 per minute")
def run_script():
    data = request.get_json()
    submission = data.get("submission")

    if not submission:
        return jsonify({"status": "error", "message": "No submission number"}), 400

    if submission in used_submissions:
        return jsonify({"status": "error", "message": "Submission already used"}), 403

    used_submissions.add(submission)

    # Simulate lookup
    result = {"info": f"Data for submission {submission}"}
    return jsonify({"status": "done", "output": result})

@app.before_request
def check_api_key():
    key = request.headers.get("X-API-KEY")
    if key != "abc123":
        return jsonify({"status": "unauthorized"}), 401


import time

@app.route("/run-script", methods=["POST"])
def run_script():
    log_file = "api_requests.log"
    with open(log_file, "a") as f:
        f.write(f"{time.time()} - {request.remote_addr} - {request.get_json()}\n")
