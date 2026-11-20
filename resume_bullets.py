import re


def extract_resume_bullets(resume_text):
    """
    Extract bullet points from the resume.
    """

    bullets = []

    for line in resume_text.split("\n"):

        line = line.strip()

        if not line:
            continue

        if (
            line.startswith("-")
            or line.startswith("•")
            or line.startswith("*")
        ):
            bullets.append(line)

    return bullets