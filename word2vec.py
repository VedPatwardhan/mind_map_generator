from gensim.models import Word2Vec
import numpy as np


def train_word2vec(sentences):
    embedder = Word2Vec(
        window=4,
        sg=1,
        hs=0,
        negative=10,
        alpha=0.03,
        min_alpha=0.0001,
        min_count=1,
        seed=42
    )
    embedder.build_vocab(sentences, progress_per=2)
    embedder.train(
        sentences,
        total_examples=embedder.corpus_count,
        epochs=2
    )
    return embedder


def get_adjacency_matrix(adjacency_matrix,
                         words,
                         wv,
                         all_headings):
    for i in range(0, len(words)):
        for j in range(i+1, len(words)):
            if words[i] not in all_headings and words[j] not in all_headings:
                adjacency_matrix[i][j] = np.abs(
                    np.dot(wv[words[i]], wv[words[j]]))
                adjacency_matrix[i][j] = 0
    return adjacency_matrix


def get_trained_adjacency_matrix(adjacency_matrix,
                                 doc_sentences,
                                 doc_heading,
                                 words):
    all_sentences, all_headings = [], []
    for i in range(len(doc_heading)):
        heading = doc_heading[i]
        sentences = doc_sentences[i]
        all_sentences += sentences
        all_headings.append(heading)
    embedder = train_word2vec(all_sentences)
    wv = embedder.wv
    adjacency_matrix = get_adjacency_matrix(adjacency_matrix,
                                            words,
                                            wv,
                                            all_headings)
    threshold = np.percentile(np.unique(adjacency_matrix), 85)
    return adjacency_matrix, threshold
