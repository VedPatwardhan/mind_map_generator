from keybert import KeyBERT
import yake

def yake_extractor(sentences, num_words, top_n):
    language = "en"
    max_ngram_size = num_words
    deduplication_threshold = 0.9
    numOfKeywords = top_n
    custom_kw_extractor = yake.KeywordExtractor(
        lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
    text = ' '.join([' '.join(sentence) for sentence in sentences])
    keywords = custom_kw_extractor.extract_keywords(text)
    for i in range(len(keywords)):
        keywords[i] = keywords[i][1], keywords[i][0]
    keywords.sort(reverse=True)
    return keywords


def bert_extractor(sentences, num_words, top_n):
    text = ' '.join([' '.join(sentence) for sentence in sentences])
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, num_words), top_n=top_n, use_mmr=True)
    keywords = [(value, word) for word, value in keywords]
    return keywords


def generate_indices(keywords, sentences):
    words = []
    for sentence in sentences:
        words += sentence
    indices = {}
    for word in keywords:
        indices[word] = [idx for idx in range(len(words)) if words[idx] == word]
    return indices
