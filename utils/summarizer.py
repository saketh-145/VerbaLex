from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
import time

load_dotenv()

# Initialize the summarizer chain
def get_summarizer_chain(model_name="llama3-8b-8192"):
    llm = ChatGroq(temperature=0.0, model_name=model_name)
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""
        Summarize the following legal text in a clear, concise paragraph:

        Text:
        {text}

        Summary:
        """
    )
    return LLMChain(llm=llm, prompt=prompt)

# Fast: one-shot summary
def summarize_text(text):
    summarizer = get_summarizer_chain()
    return summarizer.run({"text": text}).strip()

# Detailed: chunked + merged summary
def summarize_chunks(text):
    summarizer = get_summarizer_chain()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_text(text)

    all_summaries = []
    for i, chunk in enumerate(chunks):
        try:
            print(f"Summarizing chunk {i+1}/{len(chunks)}...")
            summary = summarizer.run({"text": chunk})
            all_summaries.append(summary.strip())
            time.sleep(0.3)
        except Exception as e:
            print(f"Error in chunk {i+1}: {e}")
            all_summaries.append("[Summary not available]")

    # Final optional summarization over combined summaries
    combined = "\n".join(all_summaries)
    if len(combined) > 3000:
        return summarize_text(combined[:3000])
    else:
        return combined
