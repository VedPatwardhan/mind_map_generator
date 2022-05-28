from ast import keyword
from parser import get_text
from extractors import *
from lemmatizers import *
from graph import *
from utils import *
import sys

URL, lemmatizer, identifier, drawer = "https://script.spoken-tutorial.org/index.php/Apps-On-Physics/C2/Simple-Machines/English-timed", 3, 2, 1
if len(sys.argv) == 5:
    URL, lemmatizer, identifier = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

URLS = get_urls()
for URL in URLS:
    print(URL)

doc_sentences = []
doc_heading = []
for URL in URLS:
    sentences, heading = get_text(URL)
    doc_sentences.append(sentences)
    doc_heading.append(heading)

contributors = get_contributors()
for i in range(len(URLS)):
    for j in range(len(doc_sentences[i])):
        doc_sentences[i][j] = [word for word in doc_sentences[i][j] if word not in contributors]

for i in range(len(URLS)):
    if lemmatizer == 1:
        doc_sentences[i] = nltk_lemmatizer(doc_sentences[i])
    elif lemmatizer == 2:
        doc_sentences[i] = spacy_lemmatizer(doc_sentences[i])
    elif lemmatizer == 3:
        doc_sentences[i] = stanfordcorenlp_lemmatizer(doc_sentences[i])
    
doc_keywords = []
for i in range(len(URLS)):
    if identifier == 1:
        doc_keywords.append(yake_extractor(doc_sentences[i], 1, 15))
    elif identifier == 2:
        doc_keywords.append(bert_extractor(doc_sentences[i], 1, 15))

doc_filtered_keywords = []
for i in range(len(URLS)):
    print("\n----------------------------------------------------------------------------------")
    print("URL: ", URLS[i])
    display = True
    filtered_keywords = {}
    for kw in doc_keywords[i]:
        display = True
        words = kw[1].split()
        for word in words:
            if word in contributors:
                display = False
        if display:
            filtered_keywords[kw[1]] = kw[0]
            print(kw[1], ' --> ', kw[0])
    doc_filtered_keywords.append(filtered_keywords)

doc_indices = []
for i in range(len(URLS)):
    doc_indices.append(generate_indices(doc_filtered_keywords[i], doc_sentences[i]))

for indices in doc_indices:
    print(indices, end='\n')

draw_graph(doc_filtered_keywords, doc_indices, doc_heading, doc_sentences, rule_based=drawer==1)
