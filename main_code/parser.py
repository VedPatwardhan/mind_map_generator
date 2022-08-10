import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def get_webpage_content(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup, url.split("/")[-2].lower()


def extract_table_content(soup):
    rows = soup.find("table").find_all("tr")[1:]
    stop_words = set(stopwords.words("english"))
    sentences = []
    for row in rows:
        sent_tokens = word_tokenize(row.find_all("td")[1].text.strip("\n"))
        filtered_tokens = [
            w.lower()
            for w in sent_tokens
            if not w.lower() in stop_words and w.isalpha()
        ]
        sentences.append(filtered_tokens)
    return sentences


def get_text(url):
    soup, heading = get_webpage_content(url)
    sentences = extract_table_content(soup)
    return sentences, heading
