def detect_sections(text):
    text = text.lower()

    sections = {
        "Education": "education" in text,
        "Projects": "project" in text,
        "Experience": "experience" in text,
        "Skills": "skill" in text,
        "Certifications": (
            "certification" in text or
            "certificate" in text
        ),
        "Achievements": "achievement" in text
    }

    return sections