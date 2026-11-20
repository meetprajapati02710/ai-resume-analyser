
import json
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import existing RAG components
from rag.retriever import retrieve_context
from llm_chat import ask_resume_ai


# Dataset paths
EVALUATION_DIR = PROJECT_ROOT / "evaluation"

INPUT_PATH = EVALUATION_DIR / "ragas_dataset.json"

OUTPUT_PATH = EVALUATION_DIR / "ragas_dataset_generated.json"


def collect_evaluation_data():

    # Load questions and reference answers
    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        questions = json.load(file)

    evaluation_data = []

    for index, item in enumerate(questions, start=1):

        question = item["user_input"]
        reference = item["reference"]

        print(f"\nProcessing question {index}: {question}")

        try:
            # Step 1: Retrieve relevant context from FAISS
            context, sources = retrieve_context(question)

            # Step 2: Generate answer using Gemini
            answer = ask_resume_ai(
                resume_text="",
                job_description="",
                user_question=question,
                retrieved_context=context
            )

            # Step 3: Create evaluation record
            record = {
                "user_input": question,
                "retrieved_contexts": [context],
                "response": answer,
                "reference": reference
            }

            evaluation_data.append(record)

            print("Retrieved sources:", sources)
            print("Answer generated successfully.")

        except Exception as e:
            print(f"Error processing question: {question}")
            print("Error:", str(e))

    # Step 4: Save generated dataset separately
    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(
            evaluation_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nEvaluation data collection completed!")
    print(f"Successfully processed: {len(evaluation_data)}")
    print(f"Generated dataset: {OUTPUT_PATH}")


if __name__ == "__main__":
    collect_evaluation_data()
