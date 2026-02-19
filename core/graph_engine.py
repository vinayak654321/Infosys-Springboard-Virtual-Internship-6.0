import networkx as nx
from core.keyword_extractor import extract_keywords
from core.relation_builder import build_relations

def generate_graph(topic, text, source_map):

    G = nx.Graph()

    G.add_node(topic, size=40, color="white", type="topic")

    keywords = extract_keywords(text)

    # add nodes with source type
    for word in keywords:
        src = source_map.get(word, "general")

        color = {
            "wiki": "#4da6ff",
            "paper": "#00cc66",
            "news": "#ff4d4d",
            "dataset": "#ffaa00",
            "general": "#cccccc"
        }.get(src, "#cccccc")

        G.add_node(word, color=color, type=src)
        G.add_edge(topic, word)

    # relations
    relations = build_relations(text)

    for a, b in relations:
        if a in keywords and b in keywords:
            G.add_edge(a, b)

    return G
