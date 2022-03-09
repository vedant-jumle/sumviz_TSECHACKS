from summarizer import TransformerSummarizer
from openie import StanfordOpenIE
from difflib import SequenceMatcher
import spacy

summarizer = TransformerSummarizer(
    transformer_type="GPT2",
    transformer_model_key="gpt2-medium",
)

stanford_openie = StanfordOpenIE(properties={
    'openie.affinity_probability_cap': 2/3,
})

section_nlp = spacy.load("./models/section_NER/model-best")
nlp = spacy.load('en_core_web_sm')

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_summary(text):
    return summarizer.summarize(text)

def annotate(text):
    return stanford_openie.annotate(text)

def clean_annotations(annotations, thres=0.6):
    for i, annotation in enumerate(annotations):
        for j, annotation_2 in enumerate(annotations):
            cmp_string_1 = annotation["subject"] + annotation["relation"] + annotation["object"]
            cmp_string_2 = annotation_2["subject"] + annotation_2["relation"] + annotation_2["object"]

            if i!=j and similar(cmp_string_1, cmp_string_2) > thres:
                del annotations[j]

    return annotations

def get_sections(text):
    sections = []
    for section in section_nlp(text):
        sections.append({
            "text": section.text,
            "start": section.start_char,
            "end": section.end_char,
            "type": section.label_
        })
    return sections


def get_ents(text):
    l = []
    doc = nlp(text)
    if doc.ents:
        for ent in doc.ents:
            l.append(ent.text)
    return l