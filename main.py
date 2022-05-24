from parser import get_text
from extractors import *
from lemmatizers import *
from graph import *
from utils import *
import sys

URL, lemmatizer, identifier, drawer = "https://script.spoken-tutorial.org/index.php/Apps-On-Physics/C2/Simple-Machines/English-timed", 3, 1, 1
if len(sys.argv) == 5:
    URL, lemmatizer, identifier = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

sentences, heading = get_text(URL)
contributors = get_contributors()
for i in range(len(sentences)):
    sentences[i] = [word for word in sentences[i] if word not in contributors]

sentences
if lemmatizer == 1:
    sentences = nltk_lemmatizer(sentences)
elif lemmatizer == 2:
    sentences = spacy_lemmatizer(sentences)
elif lemmatizer == 3:
    sentences = stanfordcorenlp_lemmatizer(sentences)

keywords = []
if identifier == 1:
    keywords = yake_extractor(sentences, 1, 15)
elif identifier == 2:
    keywords = bert_extractor(sentences, 1, 15)

display = True
filtered_keywords = {}
for kw in keywords:
    display = True
    words = kw[1].split()
    for word in words:
        if word in contributors:
            display = False
    if display:
        filtered_keywords[kw[1]] = kw[0]
        print(kw[1], ' --> ', kw[0])

indices = generate_indices(filtered_keywords, sentences)

draw_graph(filtered_keywords, indices, heading, sentences, rule_based=drawer==1)
