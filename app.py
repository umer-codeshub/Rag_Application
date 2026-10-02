
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
# CHATGPT STYLE UI
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
    ======================================================== */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: "Inter", sans-serif;
    }

    .stApp {
        background: #ffffff;
    }

    .main .block-container {
        max-width: 900px;
        padding-top: 0.5rem;
        padding-bottom: 8rem;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #f7f7f8;
        border-right: 1px solid #e5e5e5;
    }

    section[data-testid="stSidebar"] > div {
        padding: 0.75rem 0.75rem;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #202123;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 10px 18px 10px;
    }

    .sidebar-brand-icon {
        width: 30px;
        height: 30px;
        border-radius: 8px;
        background: #202123;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
    }

    .sidebar-brand-text {
        font-size: 15px;
        font-weight: 600;
        color: #202123;
    }

    .sidebar-section {
        font-size: 11px;
        font-weight: 600;
        color: #8e8e8e;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin: 20px 10px 8px 10px;
    }


    /* ========================================================
       SIDEBAR BUTTONS
       ======================================================== */

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: transparent;
        border: 0;
        color: #343541;
        border-radius: 8px;
        text-align: left;
        padding: 9px 10px;
        font-size: 13px;
        font-weight: 500;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #ececec;
        color: #202123;
    }


    /* ========================================================
       SIDEBAR INPUTS
       ======================================================== */

    section[data-testid="stSidebar"] .stSlider {
        padding: 0 6px;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background: #ffffff;
        border: 1px solid #dedede;
        border-radius: 8px;
    }


    /* ========================================================
       MAIN HEADER
       ======================================================== */

    .top-header {
        height: 58px;
        display: flex;
        align-items: center;
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 1.5rem;
    }

    .model-name {
        font-size: 15px;
        font-weight: 600;
        color: #202123;
    }

    .model-status {
        color: #8e8e8e;
        font-size: 13px;
        margin-left: 7px;
    }


    /* ========================================================
       WELCOME SCREEN
       ======================================================== */

    .welcome {
        min-height: 55vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    .welcome-icon {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        background: #202123;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        margin-bottom: 20px;
    }

    .welcome-title {
        font-size: 28px;
        font-weight: 600;
        color: #202123;
        letter-spacing: -0.03em;
    }

    .welcome-subtitle {
        max-width: 560px;
        color: #6b6b6b;
        font-size: 14px;
        line-height: 1.6;
        margin-top: 10px;
    }


    /* ========================================================
       CHAT MESSAGES
       ======================================================== */

    [data-testid="stChatMessage"] {
        border: none !important;
        background: transparent !important;
        padding: 1.25rem 0 !important;
        margin: 0 !important;
    }

    [data-testid="stChatMessage"] > div:first-child {
        margin-right: 14px;
    }

    [data-testid="stChatMessageContent"] {
        color: #2d2d2d;
        font-size: 15px;
        line-height: 1.7;
    }


    /* ========================================================
       USER MESSAGE
       ======================================================== */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background: #f7f7f8 !important;
        border-radius: 12px !important;
        padding: 1rem 1.1rem !important;
        margin: 0.5rem 0 !important;
    }


    /* ========================================================
       ASSISTANT MESSAGE
       ======================================================== */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background: #ffffff !important;
    }


    /* ========================================================
       CHAT INPUT
       ======================================================== */

    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 18px;
        left: 50%;
        transform: translateX(-50%);
        width: min(850px, calc(100vw - 360px));
        z-index: 999;
    }

    [data-testid="stChatInput"] > div {
        background: #ffffff;
        border: 1px solid #d9d9d9;
        border-radius: 16px;
        box-shadow:
            0 2px 6px rgba(0,0,0,0.05),
            0 8px 24px rgba(0,0,0,0.06);
    }

    [data-testid="stChatInput"] textarea {
        font-size: 15px;
        color: #202123;
        padding: 12px 15px;
    }

    [data-testid="stChatInput"] textarea:focus {
        box-shadow: none !important;
        border-color: transparent !important;
    }


    /* ========================================================
       SOURCES
       ======================================================== */

    .source-header {
        color: #6b6b6b;
        font-size: 12px;
        font-weight: 600;
        margin-top: 14px;
        margin-bottom: 5px;
    }

    [data-testid="stExpander"] {
        border: 1px solid #e5e5e5;
        border-radius: 9px;
        background: #fafafa;
    }


    /* ========================================================
       EMPTY STATE SUGGESTIONS
       ======================================================== */

    .suggestion {
        border: 1px solid #e5e5e5;
        border-radius: 10px;
        padding: 12px 14px;
        margin-top: 8px;
        color: #4b4b4b;
        font-size: 13px;
        text-align: left;
        background: #ffffff;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        position: fixed;
        bottom: 2px;
        left: 50%;
        transform: translateX(-50%);
        color: #9a9a9a;
        font-size: 10px;
        z-index: 1000;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 900px) {

        .main .block-container {
            max-width: 100%;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        [data-testid="stChatInput"] {
            width: calc(100vw - 30px);
        }

        .welcome-title {
            font-size: 24px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# STREAMLIT SECRETS
# ============================================================

try:
    for _key in ("GROQ_API_KEY", "GROQ_MODEL"):
        if _key in st.secrets and not os.getenv(_key):
            os.environ[_key] = str(st.secrets[_key])
except Exception:
    pass


# ============================================================
# IMPORT RAG SYSTEM
# ============================================================

import rag
from embeddings import Embedder
from errors import RAGError
from vector_store import VectorStore


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


# ============================================================
# LOAD RESOURCES
# ============================================================

@st.cache_resource(
    show_spinner="Loading knowledge base..."
)
def load_resources():

    embedder = Embedder(
        rag.EMBEDDING_MODEL_NAME
    )

    kb_store = rag.build_kb_store(
        embedder
    )

    return embedder, kb_store


def render_sources(sources):

    if not sources:
        return

    st.markdown(
        '<div class="source-header">Sources</div>',
        unsafe_allow_html=True,
    )

    names = list(
        dict.fromkeys(
            s["doc_name"]
            for s in sources
        )
    )

    st.caption(
        " · ".join(names)
    )

    for i, s in enumerate(
        sources,
        start=1
    ):

        with st.expander(
            f"Source {i} · {s['doc_name']} · {s['score']:.3f}"
        ):

            st.markdown(
                s["text"]
            )


def tidy(answer: str) -> str:

    return answer.replace(
        "【",
        "["
    ).replace(
        "】",
        "]"
    )


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
        <div class="sidebar-brand">

            <div class="sidebar-brand-icon">
                ✦
            </div>

            <div class="sidebar-brand-text">
                AI Knowledge Base
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # -----------------------------------------
    # New conversation
    # -----------------------------------------

    if st.button(
        "＋  New conversation",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()


    st.markdown(
        '<div class="sidebar-section">Conversation</div>',
        unsafe_allow_html=True,
    )


    if st.session_state.messages:

        st.caption(
            "Current conversation"
        )

        first_user_message = next(
            (
                m["content"]
                for m in st.session_state.messages
                if m["role"] == "user"
            ),
            "New conversation",
        )

        display_title = first_user_message[:42]

        if len(first_user_message) > 42:

            display_title += "..."

        st.markdown(
            f"""
            <div style="
                background:#ececec;
                padding:9px 10px;
                border-radius:8px;
                font-size:13px;
                color:#343541;
                margin-bottom:8px;
            ">
                💬 {display_title}
            </div>
            """,
            unsafe_allow_html=True,
        )


    # -----------------------------------------
    # Retrieval
    # -----------------------------------------

    st.markdown(
        '<div class="sidebar-section">Retrieval settings</div>',
        unsafe_allow_html=True,
    )


    top_k = st.slider(
        "Top K",
        1,
        10,
        rag.TOP_K,
        help="Number of chunks retrieved.",
    )


    min_score = st.slider(
        "Relevance threshold",
        0.0,
        0.6,
        rag.MIN_SCORE,
        0.05,
        help="Chunks below this similarity are ignored.",
    )


    # -----------------------------------------
    # Documents
    # -----------------------------------------

    st.markdown(
        '<div class="sidebar-section">Knowledge base</div>',
        unsafe_allow_html=True,
    )


    uploaded_files = st.file_uploader(
        "Upload documents",
        type=[
            "txt",
            "md",
            "pdf",
        ],
        accept_multiple_files=True,
    )


    if st.button(
        "Add documents",
        disabled=not uploaded_files,
        use_container_width=True,
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
                        f"{f.name} already exists."
                    )

                else:

                    st.success(
                        f"{f.name} added."
                    )


            except RAGError as e:

                st.error(
                    str(e)
                )


            except Exception:

                logger.exception(
                    "Unexpected ingestion error"
                )

                st.error(
                    f"Could not process {f.name}."
                )


    # -----------------------------------------
    # Knowledge base stats
    # -----------------------------------------

    st.markdown(
        '<div class="sidebar-section">Knowledge base</div>',
        unsafe_allow_html=True,
    )


    st.caption(
        f"Built in documents: "
        f"{len(kb_store.document_names())}"
    )


    st.caption(
        f"Built in chunks: "
        f"{len(kb_store)}"
    )


    st.caption(
        f"Your documents: "
        f"{len(upload_store.document_names())}"
    )


    with st.expander(
        "View documents"
    ):

        all_documents = (
            kb_store.document_names()
            + upload_store.document_names()
        )


        if all_documents:

            for name in all_documents:

                st.write(
                    f"📄 {name}"
                )

        else:

            st.caption(
                "No documents."
            )


    # -----------------------------------------
    # API warning
    # -----------------------------------------

    if not os.getenv(
        "GROQ_API_KEY"
    ):

        st.warning(
            "GROQ_API_KEY is not configured."
        )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
    <div class="top-header">

        <span class="model-name">
            AI Knowledge Base
        </span>

        <span class="model-status">
            RAG
        </span>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="welcome">

            <div class="welcome-icon">
                ✦
            </div>

            <div class="welcome-title">
                What can I help you find?
            </div>

            <div class="welcome-subtitle">
                Ask questions about the documents in your
                knowledge base. Answers are generated from
                retrieved document context.
            </div>

            <div style="
                width:100%;
                max-width:600px;
                margin-top:28px;
            ">

                <div class="suggestion">
                    What GPA is needed for the AI internship?
                </div>

                <div class="suggestion">
                    Which course teaches MLOps and when?
                </div>

                <div class="suggestion">
                    Summarize the main requirements from the documents.
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
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
    "Message AI Knowledge Base..."
):

    # User message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )


    with st.chat_message(
        "user"
    ):

        st.markdown(
            prompt
        )


    # Assistant response

    with st.chat_message(
        "assistant"
    ):

        try:

            with st.spinner(
                "Searching..."
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


            st.markdown(
                answer
            )


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
    <div class="footer">
        AI Knowledge Base
    </div>
    """,
    unsafe_allow_html=True,
)
```
