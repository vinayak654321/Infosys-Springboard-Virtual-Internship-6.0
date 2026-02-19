import pandas as pd

def read_uploaded_file(uploaded_file):
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            text = " ".join(df.astype(str).values.flatten())

        elif uploaded_file.name.endswith(".txt"):
            text = uploaded_file.read().decode("utf-8")

        else:
            return ""

        return text[:10000]

    except Exception as e:
        print("File read error:", e)
        return ""
