from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
import os

app = Flask(__name__)
app.secret_key = "fools_playground_secret_key_2026"

USERS = {
    "investigator": {"password": "investigate123", "role": "user",  "id": 1},
    "admin":        {"password": "f00l_pr0t3ct3d_p4ss", "role": "admin", "id": 2}
}

VAULT_ENTRIES = {
    1: {"owner": "investigator",
        "content": "Welcome to the vault. Nothing suspicious here.",
        "file": None},
    2: {"owner": "investigator",
        "content": "Case notes: The Fool left traces in the network logs.",
        "file": None},
    3: {"owner": "admin",
        "content": "ADMIN VAULT: Evidence package located.",
        "file": "evidence_package.zip"},
    4: {"owner": "admin",
        "content": "Fool's backup key: FP{web_a7x9k2m4}",
        "file": None},
}

FLAG = "FP{web_a7x9k2m4}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in USERS and USERS[username]["password"] == password:
            session["user"]    = username
            session["user_id"] = USERS[username]["id"]
            session["role"]    = USERS[username]["role"]
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html",
                           user=session["user"],
                           role=session["role"])

@app.route("/vault/<int:entry_id>")
def vault(entry_id):
    if "user" not in session:
        return redirect(url_for("login"))
    entry = VAULT_ENTRIES.get(entry_id)
    if not entry:
        return "Entry not found", 404
    return render_template("vault.html", entry=entry, entry_id=entry_id)

@app.route("/download/<filename>")
def download(filename):
    if "user" not in session:
        return redirect(url_for("login"))
    safe_path = os.path.join("evidence", os.path.basename(filename))
    if os.path.exists(safe_path):
        return send_file(safe_path, as_attachment=True)
    return "File not found", 404

@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return "Access Denied", 403
    return render_template("admin.html", flag=FLAG)

@app.route("/api/vault/list")
def api_vault_list():
    if "user" not in session:
        return jsonify({"error": "unauthorized"}), 401
    return jsonify({"entries": [1, 2], "hint": "Try other entry IDs..."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

