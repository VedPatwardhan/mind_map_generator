from django.shortcuts import render
from main_code.parser import get_text
from main_code.extractors import *
from main_code.lemmatizers import *
from main_code.graph import *
from main_code.utils import *


def index(request):
    if request.method == "POST":
        URLS = request.POST.getlist('url')
        doc_sentences = []
        doc_heading = []
        for URL in URLS:
            sentences, heading = get_text(URL)
            doc_sentences.append(sentences)
            doc_heading.append(heading)
        contributors = get_contributors()
        for i in range(len(URLS)):
            for j in range(len(doc_sentences[i])):
                doc_sentences[i][j] = [word for word in doc_sentences[i]
                                       [j] if word not in contributors]
        for i in range(len(URLS)):
            doc_sentences[i] = stanfordcorenlp_lemmatizer(doc_sentences[i])
        doc_keywords = []
        for i in range(len(URLS)):
            doc_keywords.append(bert_extractor(doc_sentences[i], 1, 15))
        doc_filtered_keywords = []
        for i in range(len(URLS)):
            print(
                "\n----------------------------------------------------------------------------------\n")
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
        print("\n----------------------------------------------------------------------------------\n")
        doc_indices = []
        for i in range(len(URLS)):
            doc_indices.append(generate_indices(
                doc_filtered_keywords[i], doc_sentences[i]))
        # fig = draw_graph(doc_filtered_keywords,
        #                  doc_indices,
        #                  doc_heading,
        #                  doc_sentences,
        #                  rule_based=False,
        #                  draw=False)
        return render(request, 'index.html', {})
    else:
        return render(request, 'index.html', {})
