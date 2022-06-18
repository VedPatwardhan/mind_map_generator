from dotenv import dotenv_values
env = dotenv_values(".env")

def get_contributors():
    contributors = []
    with open(env['CONTRIBUTORS']) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip('\n').lower()
            contributors += lines[i].split()
    return set(contributors)


def get_urls():
    urls = []
    with open(env['URLS']) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip('\n')
            urls += lines[i].split()
    return urls