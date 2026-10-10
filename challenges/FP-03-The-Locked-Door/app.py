
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_file,
    jsonify,
)
import os
import sys


app = Flask(__name__)

# Deployment-specific values come from the local environment.
# docker-compose.yml will load these from the ignored .env file.
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "")

INVESTIGATOR_PASSWORD = os.environ.get(
    "FP03_INVESTIGATOR_PASSWORD", ""
)
ADMIN_PASSWORD = os.environ.get("FP03_ADMIN_PASSWORD", "")
FLAG = os.environ.get("FP03_FLAG", "")


USERS = {
    "investigator": {
        "password": INVESTIGATOR_PASSWORD,
        "role": "user",
        "id": 1,
    },
    "admin": {
        "password": ADMIN_PASSWORD,
        "role": "admin",
        "id": 2,
    },
}


VAULT_ENTRIES = {
    1: {
        "owner": "investigator",
        "content": "Welcome to the vault. Nothing suspicious here.",
        "file": None,
    },
    2: {
        "owner": "investigator",
        "content": "Case notes: The Fool left traces in the network logs.",
        "file": None,
    },
    3: {
        "owner": "admin",
        "content": "ADMIN VAULT: Evidence package located.",
        "file": "evidence_package.zip",
    },
    4: {
        "owner": "admin",
        "content": f"Fool's backup key: {FLAG}",
        "file": None,
    },
}


def validate_runtime_configuration():
    """Refuse to start with missing or example-only configuration."""
    required = {
        "FLASK_SECRET_KEY": app.secret_key,
        "FP03_INVESTIGATOR_PASSWORD": INVESTIGATOR_PASSWORD,
        "FP03_ADMIN_PASSWORD": ADMIN_PASSWORD,
        "FP03_FLAG": FLAG,
    }

    invalid = [
        name
        for name, value in required.items()
        if not value
        or value.startswith("REPLACE_WITH_")
        or value == "FP{replace_with_a_unique_flag}"
    ]

    if invalid:
        names = ", ".join(invalid)
        raise RuntimeError(
            "Missing or placeholder FP-03 configuration: "
            f"{names}. Copy .env.example to .env and set unique values."
        )

    if INVESTIGATOR_PASSWORD == ADMIN_PASSWORD:
        raise RuntimeError(
            "The investigator and admin accounts must use different passwords."
        )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if (
            username in USERS
            and USERS[username]["password"]
            and USERS[username]["password"] == password
        ):
            session["user"] = username
            session["user_id"] = USERS[username]["id"]
            session["role"] = USERS[username]["role"]
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid credentials",
        )

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        user=session["user"],
        role=session["role"],
    )


@app.route("/vault/<int:entry_id>")
def vault(entry_id):
    if "user" not in session:
        return redirect(url_for("login"))

    entry = VAULT_ENTRIES.get(entry_id)

    if not entry:
        return "Entry not found", 404

    # INTENTIONAL CHALLENGE VULNERABILITY:
    # Ownership is not checked. This is the IDOR issue participants
    # are expected to identify and exploit in this training application.
    return render_template(
        "vault.html",
        entry=entry,
        entry_id=entry_id,
    )


@app.route("/download/<filename>")
def download(filename):
    if "user" not in session:
        return redirect(url_for("login"))

    safe_path = os.path.join(
        "evidence",
        os.path.basename(filename),
    )

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

    return jsonify({
        "entries": [1, 2],
        "hint": "Try other entry IDs...",
    })


if __name__ == "__main__":
    try:
        validate_runtime_configuration()
    except RuntimeError as exc:
        print(f"FP-03 configuration error: {exc}", file=sys.stderr)
        raise SystemExit(1)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )
