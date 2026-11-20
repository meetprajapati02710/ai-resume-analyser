# AI Resume Analyser & Interview Coach

An AI-powered resume analysis and interview preparation platform built with **Python, Streamlit, LangChain, FAISS, Gemini, RAG, LangSmith, and RAGAS**.

The application helps users analyse their resumes, identify skill gaps, compare resumes with job descriptions, improve resume content, and prepare for technical interviews using an AI-powered Interview Coach.

---

## 🚀 Features

### 📄 Resume Analysis
- Upload and parse resume documents.
- Extract technical and professional skills.
- Analyse resume statistics and sections.
- Identify resume strengths and improvement areas.
- Generate ATS-oriented recommendations.

### 🎯 Job Description Matching
- Compare resume skills with job requirements.
- Identify matching and missing skills.
- Calculate resume-job similarity.
- Provide personalized skill-gap recommendations.

### 🤖 RAG-Powered Resume Chatbot
The application uses **Retrieval-Augmented Generation (RAG)** to answer questions using relevant information from the knowledge base.

RAG pipeline:

```text
User Question
      ↓
Question Embedding
      ↓
FAISS Similarity Search
      ↓
Top Relevant Context
      ↓
Gemini 2.5 Flash
      ↓
Context-Aware Answer
```

### 🧠 AI Interview Coach
The Interview Coach generates personalized technical interview questions and provides answer evaluation and feedback.

Supported interview modes include:

- Quick Interview
- Standard Interview
- Comprehensive Interview
- Company Simulation

The system evaluates responses and provides feedback to help improve technical interview performance.

### 🔎 LangSmith Observability

The project integrates **LangSmith** for monitoring and tracing the RAG pipeline and LLM calls.

The trace structure includes:

```text
Resume RAG Pipeline
│
├── FAISS Context Retrieval
│
└── Gemini Resume Assistant
```

LangSmith is used for:

- LLM tracing
- RAG pipeline monitoring
- Execution tracking
- Token usage tracking
- Debugging and observability

Sensitive resume and retrieved-context content is redacted from traces.

### 📊 RAGAS Evaluation

The project includes a RAG evaluation pipeline using **RAGAS**.

Implemented metrics:

| Metric | Purpose |
|---|---|
| Faithfulness | Measures whether the answer is supported by retrieved context |
| Answer Relevancy | Measures how relevant the generated answer is to the question |
| Context Precision | Measures whether relevant retrieved information is ranked effectively |
| Context Recall | Measures whether the retrieved context contains information needed for the reference answer |

Evaluation workflow:

```text
Evaluation Questions
        ↓
Retrieve Context
        ↓
Generate Answer
        ↓
RAGAS Evaluators
        ↓
Evaluation Metrics
        ↓
CSV Results
```

---

## 🏗️ Project Architecture

```text
AI Resume Analyser
│
├── Streamlit UI
│
├── Resume Processing
│   ├── Resume Parser
│   ├── Skill Extractor
│   ├── Resume Scoring
│   └── Resume Analysis
│
├── Job Matching
│   ├── Similarity Analysis
│   ├── Skill Gap Analysis
│   └── Job Recommendation
│
├── RAG Pipeline
│   ├── Document Loader
│   ├── Text Splitter
│   ├── Embeddings
│   ├── FAISS Vector Store
│   └── Retriever
│
├── Gemini LLM
│
├── LangSmith
│   └── Tracing & Observability
│
└── RAGAS
    └── RAG Evaluation
```

---

## 🧰 Tech Stack

### Programming
- Python

### Frontend
- Streamlit

### Machine Learning / NLP
- Scikit-learn
- Sentence Transformers
- Natural Language Processing

### Generative AI
- Google Gemini 2.5 Flash

### RAG
- LangChain
- FAISS
- Retrieval-Augmented Generation

### Observability
- LangSmith

### Evaluation
- RAGAS

### Data Processing
- NumPy
- Pandas

---

## 📁 Project Structure

