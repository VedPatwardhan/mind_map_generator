from word2vec import *
import networkx as nx
from grave import plot_network
from grave.style import use_attributes
import matplotlib.pyplot as plt
from matplotlib.artist import Artist
import numpy as np
np.random.seed(0)


def add_edges_based_on_threshold(G,
                                 words,
                                 adjacency_matrix,
                                 threshold):
    for i in range(0, len(words)):
        for j in range(i+1, len(words)):
            if adjacency_matrix[i][j] >= threshold:
                G.add_edge(words[i], words[j])


def on_click(event,
             adjacency_matrix,
             doc_heading,
             words,
             ax):
    if not hasattr(event, 'nodes') or not event.nodes:
        return
    # pull out the graph,
    graph = event.artist.graph
    # clear any non-default color on nodes
    for node, attributes in graph.nodes.data():
        attributes.pop('color', None)
    for u, v, attributes in graph.edges.data():
        attributes.pop('width', None)
    for node in event.nodes:
        node_selected = node
        adjacency_matrix = update_adjacency_matrix(adjacency_matrix,
                                                   doc_heading,
                                                   words,
                                                   node_selected)
        threshold = np.percentile(np.unique(adjacency_matrix), 92)
        graph.remove_edges_from(graph.edges())
        add_edges_based_on_threshold(graph, words, adjacency_matrix, threshold)
        graph.nodes[node]['color'] = 'C1'
        for edge_attribute in graph[node].values():
            edge_attribute['width'] = 3
    # update the screen
    # plt.clf()
    # event.artist.figure.canvas.draw_idle()
    Artist.remove(event.artist)
    event.artist = plot_network(graph,
                                ax=ax,
                                layout="kamada_kawai",
                                node_style=use_attributes(),
                                edge_style=use_attributes(),
                                node_label_style={'bbox':  dict(boxstyle='round',
                                                                ec=(0.0,
                                                                    0.0, 0.0),
                                                                fc=(1.0,
                                                                    1.0, 1.0),
                                                                ),
                                                  'font_size': 10,
                                                  'font_weight': 'bold',
                                                  })
    event.artist.set_picker(10)
    # ax.set_title('Mind map')
    # event.artist.stale = True
    event.artist.figure.canvas.draw_idle()


def draw_graph(doc_keywords,
               doc_indices,
               doc_heading,
               doc_sentences,
               rule_based=False):
    G = nx.Graph()
    words = doc_heading.copy()
    for i in range(len(doc_keywords)):
        words += list(doc_keywords[i].keys())
    words = list(set(words))
    nodes = []
    for word in words:
        nodes.append((word))
    adjacency_matrix = np.zeros((len(words), len(words)))
    word_to_idx = {words[idx]: idx for idx in range(len(words))}
    adjacency_matrix = fill_adjacency_matrix_for_headings(adjacency_matrix,
                                                          word_to_idx,
                                                          doc_indices,
                                                          doc_heading,
                                                          doc_keywords)
    if rule_based:
        adjacency_matrix, threshold = get_proximity_adjacency_matrix(adjacency_matrix,
                                                                     word_to_idx,
                                                                     doc_indices,
                                                                     doc_keywords)
    else:
        adjacency_matrix, threshold = get_trained_adjacency_matrix(adjacency_matrix,
                                                                   doc_sentences,
                                                                   doc_heading,
                                                                   words)
    G.add_nodes_from(nodes)
    add_edges_based_on_threshold(G, words, adjacency_matrix, threshold)
    fig, ax = plt.subplots()
    art = plot_network(G,
                       ax=ax,
                       layout="kamada_kawai",
                       node_style=use_attributes(),
                       edge_style=use_attributes(),
                       node_label_style={'bbox':  dict(boxstyle='round',
                                                       ec=(0.0, 0.0, 0.0),
                                                       fc=(1.0, 1.0, 1.0),
                                                       ),
                                         'font_size': 10,
                                         'font_weight': 'bold',
                                         })
    art.set_picker(10)
    ax.set_title('Mind map')
    fig.set_size_inches(12, 9)
    fig.canvas.mpl_connect('pick_event', lambda event: on_click(event,
                                                                adjacency_matrix,
                                                                doc_heading,
                                                                words,
                                                                ax))
    plt.show()


def fill_adjacency_matrix_for_headings(adjacency_matrix,
                                       word_to_idx,
                                       doc_indices,
                                       doc_heading,
                                       doc_keywords):
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


def get_proximity_adjacency_matrix(adjacency_matrix,
                                   word_to_idx,
                                   doc_indices,
                                   doc_keywords):
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
                        adjacency_matrix[keyword_idx1][keyword_idx2] += (
                            keyword_indices1[x] - keyword_indices2[y]) ** (-2)
    threshold = np.percentile(np.unique(adjacency_matrix), 92)
    return adjacency_matrix, threshold
