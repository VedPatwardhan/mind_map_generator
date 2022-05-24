from nltk.stem import WordNetLemmatizer
import spacy
import stanza

load_model = spacy.load('en_core_web_sm', disable = ['parser','ner'])
stanza_pipeline = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma')

def nltk_lemmatizer(sentences):
    lemmatizer = WordNetLemmatizer()
    for i in range(len(sentences)):
        sentences[i] = [lemmatizer.lemmatize(word) for word in sentences[i]]
    return sentences
    
def spacy_lemmatizer(sentences):
    word_lengths = [len(sentence) for sentence in sentences]
    doc = load_model(' '.join([' '.join(sentence) for sentence in sentences]))
    lemmatized_output = [token.lemma_ for token in doc]
    sentences = []
    curr = 0
    for word_length in word_lengths:
        sentences.append(lemmatized_output[curr:curr+word_length])
        curr += word_length
    return sentences

def stanfordcorenlp_lemmatizer(sentences):
    word_lengths = [len(sentence) for sentence in sentences]
    lemmatized_output = stanza_pipeline(' '.join([' '.join(sentence) for sentence in sentences])).to_dict()[0]
    lemmatized_output = [token['lemma'] for token in lemmatized_output]
    sentences = []
    curr = 0
    for word_length in word_lengths:
        sentences.append(lemmatized_output[curr:curr+word_length])
        curr += word_length
    return sentences