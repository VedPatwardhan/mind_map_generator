from dotenv import dotenv_values
env = dotenv_values(".env")

def get_contributors():
    contributors = []
    with open(env['CONTRIBUTORS']) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip('\n').lower()
            contributors += lines[i].split()
    return list(set(contributors))


def get_words_to_ignore():
    words_to_ignore = []
    with open(env['WORDS_TO_IGNORE']) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip('\n').lower()
            words_to_ignore += lines[i].split()
    return list(set(words_to_ignore))


def get_urls():
    urls = []
    with open(env['URLS']) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip('\n')
            urls += lines[i].split()
    return urls