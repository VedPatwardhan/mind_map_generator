from gensim.models import Word2Vec
import numpy as np


def get_all_headings(doc_heading):
    all_headings = []
    for i in range(len(doc_heading)):
        heading = doc_heading[i]
        all_headings.append(heading)
    return all_headings


def get_all_sentences(doc_sentences):
    all_sentences = []
    for i in range(len(doc_sentences)):
        sentences = doc_sentences[i]
        all_sentences += sentences
    return all_sentences


def train_word2vec(sentences):
    embedder = Word2Vec(
        window=4,
        sg=1,
        hs=0,
        negative=10,
        alpha=0.03,
        min_alpha=0.0001,
        min_count=1,
        seed=42,
    )
    embedder.build_vocab(sentences, progress_per=2)
    embedder.train(sentences, total_examples=embedder.corpus_count, epochs=2)
    return embedder


def get_adjacency_matrix(adjacency_matrix, words, wv, all_headings, node_selected=""):
    for i in range(0, len(words)):
        factor = 1
        if words[i] == node_selected:
            factor = 5
        for j in range(i + 1, len(words)):
            if words[i] not in all_headings and words[j] not in all_headings:
                adjacency_matrix[i][j] = (
                    np.abs(np.dot(wv[words[i]], wv[words[j]])) * factor
                )
    return adjacency_matrix


def get_trained_adjacency_matrix(adjacency_matrix, doc_sentences, doc_heading, words, node_selected=""):
    all_sentences = get_all_sentences(doc_sentences)
    all_headings = get_all_headings(doc_heading)
    embedder = train_word2vec(all_sentences)
    wv = embedder.wv
    adjacency_matrix = get_adjacency_matrix(adjacency_matrix, words, wv, all_headings, node_selected)
    threshold = np.percentile(np.unique(adjacency_matrix), 80)
    return adjacency_matrix, threshold
