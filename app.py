from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Define Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()


# Route to Add a Task
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    new_task = Task(title=data["title"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully!"})

# Route to Get All Tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": task.id, "title": task.title} for task in tasks])

# Route to Delete a Task
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"message": "Task not found!"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted!"})

# Initialize DB
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This ensures the tables are created
    app.run(debug=True, host="0.0.0.0", port=5000)
