from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# API Base URL (replace with your API URL)
API_BASE_URL = "https://restapialltasks.onrender.com/task"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get data from the form
        task_name = request.form.get("task_name")
        task_description = request.form.get("task_description")
        task_status = request.form.get("task_status")

        # Create a new task using the API
        payload = {
            "task_name": task_name,
            "task_description": task_description,
            "task_status": task_status
        }

        response = requests.post(API_BASE_URL, json=payload)

        if response.status_code == 201:
            return redirect(url_for("home"))

    # Fetch all tasks from the API
    response = requests.get(API_BASE_URL)
    tasks = response.json() if response.status_code == 200 else []
    return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    # Delete a task using the API
    delete_url = f"{API_BASE_URL}/{task_id}"
    requests.delete(delete_url)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(port=5001, debug=True)
