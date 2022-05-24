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


def get_adjacency_matrix(words, embeddings):
    adjacency_matrix = np.zeros((len(words), len(words)))
    for i in range(0, len(words)):
        adjacency_matrix[0][i] = 1

    for i in range(1, len(words)):
        for j in range(i+1, len(words)):
            adjacency_matrix[i][j] = np.abs(
                np.dot(embeddings[i], embeddings[j]))

    return adjacency_matrix


def get_trained_adjacency_matrix(words, sentences):
    embedder = train_word2vec(sentences)
    wv = embedder.wv
    embeddings = [[]]
    for word in words[1:]:
        embedding = np.array(wv[word])
        embeddings.append(embedding)

    adjacency_matrix = get_adjacency_matrix(words, embeddings)
    for i in range(len(words)):
        for j in range(len(words)):
            print('{:.4f}'.format(adjacency_matrix[i][j]), end='\t')
        print()
    threshold = np.percentile(np.unique(adjacency_matrix), 85)

    return adjacency_matrix, threshold
