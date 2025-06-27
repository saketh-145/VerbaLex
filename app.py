import streamlit as st
from utils.pdf_reader import extract_text_from_pdf, detect_language
from utils.embedder import chunk_text, embed_chunks
from utils.qa_engine import create_qa_chain
from utils.summarizer import summarize_text
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="VerbaLex - Legal Document Assistant", layout="wide")
st.title("📄 VerbaLex – Multilingual Legal Document Assistant")

# Upload PDF
uploaded_file = st.file_uploader("📤 Upload a legal PDF document", type="pdf")

# Process PDF only if not already done
if uploaded_file and "pdf_text" not in st.session_state:
    with st.spinner("🔍 Extracting and processing PDF..."):
        # Step 1: Extract text
        text = extract_text_from_pdf(uploaded_file)
        st.session_state["pdf_text"] = text

        # Step 2: Detect language
        lang = detect_language(text)
        st.session_state["language"] = lang
        st.success(f"🌐 Detected Language: `{lang}`")

        # Step 3: Chunk and embed
        chunks = chunk_text(text)
        db, chunks = embed_chunks(chunks)
        st.session_state["db"] = db
        st.session_state["chunks"] = chunks
        st.success(f"✅ Document processed: {len(chunks)} chunks embedded successfully.")

# Use cached values
text = st.session_state.get("pdf_text")
chunks = st.session_state.get("chunks")
db = st.session_state.get("db")

# Tabs for Summary and Q&A
if text and chunks and db:
    tab1, tab2 = st.tabs(["📝 Summarization", "💬 Q&A Assistant"])

    with tab1:
        st.subheader("🧠 Document Summarization")
        summary_mode = st.radio("Choose summarization mode:", ["Fast Summary", "Detailed Summary"])

        if st.button("🔎 Generate Summary"):
            with st.spinner("Summarizing... Please wait."):
                if summary_mode == "Fast Summary":
                    summary = summarize_text(text[:3000])
                else:
                    chunk_summaries = []
                    progress = st.progress(0)
                    for i, chunk in enumerate(chunks):
                        try:
                            partial = summarize_text(chunk[:1000])
                            chunk_summaries.append(partial)
                            progress.progress((i + 1) / len(chunks))
                        except Exception as e:
                            chunk_summaries.append("[Summary unavailable]")
                    progress.empty()

                    # Final summarization on combined summaries
                    combined = "\n".join(chunk_summaries)
                    summary = summarize_text(combined[:3000])

            st.success("📋 Summary:")
            st.text_area("Summary Output", summary, height=300)
            st.download_button("📥 Download Summary", summary, file_name="verbalex_summary.txt")

            st.markdown("💡 **Suggested Questions:**")
            st.write("- What is the final court decision?")
            st.write("- Which parties were involved?")
            st.write("- What relief did the petitioners seek?")
            st.write("- Why were the requests rejected initially?")

    with tab2:
        st.subheader("❓ Ask Questions About the Document")
        user_question = st.text_input("Enter your legal question")

        if user_question:
            answer_box = st.empty()
            with answer_box.container():
                with st.spinner("🤖 Thinking..."):
                    qa_chain = create_qa_chain(db)
                    response = qa_chain.invoke(user_question)

                st.success("🧠 Answer:")
                st.write(response['result'])

                with st.expander("📚 Source Chunks"):
                    for i, doc in enumerate(response["source_documents"]):
                        st.markdown(f"**Chunk {i+1}:**")
                        st.write(doc.page_content)

else:
    st.info("📂 Please upload a legal PDF to begin.")
