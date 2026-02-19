from core.wiki_fetcher import fetch_wikipedia
from core.news_fetcher import fetch_news

# Arxiv text ab direct load nahi hoga (papers selection se aayega)
def load_data(topic, sources):

    combined_text = ""

    if "Wikipedia" in sources:
        combined_text += fetch_wikipedia(topic) + " "

    if "News" in sources:
        combined_text += fetch_news(topic) + " "

    return combined_text
