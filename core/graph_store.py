import pickle
import os

os.makedirs("graphs", exist_ok=True)

def save_graph(user, graph):
    with open(f"graphs/{user}.pkl", "wb") as f:
        pickle.dump(graph, f)

def load_graph(user):
    try:
        with open(f"graphs/{user}.pkl", "rb") as f:
            return pickle.load(f)
    except:
        return None
