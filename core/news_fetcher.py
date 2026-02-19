import requests

API_KEY = "PASTE_YOUR_KEY_HERE"

def fetch_news(topic):
    try:
        url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={API_KEY}&pageSize=5"
        res = requests.get(url, timeout=10).json()

        articles = []
        for a in res.get("articles", []):
            articles.append(a["title"] + " " + (a.get("description") or ""))

        return " ".join(articles)
    except:
        return ""
