from flask import Flask, request, jsonify, render_template
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# IBM AI Granite API credentials
IBM_API_KEY = os.getenv("IBM_API_KEY")
if IBM_API_KEY is None:
    raise ValueError("Missing environment variable: IBM_API_KEY")

IBM_API_URL = os.getenv("IBM_API_URL")
if IBM_API_URL is None:
    raise ValueError("Missing environment variable: IBM_API_URL")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/enhance", methods=["POST"])
def enhance_resume():
    try:
        # Get the uploaded file and form data
        resume_file = request.files["resume"]
        job_title = request.form.get("job_title")
        job_description = request.form.get("job_description")

        # Validate inputs
        if not resume_file:
            return jsonify({"error": "Missing required field: resume"}), 400
        if not job_title:
            return jsonify({"error": "Missing required field: job_title"}), 400
        if not job_description:
            return jsonify({"error": "Missing required field: job_description"}), 400

        # Prepare the payload for IBM AI Granite API
        files = {"file": (resume_file.filename, resume_file.read(), resume_file.content_type)}
        data = {
            "job_title": job_title,
            "job_description": job_description
        }
        headers = {
            "Authorization": f"Bearer {IBM_API_KEY}"
        }

        # Call IBM AI Granite API and log the response
        response = requests.post(IBM_API_URL, files=files, data=data, headers=headers)
        print(f"API Response: {response.status_code} - {response.text}")
        if response.status_code != 200:
            print("Error details:", response.json())  # Log error details for debugging


        # Check if the API call was successful
        if response.status_code == 200:
            enhanced_resume = response.json().get("enhanced_resume")
            return jsonify({"enhanced_resume": enhanced_resume})
        else:
            return jsonify({"error": "Failed to enhance resume", "details": response.text}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # To run the app in production, use a WSGI server like Gunicorn or uWSGI:
    # Example command: gunicorn -w 4 app:app
    app.run(debug=True)
