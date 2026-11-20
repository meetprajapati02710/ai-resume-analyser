
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

from ragas.llms import llm_factory
from ragas.embeddings import GoogleEmbeddings
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Asynchronous Gemini-compatible client
llm_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Gemini as LLM judge
evaluator_llm = llm_factory(
    model="gemini-2.5-flash",
    client=llm_client,
    max_tokens=8192
)

# Google GenAI client for embeddings
embedding_client = genai.Client(api_key=api_key)

evaluator_embeddings = GoogleEmbeddings(
    client=embedding_client,
    model="gemini-embedding-001"
)

print("RAGAS evaluator configured successfully!")
print("Evaluation model: Gemini 2.5 Flash")
print("Maximum output tokens: 4096")

