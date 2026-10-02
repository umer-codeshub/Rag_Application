
"""Streamlit UI only. All RAG logic lives in rag.py."""
import logging
import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Knowledge Base",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PROFESSIONAL UI STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Global ---------- */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #f8fafc;
        color: #111827;
    }

    .main .block-container {
        max-width: 1180px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.5rem 1.15rem;
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #111827;
        font-weight: 650;
        letter-spacing: -0.02em;
    }

    /* ---------- Sidebar headings ---------- */

    .sidebar-section-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 1.6rem;
        margin-bottom: 0.7rem;
    }

    /* ---------- Header ---------- */

    .app-header {
        margin-bottom: 2rem;
    }

    .app-eyebrow {
        display: inline-flex;
        align-items: center;
        padding: 0.35rem 0.7rem;
        border: 1px solid #dbe3ef;
        border-radius: 999px;
        background: #ffffff;
        color: #475569;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.85rem;
    }

    .app-title {
        font-size: 2.45rem;
        line-height: 1.1;
        font-weight: 700;
        letter-spacing: -0.045em;
        color: #0f172a;
        margin: 0;
    }

    .app-subtitle {
        margin-top: 0.7rem;
        max-width: 720px;
        color: #64748b;
        font-size: 1rem;
        line-height: 1.65;
    }

    /* ---------- Chat area ---------- */

    .chat-container {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1rem;
        margin-top: 1rem;
    }

    /* ---------- Chat messages ---------- */

    [data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.6rem;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background: #f1f5f9;
        border: 1px solid #e2e8f0;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background: #ffffff;
        border: 1px solid #e5e7eb;
    }

    /* ---------- Source section ---------- */

    .source-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-top: 0.8rem;
        margin-bottom: 0.4rem;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        border-radius: 9px;
        border: 1px solid #d1d5db;
        background: #ffffff;
        color: #111827;
        font-weight: 600;
        min-height: 42px;
        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        border-color: #94a3b8;
        background: #f8fafc;
        color: #111827;
    }

    /* ---------- Primary buttons ---------- */

    .stButton > button[kind="primary"] {
        background: #111827;
        color: #ffffff;
        border-color: #111827;
    }

    .stButton > button[kind="primary"]:hover {
        background: #1f2937;
        border-color: #1f2937;
        color: #ffffff;
    }

    /* ---------- File uploader ---------- */

    [data-testid="stFileUploader"] {
        border: 1px dashed #cbd5e1;
        border-radius: 12px;
        background: #f8fafc;
        padding: 0.25rem;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #94a3b8;
    }

    /* ---------- Sliders ---------- */

    [data-testid="stSlider"] {
        padding-top: 0.25rem;
    }

    /* ---------- Expander ---------- */

    [data-testid="stExpander"] {
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        background: #ffffff;
    }

    /* ---------- Info / Warning / Error ---------- */

    [data-testid="stAlert"] {
        border-radius: 10px;
        border-width: 1px;
    }

    /* ---------- Chat input ---------- */

    [data-testid="stChatInput"] {
        padding-bottom: 1rem;
    }

    [data-testid="stChatInput"] textarea {
        border-radius: 12px;
        border: 1px solid #cbd5e1;
        background: #ffffff;
        font-size: 0.95rem;
    }

    [data-testid="stChatInput"] textarea:focus {
        border-color: #64748b;
        box-shadow: 0 0 0 1px #64748b;
    }

    /* ---------- Knowledge base cards ---------- */

    .stat-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.5rem;
    }

    .stat-label {
        color: #64748b;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .stat-value {
        color: #0f172a;
        font-size: 1.15rem;
        font-weight: 700;
        margin-top: 0.15rem;
    }

    /* ---------- Empty state ---------- */

    .empty-state {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin: 2rem 0 1rem 0;
    }

    .empty-icon {
        width: 48px;
        height: 48px;
        margin: 0 auto 1rem auto;
        border-radius: 12px;
        background: #f1f5f9;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
    }

    .empty-title {
        color: #111827;
        font-size: 1.05rem;
        font-weight: 650;
        margin-bottom: 0.4rem;
    }

    .empty-text {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* ---------- Footer ---------- */

    .app-footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.75rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #e5e7eb;
    }

    /* ---------- Mobile ---------- */

    @media (max-width: 768px) {

        .main .block-container {
            padding: 1.5rem 1rem 3rem 1rem;
        }

        .app-title {
            font-size: 2rem;
        }

        .app-subtitle {
            font-size: 0.9rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# ENVIRONMENT
# ============================================================

try:
    for _key in ("GROQ_API_KEY", "GROQ_MODEL"):
        if _key in st.secrets and not os.getenv(_key):
            os.environ[_key] = str(st.secrets[_key])
except Exception:
    pass

import rag
from embeddings import Embedder
from errors import RAGError
from vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================
# RESOURCE LOADING
# ============================================================

@st.cache_resource(
    show_spinner="Loading knowledge base..."
)
def load_resources():
    embedder = Embedder(rag.EMBEDDING_MODEL_NAME)
    kb_store = rag.build_kb_store(embedder)
    return embedder, kb_store


def render_sources(sources):
    if not sources:
        return

    st.markdown(
        '<div class="source-label">Sources</div>',
        unsafe_allow_html=True,
    )

    names = list(
        dict.fromkeys(
            s["doc_name"]
            for s in sources
        )
    )

    st.caption(" · ".join(names))

    for i, s in enumerate(sources, start=1):
        with st.expander(
            f"Source {i}  ·  {s['doc_name']}  ·  {s['score']:.3f}"
        ):
            st.markdown(
                f"""
                <div style="
                    color:#475569;
                    font-size:0.9rem;
                    line-height:1.7;
                    padding:0.25rem 0;
                ">
                    {s["text"]}
                </div>
                """,
                unsafe_allow_html=True,
            )


def tidy(answer: str) -> str:
    return answer.replace("【", "[").replace("】", "]")


# ============================================================
# LOAD RESOURCES
# ============================================================

try:
    embedder, kb_store = load_resources()

except RAGError as e:
    st.error(str(e))
    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "upload_store" not in st.session_state:
    st.session_state.upload_store = VectorStore(
        embedder.dim
    )

upload_store = st.session_state.upload_store


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:1.35rem;
            font-weight:700;
            letter-spacing:-0.03em;
            color:#0f172a;
            margin-bottom:0.2rem;
        ">
            Knowledge Base
        </div>

        <div style="
            color:#64748b;
            font-size:0.82rem;
            margin-bottom:1.5rem;
        ">
            Retrieval augmented workspace
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section-title">Retrieval</div>',
        unsafe_allow_html=True,
    )

    top_k = st.slider(
        "Top K",
        1,
        10,
        rag.TOP_K,
        help="Number of document chunks retrieved for each question.",
    )

    min_score = st.slider(
        "Relevance threshold",
        0.0,
        0.6,
        rag.MIN_SCORE,
        0.05,
        help="Chunks below this similarity score are ignored.",
    )

    st.markdown(
        '<div class="sidebar-section-title">Conversation</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "Clear conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        '<div class="sidebar-section-title">Documents</div>',
        unsafe_allow_html=True,
    )

    uploaded_files = st.file_uploader(
        "Upload TXT, MD or PDF files",
        type=["txt", "md", "pdf"],
        accept_multiple_files=True,
        label_visibility="visible",
    )

    if st.button(
        "Add to knowledge base",
        disabled=not uploaded_files,
        use_container_width=True,
        type="primary",
    ):

        for f in uploaded_files:

            try:

                with st.spinner(
                    f"Processing {f.name}..."
                ):

                    added = rag.ingest_document(
                        upload_store,
                        embedder,
                        f.name,
                        f.getvalue(),
                        known_stores=(kb_store,),
                    )

                if added == 0:

                    st.info(
                        f"{f.name} is already in the knowledge base."
                    )

                else:

                    st.success(
                        f"{f.name} added, {added} chunks."
                    )

            except RAGError as e:

                st.error(str(e))

            except Exception:

                logger.exception(
                    "Unexpected ingestion error"
                )

                st.error(
                    f"Something went wrong while processing {f.name}."
                )

    st.markdown(
        '<div class="sidebar-section-title">Knowledge base</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">Documents</div>
                <div class="stat-value">
                    {len(kb_store.document_names())}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">Chunks</div>
                <div class="stat-value">
                    {len(kb_store)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption(
        f"Session uploads: {len(upload_store.document_names())} documents, "
        f"{len(upload_store)} chunks"
    )

    with st.expander("View documents"):

        all_documents = (
            kb_store.document_names()
            + upload_store.document_names()
        )

        if all_documents:

            for name in all_documents:
                st.markdown(
                    f"📄 `{name}`"
                )

        else:

            st.caption(
                "No documents available."
            )

    if not os.getenv("GROQ_API_KEY"):

        st.warning(
            "GROQ_API_KEY is not configured. "
            "Retrieval will work, but answer generation will not."
        )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
    <div class="app-header">

        <div class="app-eyebrow">
            📚 Knowledge Retrieval
        </div>

        <h1 class="app-title">
            AI Knowledge Base
        </h1>

        <div class="app-subtitle">
            Ask questions across your documents and receive
            grounded answers with transparent source references.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# EMPTY STATE
# ============================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="empty-state">

            <div class="empty-icon">
                📖
            </div>

            <div class="empty-title">
                Ask something about your knowledge base
            </div>

            <div class="empty-text">
                Your questions are answered using the documents
                available in the knowledge base.
                Try asking about a specific topic, requirement,
                course, concept, or document.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Example: What GPA is needed for the AI internship?"
    )

    st.caption(
        "Example: Which course teaches MLOps and when?"
    )


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        render_sources(
            message.get("sources")
        )


# ============================================================
# CHAT INPUT
# ============================================================

if prompt := st.chat_input(
    "Ask a question about your documents..."
):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        try:

            with st.spinner(
                "Searching the knowledge base..."
            ):

                out = rag.rag_query(
                    prompt,
                    embedder,
                    [
                        kb_store,
                        upload_store,
                    ],
                    top_k,
                    min_score,
                )

            answer = tidy(
                out["answer"]
            )

            st.markdown(answer)

            render_sources(
                out["sources"]
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": out["sources"],
                }
            )

        except RAGError as e:

            st.error(
                str(e)
            )

        except Exception:

            logger.exception(
                "Unexpected error"
            )

            st.error(
                "An unexpected error occurred. Please try again."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="app-footer">
        AI Knowledge Base · Retrieval augmented generation
    </div>
    """,
    unsafe_allow_html=True,
)

