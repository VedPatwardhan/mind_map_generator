import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
np.random.seed(0)
from word2vec import *


def draw_graph(doc_keywords, doc_indices, doc_heading, doc_sentences, rule_based=False):
    G = nx.Graph()
    
    words = doc_heading
    for i in range(len(doc_keywords)):
        words += list(doc_keywords[i].keys())
    words = list(set(words))

    nodes, colors = [], ['red', 'purple', 'blue', 'green', 'yellow', 'orange']
    k = 0

    for word in words:
        nodes.append((word, {"color": colors[k], "size": int(len(word)*400)}))
        k = (k + 1) % len(colors)

    if rule_based:
        adjacency_matrix, threshold = get_proximity_adjacency_matrix(words, doc_indices, doc_heading, doc_keywords)
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
    # node_sizes = list(nx.get_node_attributes(G, "size").values())
    pos = nx.kamada_kawai_layout(G)
    nx.draw(G, pos=pos, with_labels=True, font_weight='bold', node_color=node_colors)
    plt.show()


def get_proximity_adjacency_matrix(words, doc_indices, doc_heading, doc_keywords):
    proximity_matrix = np.zeros((len(words), len(words)))
    word_to_idx = {words[idx]: idx for idx in range(len(words))}
    for i in range(len(doc_indices)):
        heading = doc_heading[i]
        indices = doc_indices[i]
        keywords = doc_keywords[i]
        heading_idx = word_to_idx[heading]
        keyword_list = list(keywords.keys())
        for i in range(len(keyword_list)):
            keyword1 = keyword_list[i]
            keyword_indices1 = indices[keyword1]
            keyword_idx1 = word_to_idx[keyword1]
            idxs = [heading_idx, keyword_idx1]
            idxs.sort()
            proximity_matrix[idxs[0]][idxs[1]] = 1
            for j in range(i+1, len(keyword_list)):
                keyword2 = keyword_list[j]
                keyword_indices2 = indices[keyword2]
                keyword_idx2 = word_to_idx[keyword2]
                for x in range(len(keyword_indices1)):
                    for y in range(len(keyword_indices2)):
                        proximity_matrix[keyword_idx1][keyword_idx2] += (keyword_indices1[x] - keyword_indices2[y]) ** (-2)
    threshold = np.percentile(proximity_matrix, 85)
    return proximity_matrix, threshold


def get_random_edge_weights(G, words):
    edge_weights = np.random.rand(len(words), len(words))
    m = np.mean(edge_weights)
    return edge_weights, m


def generate_random_embeddings(words):
    embeddings = np.random.randn(len(words), 16)
    return embeddings