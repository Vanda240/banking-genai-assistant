import os
import streamlit as st
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Banking GenAI Assistant",
    page_icon="🏦",
    layout="wide"
)

# ---------- Session state ----------
if "sample_question" not in st.session_state:
    st.session_state.sample_question = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_answer" not in st.session_state:
    st.session_state.current_answer = ""

if "current_sources" not in st.session_state:
    st.session_state.current_sources = []

if "current_query" not in st.session_state:
    st.session_state.current_query = ""

# ---------- Simple custom styling ----------
st.markdown("""
<style>
    .main {
        padding-top: 1.5rem;
    }

    .hero-card {
        background: linear-gradient(135deg, #0f172a, #1e3a8a);
        padding: 1.5rem 1.75rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1.2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        opacity: 0.9;
    }

    .section-card {
        background: #ffffff;
        padding: 1.1rem 1.2rem;
        border-radius: 16px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
        border: 1px solid #eef2f7;
        margin-bottom: 1rem;
    }

    .answer-box {
        background: #f8fafc;
        border-left: 5px solid #2563eb;
        padding: 1rem 1rem;
        border-radius: 10px;
        font-size: 1rem;
        line-height: 1.7;
    }

    .small-label {
        font-size: 0.88rem;
        color: #475569;
        margin-bottom: 0.35rem;
        font-weight: 600;
    }

    .footer-note {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 1rem;
    }

    div[data-testid="stExpander"] details {
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        background: #f8fafc;
    }

    div[data-testid="stExpander"] summary {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.title("⚙️ Controls")
    st.markdown("Use sample questions to quickly test the assistant.")

    sample_questions = [
        "What is a compliance management system?",
        "What are the main components of an effective CMS?",
        "Who is responsible for developing and administering a CMS?",
        "What is FOCUS?",
        "What is the purpose of the Consumer Compliance Examination Manual?",
        "Why is documentation important during an examination?"
    ]

    selected_question = st.selectbox(
        "Sample questions",
        [""] + sample_questions
    )

    if st.button("Use selected question"):
        st.session_state.sample_question = selected_question

    st.markdown("---")
    st.markdown("### Tips")
    st.markdown("""
- Ask direct compliance questions  
- Try broad and edge-case questions  
- Expand sources to verify grounding
""")

# ---------- Hero ----------
st.markdown("""
<div class="hero-card">
    <div class="hero-title">🏦 Banking GenAI Assistant</div>
    <div class="hero-subtitle">
        Ask grounded questions based on indexed FDIC compliance documents.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- Input section ----------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="small-label">Enter your question</div>', unsafe_allow_html=True)

query = st.text_input(
    label="Question",
    value=st.session_state.sample_question,
    label_visibility="collapsed",
    placeholder="Example: What is a compliance management system?"
)

col1, col2 = st.columns([1, 1])
with col1:
    ask_clicked = st.button("Get Answer", use_container_width=True)
with col2:
    clear_clicked = st.button("Clear", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Clear ----------
if clear_clicked:
    st.session_state.sample_question = ""
    st.session_state.chat_history = []
    st.session_state.current_answer = ""
    st.session_state.current_sources = []
    st.session_state.current_query = ""
    st.rerun()

# ---------- Answer flow ----------
if ask_clicked:
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching documents and generating answer..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={"question": query}
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer returned.")
                    sources = data.get("sources", [])
                else:
                    st.error(f"Backend API returned error: {response.status_code}")
                    st.stop()

            except Exception as e:
                st.error(f"Could not connect to backend: {e}")
                st.stop()

        st.session_state.current_query = query
        st.session_state.current_answer = answer
        st.session_state.current_sources = sources

        used_docs = sorted(list(set([s["source_file"] for s in sources])))

        st.session_state.chat_history.append({
            "question": query,
            "answer": answer,
            "sources": sources,
            "documents_used": used_docs,
            "retrieved_chunks": len(sources)
        })

        st.session_state.sample_question = ""

# ---------- Show latest answer ----------
if st.session_state.current_answer:
    left_col, right_col = st.columns([2.2, 1])

    with left_col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Answer")
        st.markdown(
            f'<div class="answer-box">{st.session_state.current_answer}</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Sources")
        for i, source in enumerate(st.session_state.current_sources, start=1):
            with st.expander(
                f"Source {i}: {source['source_file']} | start_index={source['start_index']}"
            ):
                st.write(source["content"][:1500])
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Query Summary")
        st.write(f"**Question:** {st.session_state.current_query}")
        st.write(f"**Retrieved Chunks:** {len(st.session_state.current_sources)}")

        used_docs = sorted(list(set([
            s["source_file"] for s in st.session_state.current_sources
        ])))

        st.write("**Documents Used:**")
        for doc in used_docs:
            st.write(f"- {doc}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Grounding Note")
        st.write(
            "This answer is generated only from the retrieved FDIC document chunks shown below."
        )
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- Chat history ----------
if st.session_state.chat_history:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Chat History")

    recent_chats = list(reversed(st.session_state.chat_history[-5:]))

    for i, chat in enumerate(recent_chats, start=1):
        with st.expander(f"{i}. {chat['question']}"):
            st.markdown(f"**Answer:** {chat['answer']}")
            st.markdown(f"**Retrieved Chunks:** {chat['retrieved_chunks']}")

            if chat.get("documents_used"):
                st.markdown("**Documents Used:**")
                for doc in chat["documents_used"]:
                    st.markdown(f"- {doc}")

            if chat.get("sources"):
                st.markdown("**Sources:**")
                for j, src in enumerate(chat["sources"], start=1):
                    st.markdown(
                        f"- Source {j}: {src['source_file']} | start_index={src['start_index']}"
                    )

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown(
    '<div class="footer-note">Built with Streamlit, FastAPI, LangChain, Chroma, OpenAI embeddings, and FDIC compliance documents.</div>',
    unsafe_allow_html=True
)