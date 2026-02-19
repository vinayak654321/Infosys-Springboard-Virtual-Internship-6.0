import re

def build_relations(text):

    relations = []
    sentences = re.split(r'[.!?]', text.lower())

    for sent in sentences:

        words = sent.split()

        # pattern: X is Y
        for i in range(len(words)-2):
            if words[i+1] == "is":
                relations.append((words[i], words[i+2]))

        # pattern: X uses Y
        for i in range(len(words)-2):
            if words[i+1] in ["uses","use","using"]:
                relations.append((words[i], words[i+2]))

        # pattern: X in Y
        for i in range(len(words)-2):
            if words[i+1] == "in":
                relations.append((words[i], words[i+2]))

    return relations
