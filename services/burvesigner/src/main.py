#!/usr/bin/env python3
from burvesigner import BurveSigner
from flask import Flask, make_response, render_template, request, flash
from hashlib import sha256
from time import time
import base64
import json
import secrets
import sqlite3


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex()
db = "database.db"
signer = BurveSigner()


b64p = lambda x: x + b"=" * (-len(x) % 4)
b64u = lambda x: x.rstrip(b"=")
b64e = lambda x: b64u(base64.urlsafe_b64encode(x))
b64d = lambda x: base64.urlsafe_b64decode(b64p(x))


def generate_token(user, role):
    payload = b64e(json.dumps({
        "user": user,
        "role": role,
        "exp": int(time()) + 300
    }).encode())
    signature = signer.sign(payload)
    token = payload + b"." + signature
    return token.decode()


def validate_token(token):
    assert token.count(".") == 1
    payload, signature = token.split(".")
    assert signer.verify(payload.encode(), signature.encode())
    payload = json.loads(b64d(payload.encode()).decode())
    assert payload.get("user") and payload.get("role") and payload.get("exp")
    user, role, exp = payload.get("user"), payload.get("role"), payload.get("exp")
    assert int(time()) < exp
    return [user, role, exp]


def create_response_data(user, role):
    data = f"Welcome, {user}! "
    if role == "admin":
        try:
            data += open("/flag.txt").read()
        except:
            data += "Flag is missing, please contact probset"
    else:
        data += "Only admin can access the flag"
    return data


def get_role(username, password):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT role FROM users WHERE username = ? AND password = ?",
        (username, sha256(b"gema" + password.encode() + b"steg").hexdigest()),
    )
    role = cursor.fetchone()
    connection.close()
    assert role
    return role[0]


@app.route("/params", methods=["GET"])
def params():
    return f"<pre>{json.dumps(signer.get_params(), indent=2)}</pre>"


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            assert 2 <= len(username) <= 32
            assert 2 <= len(password) <= 32
            role = get_role(username, password)
            token = generate_token(username, role)
            validate_token(token)
            response = make_response(render_template(
                "index.html",
                data=create_response_data(username, role)
            ))
            response.set_cookie("token", token)
            return response
        except:
            flash("Invalid username and/or password")
            return render_template("index.html")
    else:
        token = request.cookies.get("token")
        if token:
            try:
                username, role, _ = validate_token(token)
                return render_template(
                    "index.html",
                    data=create_response_data(username, role)
                )
            except:
                flash("Invalid token")
                return render_template("index.html")
        else:
            return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)
