"""Streamlit UI only. All RAG logic lives in rag.py."""
import logging
import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="AI Knowledge Base RAG", page_icon="📚", layout="wide")

# Streamlit secrets -> environment variables (so rag.py only ever reads os.environ)
try:
    for _key in ("GROQ_API_KEY", "GROQ_MODEL"):
        if _key in st.secrets and not os.getenv(_key):
            os.environ[_key] = str(st.secrets[_key])
except Exception:
    pass  # no secrets file locally; .env is used instead

import rag  # noqa: E402
from embeddings import Embedder  # noqa: E402
from errors import RAGError  # noqa: E402
from vector_store import VectorStore  # noqa: E402

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@st.cache_resource(show_spinner="Loading embedding model and building the knowledge base index...")
def load_resources():
    embedder = Embedder(rag.EMBEDDING_MODEL_NAME)
    kb_store = rag.build_kb_store(embedder)
    return embedder, kb_store


def render_sources(sources):
    if not sources:
        return
    names = list(dict.fromkeys(s["doc_name"] for s in sources))
    st.markdown("**Sources:** " + ", ".join(f"`{n}`" for n in names))
    for i, s in enumerate(sources, start=1):
        with st.expander(f"[Source {i}] {s['doc_name']} · similarity {s['score']:.3f}"):
            st.text(s["text"])


def tidy(answer: str) -> str:
    return answer.replace("【", "[").replace("】", "]")


# ---------- Load resources ----------
try:
    embedder, kb_store = load_resources()
except RAGError as e:
    st.error(str(e))
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "upload_store" not in st.session_state:
    st.session_state.upload_store = VectorStore(embedder.dim)   # private to this browser session
upload_store = st.session_state.upload_store

# ---------- Sidebar ----------
with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Top K (chunks retrieved)", 1, 10, rag.TOP_K)
    min_score = st.slider("Relevance threshold", 0.0, 0.6, rag.MIN_SCORE, 0.05,
                          help="Chunks with a cosine similarity below this are ignored.")
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.header("Upload documents")
    uploaded_files = st.file_uploader("TXT, MD or PDF", type=["txt", "md", "pdf"], accept_multiple_files=True)
    if st.button("Add to knowledge base", disabled=not uploaded_files, use_container_width=True):
        for f in uploaded_files:
            try:
                with st.spinner(f"Processing {f.name}..."):
                    added = rag.ingest_document(upload_store, embedder, f.name, f.getvalue(),
                                                known_stores=(kb_store,))
                if added == 0:
                    st.info(f"{f.name}: already in the knowledge base, skipped.")
                else:
                    st.success(f"{f.name}: added {added} chunks.")
            except RAGError as e:
                st.error(str(e))
            except Exception:
                logger.exception("Unexpected ingestion error")
                st.error(f"Something went wrong while processing {f.name}.")

    st.header("Knowledge base")
    st.caption(f"Built-in: {len(kb_store.document_names())} documents, {len(kb_store)} chunks")
    st.caption(f"Your uploads (this session only): {len(upload_store.document_names())} documents, {len(upload_store)} chunks")
    with st.expander("Document list"):
        for name in kb_store.document_names() + upload_store.document_names():
            st.write(f"- {name}")

    if not os.getenv("GROQ_API_KEY"):
        st.warning("GROQ_API_KEY is not set. Retrieval works, but answers cannot be generated.")

# ---------- Main ----------
st.title("AI Knowledge Base RAG")
st.caption("Ask questions and get answers grounded in the knowledge base and your uploaded documents, with sources.")

if not st.session_state.messages:
    st.info("Try: *What GPA is needed for the AI internship?* or *Which course teaches MLOps and when?*")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        render_sources(message.get("sources"))

if prompt := st.chat_input("Ask a question about the documents"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching and generating an answer..."):
                out = rag.rag_query(prompt, embedder, [kb_store, upload_store], top_k, min_score)
            answer = tidy(out["answer"])
            st.markdown(answer)
            render_sources(out["sources"])
            st.session_state.messages.append(
                {"role": "assistant", "content": answer, "sources": out["sources"]})
        except RAGError as e:
            st.error(str(e))
        except Exception:
            logger.exception("Unexpected error")
            st.error("An unexpected error occurred. Please try again.")
