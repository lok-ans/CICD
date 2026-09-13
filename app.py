from flask import Flask, jsonify, request

app = Flask(__name__)

# Simple in-memory task store.
# Data will reset whenever the Flask process restarts.
tasks = {}
next_task_id = 1


@app.route("/tasks", methods=["GET"])
def get_tasks():
    """Return all tasks."""
    return jsonify(list(tasks.values())), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task."""
    global next_task_id

    data = request.get_json(silent=True) or {}
    title = data.get("title")

    if not title or not isinstance(title, str):
        return jsonify({"error": "title is required and must be a string"}), 400

    task = {
        "id": next_task_id,
        "title": title,
        "completed": False,
    }

    tasks[next_task_id] = task
    next_task_id += 1

    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """Return a task by ID."""
    task = tasks.get(task_id)

    if task is None:
        return jsonify({"error": "task not found"}), 404

    return jsonify(task), 200


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Update an existing task."""
    task = tasks.get(task_id)

    if task is None:
        return jsonify({"error": "task not found"}), 404

    data = request.get_json(silent=True) or {}

    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"]:
            return jsonify({"error": "title must be a non-empty string"}), 400
        task["title"] = data["title"]

    if "completed" in data:
        if not isinstance(data["completed"], bool):
            return jsonify({"error": "completed must be a boolean"}), 400
        task["completed"] = data["completed"]

    return jsonify(task), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task by ID."""
    if task_id not in tasks:
        return jsonify({"error": "task not found"}), 404

    deleted_task = tasks.pop(task_id)
    return jsonify(deleted_task), 200


if __name__ == "__main__":
    app.run(debug=True)
