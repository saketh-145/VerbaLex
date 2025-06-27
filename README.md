# VerbaLex – AI-Powered Legal Document Analyzer

VerbaLex is an AI-driven legal assistant that analyzes, summarizes, translates, and interacts with uploaded legal documents in PDF format.

##  Features

### 1. Document Analyzer
- Upload any text-based legal PDF.
- Automatically extracts, chunkifies, and embeds the document.
- Provides:
  - Fast summary
  - Option to generate a detailed summary
  - Extracted metadata (case type, date, court)

### 2. Translator
- Translate extracted content into:
  - Hindi
  - Telugu
  - French
  - Spanish
  - German

### 3. Legal Chatbot
- Conversational interface to ask questions about the document.
- Context-aware Q&A using LangChain and vector store.

---

## ⚙️ Technologies Used

| Layer            | Tech Stack                                       |
|------------------|--------------------------------------------------|
| Frontend         | Streamlit                                        |
| PDF Handling     | PyMuPDF                                           |
| Embeddings       | HuggingFace + FAISS via LangChain                |
| Language Detection | langdetect                                      |
| Summarization    | HuggingFace Transformers                         |
| Translation      | Helsinki-NLP / AI4Bharat models (via Transformers) |
| Vector DB        | FAISS                                             |
| Chat Interface   | LangChain, OpenAI-compatible chain (local/Groq)   |

---

##  Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/your-username/verbalex.git
cd verbalex
````

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add environment variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key
```

### 5. Run the app

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
verbalex/
├── app.py
├── requirements.txt
├── .env
├── utils/
│   ├── pdf_reader.py
│   ├── embedder.py
│   ├── qa_engine.py
│   ├── summarizer.py
│   ├── meta_extractor.py
│   └── translator.py
```

---

## ✅ Todo / Future Features

* Case classification
* OCR support for scanned documents
* Export summaries to Word/PDF
* Admin dashboard for legal data logs

---