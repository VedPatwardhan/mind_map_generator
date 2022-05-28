import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
np.random.seed(0)
from word2vec import *


def draw_graph(doc_keywords, doc_indices, doc_heading, doc_sentences, rule_based=False):
    G = nx.Graph()

    words = []
    for i in range(len(doc_keywords)):
        words += list(doc_keywords[i].keys())
        doc_keywords[i][doc_heading[i]] = 1
    words = list(set(words))

    nodes, colors = [], ['red', 'purple', 'blue', 'green', 'yellow', 'orange']
    k = 0

    for word in words:
        nodes.append((word, {"color": colors[k], "size": int(len(word)*400)}))
        k = (k + 1) % len(colors)

    if rule_based:
        adjacency_matrix, threshold = get_proximity_adjacency_matrix(words, doc_indices, doc_heading)
    else:
        for i in range(0, len(words)):
            for j in range(i+1, len(words)):
                G.add_edge(words[i], words[j])
        adjacency_matrix, threshold = get_trained_adjacency_matrix(words, doc_sentences)
    
    G.add_nodes_from(nodes)
    for i in range(0, len(words)):
        for j in range(i+1, len(words)):
            if adjacency_matrix[i][j] >= threshold:
                G.add_edge(words[i], words[j])

    node_colors = list(nx.get_node_attributes(G, "color").values())
    node_sizes = list(nx.get_node_attributes(G, "size").values())
    pos = nx.kamada_kawai_layout(G)
    nx.draw(G, pos=pos, with_labels=True, font_weight='bold', node_color=node_colors, node_size=node_sizes)
    plt.show()


def get_proximity_adjacency_matrix(words, doc_indices, doc_heading):
    proximity_matrix = np.zeros((len(words), len(words)))
    for i in range(1, len(words)):
        proximity_matrix[0][i] = 1

    for i in range(1, len(words)):
        for j in range(i+1, len(words)):
            indices1 = indices[words[i]]
            indices2 = indices[words[j]]
            for m in range(len(indices1)):
                for n in range(len(indices2)):
                    proximity_matrix[i][j] += 1/(abs(indices1[m] - indices2[n])**2)
    proximity_matrix[i][j] *= 10000
    threshold = np.percentile(np.unique(proximity_matrix), 85)

    return proximity_matrix, threshold


def get_random_edge_weights(G, words):
    edge_weights = np.random.rand(len(words), len(words))
    m = np.mean(edge_weights)
    return edge_weights, m


def generate_random_embeddings(words):
    embeddings = np.random.randn(len(words), 16)
    return embeddings