```text
ai_resume_analyser/
│
├── app.py
├── chatbot.py
├── interview_coach.py
├── interview_evaluator.py
├── llm_chat.py
├── job_recommender.py
│
├── preprocessing.py
├── resume_parser.py
├── resume_score.py
├── resume_statistics.py
├── resume_strength.py
├── resume_sections.py
├── resume_rewriter.py
├── resume_bullets.py
│
├── skill_extractor.py
├── skill_category.py
├── skill_gap.py
├── similarity.py
├── recommendation.py
├── report_generator.py
│
├── tracing_utils.py
│
├── rag/
│   ├── embeddings.py
│   ├── loader.py
│   ├── qa.py
│   ├── retriever.py
│   ├── splitter.py
│   └── vector_store.py
│
├── evaluation/
│   ├── collect_dataset.py
│   ├── evaluate_rag.py
│   ├── ragas_config.py
│   ├── ragas_dataset.json
│   ├── ragas_dataset_generated.json
│   └── ragas_results.csv
│
├── knowledge_base/
│   ├── ats/
│   ├── career/
│   ├── interview/
│   ├── job_roles/
│   ├── learning/
│   └── resume_examples/
│
├── services/
│   └── resume_service.py
│
├── vector_db/
│   ├── index.faiss
│   └── index.pkl
│
├── data/
│   └── skills.csv
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔄 RAG Implementation

The RAG system uses a knowledge base containing information about:

- ATS optimization
- Resume formatting
- Resume keywords
- LinkedIn
- GitHub
- Interview preparation
- Machine learning
- Deep learning
- LLMs
- Python
- SQL
- AI/ML Engineer roles
- Data Scientist roles
- Software Engineer roles
- Learning roadmaps
- Resume examples

Documents are loaded and split into smaller chunks before being converted into embeddings.

The embeddings are stored in a **FAISS vector database**.

For each user question:

1. The question is received.
2. Relevant documents are retrieved using semantic similarity.
3. Retrieved context is passed to Gemini.
4. Gemini generates a context-aware response.
5. LangSmith records the execution trace while sensitive content is redacted.

---

## 📊 Evaluation

The project contains an evaluation pipeline under:

```text
evaluation/
```

The evaluation dataset contains questions, retrieved contexts, generated responses, and reference answers.

RAGAS evaluates the RAG pipeline using:

```text
Faithfulness
Answer Relevancy
Context Precision
Context Recall
```

Results are stored in:

```text
evaluation/ragas_results.csv
```

> **Note:** RAGAS evaluation using Gemini can be affected by Gemini API rate limits and free-tier quotas. Therefore, the evaluation CSV should be interpreted as the results of the available evaluation runs rather than a permanent benchmark.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/meetprajapati02710/ai-resume-analyser.git
```

### 2. Navigate to the project

```bash
cd ai-resume-analyser
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=AI-Resume-Analyser
```

Never commit your `.env` file or expose API keys publicly.

The repository includes `.env` in `.gitignore`.

---

## ▶️ Run the Application

After activating the virtual environment:

```bash
streamlit run app.py
```

The Streamlit application will start locally.

---

## 🔬 Run RAG Evaluation

Generate the evaluation dataset:

```bash
python -m evaluation.collect_dataset
```

Run the RAGAS evaluation:

```bash
python -m evaluation.evaluate_rag
```

Results are saved to:

```text
evaluation/ragas_results.csv
```

---

## 📈 Observability with LangSmith

To view traces:

1. Configure the LangSmith API key in `.env`.
2. Start the Streamlit application.
3. Interact with the RAG chatbot.
4. Open your LangSmith project.

The RAG execution can be inspected as:

```text
Resume RAG Pipeline
        │
        ├── FAISS Context Retrieval
        │
        └── Gemini Resume Assistant
```

This makes it possible to inspect execution flow, latency, token usage, and failures without exposing raw resume or knowledge-base content in traces.

---

## 🛡️ Security

API credentials are intentionally excluded from the repository.

The following files and directories should not contain secrets:

```text
.env
```

The `.gitignore` file also excludes Python cache files.

If an API key is accidentally exposed, revoke and regenerate it immediately.

---

## 🎯 Future Improvements

Potential future enhancements include:

- DeepEval-based automated regression testing
- Improved retrieval evaluation
- Reranking for better context retrieval
- Hybrid keyword + semantic search
- Automated evaluation datasets
- Resume version comparison
- Job-specific resume optimization
- Deployment using Docker
- Cloud deployment
- CI/CD-based evaluation pipeline

---

## 👨‍💻 Author

**Meet Prajapati**

Data Science Undergraduate | AI/ML Engineer Aspirant

GitHub:  
https://github.com/meetprajapati02710

---

## 📄 License

This project is intended for educational and portfolio purposes.