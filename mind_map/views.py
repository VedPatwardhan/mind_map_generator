import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")
import io
import json
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main_code.parser import get_text
from main_code.extractors import *
from main_code.lemmatizers import *
from main_code.graph import *
from main_code.utils import *


@csrf_exempt
def index(request):
    fig = None
    if request.method == "POST":
        json_body = json.loads(request.body)
        adjacency_matrix = json_body["adjacency_matrix"]
        doc_sentences = json_body["doc_sentences"]
        doc_heading = json_body["doc_heading"]
        words = json_body["words"]
        node_selected = json_body["node_selected"]
        adjacency_matrix, threshold = get_trained_adjacency_matrix(np.array(adjacency_matrix), doc_sentences, doc_heading, words, node_selected)
        response = {
            "nodes": [
                (node["id"], {"color": [color / 255 for color in node["color"]]})
                for node in json_body["nodes"]
            ],
            "links": [],
            "adjacency_matrix": adjacency_matrix.tolist(),
            "doc_sentences": doc_sentences,
            "doc_heading": doc_heading,
            "words": words,
        }
        for i in range(len(words)):
            for j in range(len(words)):
                if adjacency_matrix[i][j] >= threshold:
                    response["links"].append((words[i], words[j]))
        return JsonResponse(response, safe=False)
    elif len(request.GET.getlist("url")):
        URLS = [url for url in request.GET.get("url").split(",") if url != ""]
        doc_sentences = []
        doc_heading = []
        for URL in URLS:
            sentences, heading = get_text(URL)
            doc_sentences.append(sentences)
            doc_heading.append(heading)
        contributors = get_contributors()
        for i in range(len(URLS)):
            for j in range(len(doc_sentences[i])):
                doc_sentences[i][j] = [
                    word for word in doc_sentences[i][j] if word not in contributors
                ]
        for i in range(len(URLS)):
            doc_sentences[i] = stanfordcorenlp_lemmatizer(doc_sentences[i])
        doc_keywords = []
        for i in range(len(URLS)):
            doc_keywords.append(bert_extractor(doc_sentences[i], 1, 15))
        doc_filtered_keywords = []
        for i in range(len(URLS)):
            print(
                "\n----------------------------------------------------------------------------------\n"
            )
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
                    print(kw[1], " --> ", kw[0])
            doc_filtered_keywords.append(filtered_keywords)
        print(
            "\n----------------------------------------------------------------------------------\n"
        )
        doc_indices = []
        for i in range(len(URLS)):
            doc_indices.append(
                generate_indices(doc_filtered_keywords[i], doc_sentences[i])
            )
        G, adjacency_matrix, doc_heading, words = draw_graph(
            doc_filtered_keywords,
            doc_indices,
            doc_heading,
            doc_sentences,
            rule_based=False,
            draw=False,
        )
        response = JsonResponse(
            {
                "nodes": list(G.nodes(data=True)),
                "links": list(G.edges()),
                "adjacency_matrix": adjacency_matrix.tolist(),
                "doc_sentences": doc_sentences,
                "doc_heading": doc_heading,
                "words": words,
            },
            safe=False,
        )
        return response
    return render(
        request, "Command line arguments in C - English _ spoken-tutorial.org.html"
    )
