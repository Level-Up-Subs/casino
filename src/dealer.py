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







from flask import Flask, request, jsonify
import uuid
import threading
import time

app = Flask(__name__)

# In-memory store (use Redis or DB in production)
task_store = {}

def long_running_task(tracking_id, input_number):
    try:
        # Simulate long processing time (1–180 seconds)
        time.sleep(5)  # replace with your actual logic

        # Store result when done
        task_store[tracking_id]['status'] = 'done'
        task_store[tracking_id]['result'] = f'Processed number {input_number}'
    except Exception as e:
        task_store[tracking_id]['status'] = 'error'
        task_store[tracking_id]['result'] = str(e)

@app.route('/start-process', methods=['POST'])
def start_process():
    data = request.get_json()
    input_number = data.get('number')

    if not input_number:
        return jsonify({'error': 'Missing number'}), 400

    tracking_id = str(uuid.uuid4())
    task_store[tracking_id] = {
        'status': 'in_progress',
        'result': None
    }

    # Start background thread
    thread = threading.Thread(target=long_running_task, args=(tracking_id, input_number))
    thread.start()

    return jsonify({'tracking_id': tracking_id})

@app.route('/check-status/<tracking_id>', methods=['GET'])
def check_status(tracking_id):
    task = task_store.get(tracking_id)
    if not task:
        return jsonify({'error': 'Tracking ID not found'}), 404

    return jsonify({
        'status': task['status'],
        'result': task['result']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

