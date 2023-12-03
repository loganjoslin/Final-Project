from flask import Flask, redirect, render_template, request, jsonify, session
from seating import seating_algorithm
import re

# Configure app
app = Flask(__name__)
app.secret_key = 'Minecraft'

# ENSURE TOTAL SESSION CLEARING

# Homepage
@app.route("/", methods=["GET", "POST"])
def index():
    session.clear()
    if request.method == "POST":
        nameText = request.form.get("Names")
        Partners = False
        if request.form.get("partners") == "True":
            Partners = True
        Names = []
        split = re.split(r'[,; \n]+', nameText)
        for s in split:
            if (not s.strip() == ''):
                Names.append(s.strip().capitalize())
        session['Names'] = Names
        session['Height'] = int(request.form.get("height"))
        session['Width'] = int(request.form.get("width"))
        session['Partners'] = Partners

        return render_template("compatibles.html", Names=Names)
    elif request.method == "GET":
        return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    height = session['Height']
    width = session['Width']
    partners = session['Partners']
    names = session['Names']

    lists = request.get_json()
    HI = lists['HIncomps']
    I = lists['Incomps']
    C = lists['Comps']
    F = lists['Fronts']
    Ass = seating_algorithm(names, height, width, HI, I, C, F, partners)

    data = {
        "Ass": Ass,
        "Height": height,
        "Width": width,
        "Partners": partners,
        "Fronts": F,
        "HI": HI
    }
    print("Generate route called!")
    session.clear()
    print(f"Session: {session}")
    print("Data to be JSONified:", data)
    return jsonify(data)