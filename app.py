import streamlit as st
from core.auth import register_user, login_user
from core.dataset_loader import load_data
from core.graph_engine import generate_graph
from core.graph_store import save_graph, load_graph
from core.arxiv_fetcher import search_arxiv_papers
from core.file_loader import read_uploaded_file
from pyvis.network import Network
import streamlit.components.v1 as components

st.set_page_config(page_title="KnowMap Tool", layout="wide")

# --------- MODERN UI STYLE ---------
custom_css = """
<style>
.stApp {
    background: linear-gradient(135deg,#0f172a,#020617);
    color: #e5e7eb;
}
section[data-testid="stSidebar"] {
    background: rgba(15,23,42,0.85);
    backdrop-filter: blur(10px);
}
.stButton>button {
    border-radius: 12px;
    background: linear-gradient(90deg,#6366f1,#22c55e);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    font-weight: 600;
}
.stTextInput>div>div>input {
    border-radius: 10px;
    background: rgba(30,41,59,0.6);
    color: white;
}
.stFileUploader {
    border-radius: 14px;
    border: 1px dashed #475569;
    padding: 10px;
    background: rgba(30,41,59,0.4);
}
h1, h2, h3 {
    letter-spacing: 0.5px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------- SESSION ----------
if "user" not in st.session_state:
    st.session_state.user = None

if "papers" not in st.session_state:
    st.session_state.papers = []

# ================= AUTH SCREEN =================
if st.session_state.user is None:

    st.title("🧠 KnowMap")
    st.subheader("Cross-Domain Knowledge Mapping System")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    # LOGIN
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if login_user(username, password):
                st.session_state.user = username
                st.success("Login successful")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")

    # REGISTER
    with tab2:
        new_user = st.text_input("Choose Username")
        new_pass = st.text_input("Choose Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Register"):
            if new_pass != confirm:
                st.warning("Passwords do not match")
            else:
                if register_user(new_user, new_pass):
                    st.success("Account created! Now login.")
                else:
                    st.error("Username already exists")

    st.stop()

# ================= DASHBOARD =================
st.sidebar.success(f"Logged in as: {st.session_state.user}")

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.experimental_rerun()

st.title("📊 Knowledge Map Dashboard")

col1, col2 = st.columns([2,1])

# -------- LEFT SIDE --------
with col1:

    # Source selection
    sources = st.multiselect(
        "Select Knowledge Sources",
        ["Wikipedia", "News"],
        default=["Wikipedia"]
    )

    topic = st.text_input("Enter Topic")

    # -------- DATASET UPLOAD --------
    uploaded_file = st.file_uploader("Upload Dataset (CSV or TXT)", type=["csv","txt"])

    file_text = ""
    if uploaded_file is not None:
        file_text = read_uploaded_file(uploaded_file)
        st.success("Dataset loaded and will be included in graph")

    # -------- SEARCH PAPERS --------
    if st.button("📄 Search Research Papers"):
        if topic.strip() == "":
            st.warning("Enter topic first")
        else:
            st.session_state.papers = search_arxiv_papers(topic)

    # -------- PAPER SELECTOR --------
    selected_text = ""

    if len(st.session_state.papers) > 0:
        st.subheader("Select Papers to Include")

        for i, p in enumerate(st.session_state.papers):
            if st.checkbox(p["title"], key=f"paper_{i}"):
                selected_text += " " + p["summary"]

            st.caption(p["link"])

    # -------- GENERATE GRAPH --------
    if st.button("🔎 Generate Knowledge Map"):

        if topic.strip() == "":
            st.warning("Please enter a topic")
        else:
            with st.spinner("Building knowledge map..."):

                result = load_data(topic, sources)
                if isinstance(result, tuple):
                    base_text, source_map = result
                else:
                    base_text = result
                    source_map = {}
                text = base_text + " " + selected_text + " " + file_text

                graph = generate_graph(topic, text, source_map)
                save_graph(st.session_state.user, graph)
                st.session_state.graph = graph

                st.success("Knowledge Map Generated!")

# -------- RIGHT SIDE --------
with col2:
    st.subheader("Saved Graph")

    if st.button("Load Last Map"):
        graph = load_graph(st.session_state.user)
        if graph:
            st.session_state.graph = graph
            st.success("Graph loaded")
        else:
            st.warning("No saved graph found")

# -------- GRAPH DISPLAY --------
if "graph" in st.session_state and st.session_state.graph:

    st.subheader("🗺 Knowledge Map Visualization")

    net = Network(height="650px", width="100%", bgcolor="#111111", font_color="white")
    net.from_nx(st.session_state.graph)
    net.save_graph("graph.html")

    HtmlFile = open("graph.html","r",encoding="utf-8")
    components.html(HtmlFile.read(),height=700)
  