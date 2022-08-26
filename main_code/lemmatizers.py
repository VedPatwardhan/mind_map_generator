from nltk.stem import WordNetLemmatizer
import spacy
import stanza

load_model = spacy.load("en_core_web_sm", disable=["parser", "ner"])
stanza_pipeline = stanza.Pipeline(lang="en", processors="tokenize,mwt,pos,lemma")

cache_nltk = {}
cache_spacy = {}
cache_stanford = {}


def nltk_lemmatizer(sentences):
    lemmatizer = WordNetLemmatizer()
    for i in range(len(sentences)):
        lemma = []
        for word in sentences[i]:
            if word not in cache_nltk.keys():
                lemma.append(lemmatizer.lemmatize(word))
                cache_nltk[word] = lemma[-1]
            else:
                lemma.append(cache_nltk[word])
        sentences[i] = lemma
    return sentences


def spacy_lemmatizer(sentences):
    word_lengths = [len(sentence) for sentence in sentences]
    doc = load_model(" ".join([" ".join(sentence) for sentence in sentences]))
    lemmatized_output = []
    for token in doc:
        if token not in cache_spacy.keys():
            lemmatized_output.append(token.lemma_)
            cache_spacy[token] = lemmatized_output[-1]
        else:
            lemmatized_output.append(cache_spacy[token])
    sentences = []
    curr = 0
    for word_length in word_lengths:
        sentences.append(lemmatized_output[curr : curr + word_length])
        curr += word_length
    return sentences


def stanfordcorenlp_lemmatizer(sentences, special_seq):
    word_lengths = [len(sentence) for sentence in sentences]
    doc = stanza_pipeline(
        " ".join([" ".join(sentence) for sentence in sentences])
    ).to_dict()[0]
    lemmatized_output = []
    for token in doc:
        if token["text"] not in cache_stanford.keys():
            lemmatized_output.append(token["lemma"])
            cache_stanford[token["text"]] = lemmatized_output[-1]
        else:
            lemmatized_output.append(cache_stanford[token["text"]])
    sentences = []
    curr, x, k = 0, 0, 2
    for word_length in word_lengths:
        sentences.append(lemmatized_output[curr : curr + word_length])
        if x % k == 0:
            sentences.append(special_seq)
        x += 1
        curr += word_length
    for i in range(len(sentences)):
        sentences[i] = [word.lower() for word in sentences[i]]
    print('special_seq', special_seq)
    print('sentences', sentences)
    return sentences
