from flask import Flask, request, jsonify

app = Flask(__name__)

students = {}

@app.route("/")
def home():
    return "Coordinator is running"

@app.route("/set", methods=["POST"])
def set_student():
    data = request.json

    student_id = data["student_id"]

    students[student_id] = data

    return jsonify({
        "message": "Student saved",
        "student": data
    })

@app.route("/get/<student_id>")
def get_student(student_id):

    if student_id not in students:
        return jsonify({"error": "Not found"}), 404

    return jsonify(students[student_id])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)