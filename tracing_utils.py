from langsmith import traceable


def safe_trace_inputs(inputs: dict) -> dict:
    """Keep input metadata but never upload original text."""
    safe = {}

    for key, value in inputs.items():
        if isinstance(value, str):
            safe[key] = {
                "characters": len(value),
                "content": "[REDACTED]"
            }
        else:
            safe[key] = {
                "type": type(value).__name__
            }

    return safe


def safe_trace_outputs(outputs) -> dict:
    """Record output statistics without recording generated content."""

    if isinstance(outputs, str):
        return {
            "output_characters": len(outputs),
            "content": "[REDACTED]"
        }

    if isinstance(outputs, tuple):
        return {
            "output_type": "tuple",
            "item_count": len(outputs)
        }

    return {
        "output_type": type(outputs).__name__
    }