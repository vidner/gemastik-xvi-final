#!/usr/bin/env python3
from flask import Flask, request, redirect, render_template
import os


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024


@app.route("/upload", methods=["POST"])
def aplot():
    try:
        file = request.files["file"]
        filename = file.filename
        path = os.path.join("uploads/", filename)
        assert filename and ".." not in filename and "flag" not in filename
        assert not os.path.exists(path)
        file.save(os.path.join("uploads/", filename))
        return f'Download <a href="/download?filename={filename}">here</a>'
    except:
        return ">:("


@app.route("/download", methods=["GET"])
def donlot():
    try:
        filename = request.args.get("filename")
        assert filename and ".." not in filename
        return open(os.path.join("uploads/", filename)).read()
    except:
        return ">:("


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)
