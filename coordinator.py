import hashlib
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

NODES = [
    "http://127.0.0.1:5001",
    "http://127.0.0.1:5002",
    "http://127.0.0.1:5003"
]


def get_node(student_id):
    hash_value = int(hashlib.md5(student_id.encode()).hexdigest(), 16)
    index = hash_value % len(NODES)
    return NODES[index]


@app.route("/")
def home():
    return jsonify({
        "message": "Coordinator is running",
        "nodes": NODES
    })


@app.route("/set", methods=["POST"])
def set_student():
    data = request.json
    student_id = data["student_id"]

    node = get_node(student_id)

    response = requests.post(
        f"{node}/set",
        json=data
    )

    return jsonify({
        "message": "Student routed successfully",
        "student_id": student_id,
        "target_node": node,
        "response": response.json()
    })


@app.route("/get/<student_id>", methods=["GET"])
def get_student(student_id):
    node = get_node(student_id)

    response = requests.get(
        f"{node}/get/{student_id}"
    )

    return jsonify({
        "student_id": student_id,
        "target_node": node,
        "response": response.json()
    }), response.status_code


@app.route("/delete/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    node = get_node(student_id)

    response = requests.delete(
        f"{node}/delete/{student_id}"
    )

    return jsonify({
        "student_id": student_id,
        "target_node": node,
        "response": response.json()
    }), response.status_code


@app.route("/all", methods=["GET"])
def get_all_students():
    result = {}

    for node in NODES:
        try:
            response = requests.get(f"{node}/all")
            result[node] = response.json()
        except requests.exceptions.RequestException:
            result[node] = {
                "error": "Node unavailable"
            }

    return jsonify({
        "message": "Distributed query completed",
        "data": result
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)