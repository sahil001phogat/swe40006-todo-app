from flask import Flask, jsonify
from datetime import datetime
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Hello from my Dockerized Flask app!",
        "hostname": socket.gethostname(),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    # Bind to 0.0.0.0 so it's reachable from outside the container
    app.run(host="0.0.0.0", port=5000)
