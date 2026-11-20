import re

def clean_text(text):
    """
    Clean the extracted resume text.
    """

    # Convert to lowercase
    text = text.lower()

    # Remove newline characters
    text = text.replace("\n", " ")

    # Remove tabs
    text = text.replace("\t", " ")

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Remove special characters except letters, numbers and spaces
    text = re.sub(r"[^a-zA-Z0-9 ]", "", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text