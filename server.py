# make a basic flask server with one route, and import jasonify
from datasets import ReadInstruction
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from modules import *
import os
import json


# create a flask app
app = Flask(__name__)
# CORS(app)


# set static folder
app.config['STATIC_FOLDER'] = 'static'


# create a route
@app.route('/')
def index():
    # render the index.html file
    return render_template('index.html')


# get the text from the body of the get request
@app.route("/process/")
def process():
    text = request.args.get("text")
    return jsonify({
        "summary": get_summary(text),
        "nodes": create_nodes(clean_annotations(annotate(text))),
        "sections": get_sections(text),
        "entities": get_ents(text)
    })
        


@app.route("/tree")
def tree():
    return jsonify(json.load(open("./static/tree.json")))

# run the app
if __name__ == "__main__":
    app.run(debug=True)
