import os
import uuid
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory store: {id: {"text": str, "done": bool}}
tasks = {}


@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("task", "").strip()
    if text:
        task_id = str(uuid.uuid4())
        tasks[task_id] = {"text": text, "done": False}
    return redirect(url_for("index"))


@app.route("/toggle/<task_id>", methods=["POST"])
def toggle(task_id):
    if task_id in tasks:
        tasks[task_id]["done"] = not tasks[task_id]["done"]
    return redirect(url_for("index"))


@app.route("/delete/<task_id>", methods=["POST"])
def delete(task_id):
    tasks.pop(task_id, None)
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
