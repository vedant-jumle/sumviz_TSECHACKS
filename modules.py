from summarizer import TransformerSummarizer
from openie import StanfordOpenIE
from difflib import SequenceMatcher
import spacy

summarizer = TransformerSummarizer(
    transformer_type="GPT2",
    transformer_model_key="gpt2-medium",
)

properties = {
    'openie.affinity_probability_cap': 2/3,
}

section_nlp = spacy.load("./models/section_NER/model-best")
nlp = spacy.load('en_core_web_sm')

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_summary(text):
    summary = "".join(summarizer(text, min_length=20))
    return summary

def annotate(text):
    print("ann", text)
    with StanfordOpenIE(properties=properties) as stanford_openie:
        return stanford_openie.annotate(text)

def clean_annotations(annotations, thres=0.6):
    for i, annotation in enumerate(annotations):
        for j, annotation_2 in enumerate(annotations):
            cmp_string_1 = annotation["subject"] + annotation["relation"] + annotation["object"]
            cmp_string_2 = annotation_2["subject"] + annotation_2["relation"] + annotation_2["object"]

            if i!=j and similar(cmp_string_1, cmp_string_2) > thres:
                del annotations[j]

    print(annotations)

    return annotations

def get_sections(text):
    sections = []
    for section in section_nlp(text).ents:
        sections.append({
            "text": section.text,
            "start": section.start_char,
            "end": section.end_char,
            "type": section.label_
        })
    return sections


def create_nodes(annotations):
    data = {
        "data": {"sub": "summary", "type": "root"},
        "children": []
    }

    parents = []

    for i, annotation in enumerate(annotations):
        if annotation["subject"] not in parents:
            parents.append(annotation["subject"])
            data["children"].append({
                "data": {"sub": annotation["subject"], "click": "click"},
                "children": [
                    {
                        "data": {"sub": annotation["relation"], "type": "ref"},
                        "children": [{
                            "data": {"sub": annotation["object"], "type": "obj"}
                        }]
                    }
                ]
            })
        else:
            index = parents.index(annotation["subject"])
            data["children"][index]["children"].append({
                "data": {"sub": annotation["relation"], "type": "ref"},
                "children": [{
                    "data": {"sub": annotation["object"], "type": "obj"},
                }]
            })

    return data


def get_ents(text):
    l = []
    doc = nlp(text)
    if doc.ents:
        for ent in doc.ents:
            l.append(ent.text)
    return l