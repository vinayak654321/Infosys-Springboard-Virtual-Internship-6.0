from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(text):
    if not text:
        return []

    vectorizer = TfidfVectorizer(stop_words="english", max_features=15)
    X = vectorizer.fit_transform([text])
    return vectorizer.get_feature_names_out().tolist()
