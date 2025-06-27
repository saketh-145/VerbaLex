import streamlit as st
from utils.translator import translate_text
from utils.pdf_reader import extract_text_from_pdf, detect_language
from utils.embedder import chunk_text, embed_chunks
from utils.qa_engine import create_qa_chain
from utils.summarizer import summarize_text
from utils.meta_extractor import get_case_summary
from dotenv import load_dotenv
import textwrap

load_dotenv()
st.set_page_config(page_title="VerbaLex", layout="wide")

app_mode = st.sidebar.radio("Go to", ["Document Analyzer", "Translator", "Legal Chatbot"])

# Session state initialization
for key in ["pdf_text", "chunks", "db", "language", "filename", "fast_summary", "chat_history", "case_info"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "chat_history" else []

# Show extracted file info
def display_file_info():
    if st.session_state.get("case_info"):
        st.markdown(
            f"<p style='color:gray; font-size:0.9rem; margin-top:0.5rem;'>{st.session_state['case_info']}</p>",
            unsafe_allow_html=True
        )

# === Document Analyzer ===
if app_mode == "Document Analyzer":
    st.title("VerbaLex – Document Analyzer")
    col1, col2 = st.columns([4, 2])

    with col1:
        uploaded_file = st.file_uploader("Upload Legal PDF", type="pdf", label_visibility="collapsed", key="upload")
        st.caption("Only text-based PDFs supported. Avoid scanned image-only files.")

    with col2:
        display_file_info()

    if uploaded_file and not st.session_state["pdf_text"]:
        with st.spinner("Processing document..."):
            text = extract_text_from_pdf(uploaded_file)
            st.session_state["pdf_text"] = text
            st.session_state["language"] = detect_language(text)
            chunks = chunk_text(text)
            db, chunks = embed_chunks(chunks)
            st.session_state["chunks"] = chunks
            st.session_state["db"] = db
            st.session_state["filename"] = uploaded_file.name
            st.session_state["fast_summary"] = summarize_text(text[:3000])
            st.session_state["case_info"] = get_case_summary(text)
        st.rerun()

    if st.session_state["fast_summary"]:
        st.subheader("Fast Summary")
        st.text_area("Summary", st.session_state["fast_summary"], height=250)

        if st.button("Generate Detailed Summary"):
            with st.spinner("Generating detailed summary..."):
                detailed_parts = []
                progress = st.progress(0)
                for i, chunk in enumerate(st.session_state["chunks"]):
                    try:
                        part = summarize_text(chunk[:1000])
                        detailed_parts.append(part)
                    except:
                        detailed_parts.append("[Summary unavailable]")
                    progress.progress((i + 1) / len(st.session_state["chunks"]))
                progress.empty()
                detailed_summary = summarize_text("\n".join(detailed_parts)[:3000])
                st.text_area("Detailed Summary", detailed_summary, height=300)

# === Translator ===
elif app_mode == "Translator":
    st.title("VerbaLex – Translator")
    display_file_info()

    if st.session_state["pdf_text"]:
        st.subheader("Extracted Text")
        st.text_area("Original", st.session_state["pdf_text"][:2000], height=200)

        lang_choice = st.selectbox("Target Language", ["Hindi", "Telugu", "French", "Spanish", "German"])

        if st.button("Translate Now"):
            with st.spinner(f"Translating to {lang_choice}..."):
                chunks = textwrap.wrap(st.session_state["pdf_text"], 500)
                translated_chunks = []
                progress = st.progress(0)
                for i, chunk in enumerate(chunks):
                    try:
                        translated = translate_text(chunk, lang_choice)
                        translated_chunks.append(translated)
                    except:
                        translated_chunks.append("[Translation Error]")
                    progress.progress((i + 1) / len(chunks))
                st.session_state["translated_text"] = "\n\n".join(translated_chunks)

        if st.session_state.get("translated_text"):
            st.subheader(f"Translation Output ({lang_choice})")
            st.text_area("Translated Text", st.session_state["translated_text"], height=300)
            st.download_button(
                "Download Translated Text",
                st.session_state["translated_text"],
                file_name=f"translated_{lang_choice.lower()}.txt"
            )
    else:
        st.warning("Please upload and analyze a document in the 'Document Analyzer' tab first.")

# === Legal Chatbot ===
elif app_mode == "Legal Chatbot":
    st.title("VerbaLex – Legal Chatbot")
    display_file_info()

    if st.session_state["db"]:
        for msg in st.session_state["chat_history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("Ask a legal question...")

        if user_input:
            st.session_state["chat_history"].append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    qa_chain = create_qa_chain(st.session_state["db"])
                    response = qa_chain.invoke(user_input)
                    answer = response["result"]
                    st.markdown(answer)

            st.session_state["chat_history"].append({"role": "assistant", "content": answer})
    else:
        st.warning("Please upload and analyze a PDF in 'Document Analyzer' first.")
