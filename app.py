from flask import Flask, redirect, render_template, request, jsonify, session
from seating import seating_algorithm
import re

# Configure app
app = Flask(__name__)
app.secret_key = 'Minecraft'

# Starting page "index.html"
# Initialize session data
@app.route("/", methods=["GET", "POST"])
def index():
    session.clear()
    session["I"] = []
    session["C"] = []
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

        return redirect("/setup")
    elif request.method == "GET":
        return render_template("index.html")

# Second page "compatibles.html"
# HI, I, C, F selection
@app.route("/setup", methods=["GET"])
def change_inputs():
    return render_template("compatibles.html", Names=session['Names'], PartnerMode=session['Partners'], I=session["I"], C=session["C"])

# Receive and process all data before returning plan
# Responds to AJAX request using JSON data
@app.route("/generate", methods=["POST"])
def generate():
    print(f'session["I"]: {session["I"]}')
    print(len(session["I"]))
    height = session['Height']
    width = session['Width']
    partners = session['Partners']
    names = session['Names']

    lists = request.get_json()
    HI = lists['HIncomps']
    F = lists['Fronts']
    I = lists['Incomps']
    C = lists['Comps']
    session["I"] = I.copy()
    session["C"] = C.copy()

    output = seating_algorithm(names, height, width, HI, I, C, F, partners)
    if not output["Timeout"]:
        Ass = output["Ass"]
        CompRemoved = output["CompRemoved"]
        IncompRemoved = output["IncompRemoved"]
        data = {
            "Ass": Ass,
            "Height": height,
            "Width": width,
            "Partners": partners,
            "Fronts": F,
            "HI": HI,
            "CompRemoved": CompRemoved,
            "IncompRemoved": IncompRemoved,
            "Timeout": False
        }
        return jsonify(data)
    else:
        return jsonify({"Timeout": True})

@app.route("/tutorial", methods=["GET"])
def tutorial():
    return render_template("tutorial.html")