from flask import Flask, redirect, render_template, request
from seating import seating_algorithm
import re

# Configure app
app = Flask(__name__)

# Homepage
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect("/sizing")
    return render_template("index.html")

@app.route("/sizing", methods=["GET", "POST"])
def sizing():
    if request.method == "POST":
        width = request.form.get("width")
        height = request.form.get("height")
        print(f"width: {width}")
        print(f"height: {height}")
        return render_template("namelist.html")
    return render_template("sizing.html")

@app.route("/selection", methods=["POST"])
def selection():
    nameText = request.form.get("Names")
    clean = []
    split = re.split(r'[,; \n]+', nameText)
    for s in split:
        if (not s.strip() == ''):
            clean.append(s.strip().capitalize())
    print(clean)
    return render_template("compatibles.html", Names=clean)