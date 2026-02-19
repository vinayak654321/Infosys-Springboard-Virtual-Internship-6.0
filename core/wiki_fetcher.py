import wikipedia

def fetch_wikipedia(topic):
    try:
        return wikipedia.summary(topic, sentences=8)
    except:
        return ""
