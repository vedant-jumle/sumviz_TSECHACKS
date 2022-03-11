# make a basic flask server with one route, and import jasonify
from flask import Flask, jsonify, request, render_template
from modules import *
import json


# create a flask app
app = Flask(__name__)

temp_text = ""

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

    summary = get_summary(text)

    nodes = create_nodes(clean_annotations(annotate(summary)))
    json_output = open("temp.json", "w")
    json.dump(nodes, json_output, indent=4)

    
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
