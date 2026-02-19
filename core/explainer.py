def explain_node(node, neighbors):

    if not neighbors:
        return f"{node} is an independent concept in this topic."

    explanation = f"{node} is related to "

    explanation += ", ".join(neighbors[:5])

    explanation += ". These relationships were discovered across multiple knowledge sources."

    return explanation
