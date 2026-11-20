import re


SECTION_HEADERS = {
    "Projects": [
        "projects",
        "project",
        "academic projects",
        "personal projects"
    ],

    "Experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "internship",
        "internships"
    ]
}


def extract_resume_sections(resume_text):
    """
    Extract Projects and Experience sections from resume.

    Returns:
    {
        "Projects": [...],
        "Experience": [...]
    }
    """

    sections = {
        "Projects": [],
        "Experience": []
    }

    current_section = None

    lines = [line.strip() for line in resume_text.splitlines()]

    for line in lines:

        if not line:
            continue

        lower = line.lower().rstrip(":")

        # ----------------------------
        # Detect section heading
        # ----------------------------

        found = False

        for section, headers in SECTION_HEADERS.items():

            if lower in headers:
                current_section = section
                found = True
                break

        if found:
            continue

        # ----------------------------
        # Stop when another ALL CAPS heading appears
        # ----------------------------

        if (
            current_section
            and re.fullmatch(r"[A-Z][A-Z\s]+", line)
        ):
            current_section = None
            continue

        # ----------------------------
        # Save line
        # ----------------------------

        if current_section:
            sections[current_section].append(line)

    return sections