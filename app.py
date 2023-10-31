from flask import Flask, redirect, render_template, request
from seating import seating_algorithm

# Configure app
app = Flask(__name__)

# Homepage
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect("/presetting")
    return render_template("index.html")

@app.route("/presetting", methods=["GET", "POST"])
def presetting():
    return render_template("sizing.html")

