
import json
import sys
import time
import traceback
from pathlib import Path

import pandas as pd

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# RAGAS metrics
from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall
)

# Evaluator configuration
from evaluation.ragas_config import (
    evaluator_llm,
    evaluator_embeddings
)

# File paths
INPUT_PATH = PROJECT_ROOT / "evaluation" / "ragas_dataset_generated.json"
OUTPUT_PATH = PROJECT_ROOT / "evaluation" / "ragas_results.csv"


def evaluate_rag():

    # Load evaluation dataset
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Evaluation dataset not found: {INPUT_PATH}"
        )

    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    if not dataset:
        raise ValueError("Evaluation dataset is empty!")

    print(f"Loaded {len(dataset)} evaluation samples.")

    # Initialize metrics
    metrics = {
        "faithfulness": Faithfulness(
            llm=evaluator_llm
        ),

        "answer_relevancy": AnswerRelevancy(
            llm=evaluator_llm,
            embeddings=evaluator_embeddings
        ),

        "context_precision": ContextPrecision(
            llm=evaluator_llm
        ),

        "context_recall": ContextRecall(
            llm=evaluator_llm
        )
    }

    results = []

    # Evaluate each sample
    for index, item in enumerate(dataset, start=1):

        print("\n" + "=" * 60)
        print(f"Evaluating sample {index}/{len(dataset)}")
        print("Question:", item["user_input"])

        contexts = item["retrieved_contexts"]

        if isinstance(contexts, str):
            contexts = [contexts]

        sample_result = {
            "user_input": item["user_input"]
        }

        # Correct inputs for each metric
        metric_inputs = {

            "faithfulness": {
                "user_input": item["user_input"],
                "response": item["response"],
                "retrieved_contexts": contexts
            },

            "answer_relevancy": {
                "user_input": item["user_input"],
                "response": item["response"]
            },

            "context_precision": {
                "user_input": item["user_input"],
                "reference": item["reference"],
                "retrieved_contexts": contexts
            },

            "context_recall": {
                "user_input": item["user_input"],
                "reference": item["reference"],
                "retrieved_contexts": contexts
            }
        }

        # Run metrics one by one
        for metric_name, metric in metrics.items():

            try:
                print(f"\nRunning {metric_name}...")

                result = metric.score(
                    **metric_inputs[metric_name]
                )

                score = result.value

                sample_result[metric_name] = score

                print(f"{metric_name}: {score:.4f}")

            except Exception as error:

                sample_result[metric_name] = None

                print(f"{metric_name} FAILED")
                print("Error:", repr(error))

                traceback.print_exc()

            # Wait to reduce API rate-limit errors
            if metric_name != "context_recall":
                print("Waiting 20 seconds...")
                time.sleep(20)

        results.append(sample_result)

        # Save after every sample so completed results are retained
        dataframe = pd.DataFrame(results)
        dataframe.to_csv(OUTPUT_PATH, index=False)

    # Final summary
    dataframe = pd.DataFrame(results)

    print("\n" + "=" * 60)
    print("RAGAS EVALUATION SUMMARY")
    print("=" * 60)

    for metric_name in metrics:

        average = dataframe[metric_name].mean()

        if pd.notna(average):
            print(f"{metric_name}: {average:.4f}")
        else:
            print(f"{metric_name}: No valid scores")

    print("\nResults saved to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    evaluate_rag()
