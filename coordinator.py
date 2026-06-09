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

# --- API CHO QUẢN LÝ REPLICATION VÀ FAILOVER ---

@app.route("/status", methods=["GET"])
def get_status():
    """Lấy trạng thái của toàn bộ các Node (Shard)"""
    result = {}
    for i, node in enumerate(NODES):
        try:
            # Lấy thông tin record_count và primary_failed
            r_all = requests.get(f"{node}/all")
            r_home = requests.get(f"{node}/")
            
            all_data = r_all.json()
            home_data = r_home.json()
            
            result[f"shard_{i}"] = {
                "node_url": node,
                "record_count": all_data.get("record_count", 0),
                "primary_failed": home_data.get("primary_failed", False)
            }
        except requests.exceptions.RequestException:
             result[f"shard_{i}"] = {
                "node_url": node,
                "error": "Node unavailable"
            }
             
    return jsonify({
        "message": "Shard status retrieved",
        "shards": result
    })

@app.route("/simulate_error/<int:node_index>", methods=["POST"])
def simulate_error(node_index):
    """Giả lập lỗi trên một Node cụ thể"""
    if node_index < 0 or node_index >= len(NODES):
        return jsonify({"error": "Invalid node index"}), 400
        
    node = NODES[node_index]
    try:
        response = requests.post(f"{node}/failover/simulate")
        return jsonify(response.json())
    except requests.exceptions.RequestException:
        return jsonify({"error": "Node unavailable"}), 500

@app.route("/restore/<int:node_index>", methods=["POST"])
def restore_node(node_index):
    """Phục hồi một Node cụ thể"""
    if node_index < 0 or node_index >= len(NODES):
        return jsonify({"error": "Invalid node index"}), 400
        
    node = NODES[node_index]
    try:
        response = requests.post(f"{node}/failover/restore")
        return jsonify(response.json())
    except requests.exceptions.RequestException:
        return jsonify({"error": "Node unavailable"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)