def get_contributors():
    contributors = []
    with open('contributors.txt') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip('\n').lower()
            contributors += lines[i].split()
    return set(contributors)