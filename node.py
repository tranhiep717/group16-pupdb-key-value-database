from pathlib import Path
import os
from flask import Flask, request, jsonify
from pupdb.core import PupDB

app = Flask(__name__)

NODE_ID = os.getenv("NODE_ID", "node1")
DATA_DIR = Path(__file__).with_name("data")
DATA_DIR.mkdir(exist_ok=True)

DB_FILE = DATA_DIR / f"{NODE_ID}.json"
REPLICA_FILE = DATA_DIR / f"{NODE_ID}_replica.json"

db = PupDB(str(DB_FILE))
replica_db = PupDB(str(REPLICA_FILE))

# Biến trạng thái để giả lập lỗi shard chính (Failover test)
simulate_fail_primary = False

@app.route("/")
def home():
    return jsonify({
        "message": "Node is running",
        "node_id": NODE_ID,
        "db_file": str(DB_FILE),
        "replica_file": str(REPLICA_FILE),
        "primary_failed": simulate_fail_primary
    })


@app.route("/set", methods=["POST"])
def set_student():
    data = request.json
    student_id = data["student_id"]

    # REPLICATION: Lưu vào cả shard chính và replica
    if not simulate_fail_primary:
        db.set(student_id, data)
    
    # Luôn lưu vào replica để đảm bảo tính đồng bộ
    replica_db.set(student_id, data)

    return jsonify({
        "message": "Saved to node and replica",
        "node_id": NODE_ID,
        "student": data
    })


@app.route("/get/<student_id>", methods=["GET"])
def get_student(student_id):
    used_replica = False
    
    # FAILOVER: Nếu shard chính lỗi, lấy từ replica
    if simulate_fail_primary:
        student = replica_db.get(student_id)
        used_replica = True
    else:
        student = db.get(student_id)

    if student is None:
        return jsonify({"error": "Not found", "node_id": NODE_ID, "used_replica": used_replica}), 404

    return jsonify({
        "node_id": NODE_ID,
        "student": student,
        "used_replica": used_replica
    })


@app.route("/delete/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    # Lấy thông tin xem có tồn tại không từ cả 2
    exists_primary = db.get(student_id) is not None
    exists_replica = replica_db.get(student_id) is not None

    if not exists_primary and not exists_replica:
        return jsonify({"error": "Not found", "node_id": NODE_ID}), 404

    # REPLICATION: Xóa từ cả 2
    if not simulate_fail_primary:
        try:
            db.remove(student_id)
        except KeyError:
            pass # Ignore if not exists

    try:
        replica_db.remove(student_id)
    except KeyError:
        pass

    return jsonify({
        "message": "Deleted from node and replica",
        "node_id": NODE_ID
    })


@app.route("/all", methods=["GET"])
def get_all():
    used_replica = False
    
    # FAILOVER
    if simulate_fail_primary:
        data = dict(replica_db.items())
        used_replica = True
    else:
        data = dict(db.items())
        
    return jsonify({
        "node_id": NODE_ID,
        "data": data,
        "used_replica": used_replica,
        "record_count": len(data)
    })

@app.route("/failover/simulate", methods=["POST"])
def simulate_failover():
    global simulate_fail_primary
    simulate_fail_primary = True
    return jsonify({
        "message": f"Shard chính của {NODE_ID} đã bị GIẢ LẬP LỖI. Hệ thống sẽ dùng Replica.",
        "node_id": NODE_ID,
        "primary_failed": simulate_fail_primary
    })

@app.route("/failover/restore", methods=["POST"])
def restore_failover():
    global simulate_fail_primary
    simulate_fail_primary = False
    return jsonify({
        "message": f"Shard chính của {NODE_ID} đã ĐƯỢC PHỤC HỒI.",
        "node_id": NODE_ID,
        "primary_failed": simulate_fail_primary
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    app.run(host="127.0.0.1", port=port, debug=True)