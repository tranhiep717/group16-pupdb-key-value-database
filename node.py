from pathlib import Path
import os
from flask import Flask, request, jsonify
from pupdb.core import PupDB

app = Flask(__name__)

NODE_ID = os.getenv("NODE_ID", "node1")
DATA_DIR = Path(__file__).with_name("data")
DATA_DIR.mkdir(exist_ok=True)

DB_FILE = DATA_DIR / f"{NODE_ID}.json"
db = PupDB(str(DB_FILE))


@app.route("/")
def home():
    return jsonify({
        "message": "Node is running",
        "node_id": NODE_ID,
        "db_file": str(DB_FILE)
    })


@app.route("/set", methods=["POST"])
def set_student():
    data = request.json
    student_id = data["student_id"]

    db.set(student_id, data)

    return jsonify({
        "message": "Saved to node",
        "node_id": NODE_ID,
        "student": data
    })


@app.route("/get/<student_id>", methods=["GET"])
def get_student(student_id):
    student = db.get(student_id)

    if student is None:
        return jsonify({"error": "Not found", "node_id": NODE_ID}), 404

    return jsonify({
        "node_id": NODE_ID,
        "student": student
    })


@app.route("/delete/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    if db.get(student_id) is None:
        return jsonify({"error": "Not found", "node_id": NODE_ID}), 404

    db.remove(student_id)

    return jsonify({
        "message": "Deleted from node",
        "node_id": NODE_ID
    })


@app.route("/all", methods=["GET"])
def get_all():
    return jsonify({
        "node_id": NODE_ID,
        "data": dict(db.items())
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    app.run(host="127.0.0.1", port=port, debug=True)