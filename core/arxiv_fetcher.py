import requests
import xml.etree.ElementTree as ET

def search_arxiv_papers(query, max_results=8):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
    r = requests.get(url, timeout=10)

    papers = []
    root = ET.fromstring(r.text)

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
        link = entry.find("{http://www.w3.org/2005/Atom}id").text

        papers.append({
            "title": title.strip(),
            "summary": summary.strip(),
            "link": link.strip()
        })

    return papers
