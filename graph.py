import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
np.random.seed(0)
from word2vec import *


def draw_graph(doc_keywords, doc_indices, doc_heading, doc_sentences, rule_based=False):
    G = nx.Graph()
    words = doc_heading.copy()
    for i in range(len(doc_keywords)):
        words += list(doc_keywords[i].keys())
    words = list(set(words))
    nodes, colors = [], ['red', 'purple', 'blue', 'green', 'yellow', 'orange']
    k = 0
    for word in words:
        nodes.append((word, {"color": colors[k], "size": int(len(word)*300)}))
        k = (k + 1) % len(colors)
    adjacency_matrix = np.zeros((len(words), len(words)))
    word_to_idx = {words[idx]: idx for idx in range(len(words))}
    adjacency_matrix = fill_adjacency_matrix_for_headings(adjacency_matrix, word_to_idx, doc_indices, doc_heading, doc_keywords)
    if rule_based:
        adjacency_matrix, threshold = get_proximity_adjacency_matrix(adjacency_matrix, word_to_idx, doc_indices, doc_keywords)
    else:
        adjacency_matrix, threshold = get_trained_adjacency_matrix(adjacency_matrix, doc_sentences, doc_heading, words)
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


def fill_adjacency_matrix_for_headings(adjacency_matrix, word_to_idx, doc_indices, doc_heading, doc_keywords):
    for i in range(len(doc_indices)):
        heading = doc_heading[i]
        keywords = doc_keywords[i]
        heading_idx = word_to_idx[heading]
        keyword_list = list(keywords.keys())
        for i in range(len(keyword_list)):
            keyword = keyword_list[i]
            keyword_idx = word_to_idx[keyword]
            idxs = [heading_idx, keyword_idx]
            idxs.sort()
            adjacency_matrix[idxs[0]][idxs[1]] = 1
    return adjacency_matrix


def get_proximity_adjacency_matrix(adjacency_matrix, word_to_idx, doc_indices, doc_keywords):
    for i in range(len(doc_indices)):
        indices = doc_indices[i]
        keywords = doc_keywords[i]
        keyword_list = list(keywords.keys())
        for i in range(len(keyword_list)):
            keyword1 = keyword_list[i]
            keyword_indices1 = indices[keyword1]
            keyword_idx1 = word_to_idx[keyword1]
            for j in range(i+1, len(keyword_list)):
                keyword2 = keyword_list[j]
                keyword_indices2 = indices[keyword2]
                keyword_idx2 = word_to_idx[keyword2]
                for x in range(len(keyword_indices1)):
                    for y in range(len(keyword_indices2)):
                        adjacency_matrix[keyword_idx1][keyword_idx2] += (keyword_indices1[x] - keyword_indices2[y]) ** (-2)
    threshold = np.percentile(np.unique(adjacency_matrix), 85)
    return adjacency_matrix, threshold
