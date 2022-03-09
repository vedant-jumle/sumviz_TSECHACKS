# make a basic flask server with one route, and import jasonify
from datasets import ReadInstruction
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from js2py import require
from modules import *
import os
import json


# create a flask app
app = Flask(__name__)
# CORS(app)


temp_text = ""


# set static folder
app.config['STATIC_FOLDER'] = 'static'


# create a route
@app.route('/')
def index():
    # render the index.html file
    return render_template('index.html')


# get the text from the body of the get request
@app.route("/process")
def process():
    text = request.args.get("text", "").replace("\n", " ").replace("%20", " ")
    temp_text = text

    nodes = create_nodes(clean_annotations(annotate(text)))
    json_output = open("temp.json", "w")
    json.dump(nodes, json_output, indent=4)

    summary = get_summary(text)
    sections = get_sections(text)
    ents = get_ents(summary)

    return jsonify({
        "summary": summary,
        "sections": sections,
        "entities": ents
    })
        

@app.route("/tree")
def tree():
    # text = request.args.get("text", "").replace("\n", " ").replace("%20", " ")

    input_file = open("temp.json", "r")
    data = json.load(input_file)

    return jsonify(data)

# run the app
if __name__ == "__main__":
    app.run(debug=True)
