from resume_parser import extract_text_from_pdf
from preprocessing import clean_text
from resume_statistics import resume_statistics
from resume_sections import detect_sections
from skill_extractor import extract_skills
from skill_category import categorize_skills


def analyze_resume(pdf_path, skills):

    resume_text = extract_text_from_pdf(pdf_path)

    cleaned_text = clean_text(resume_text)

    words, characters, lines = resume_statistics(
        resume_text
    )

    sections = detect_sections(cleaned_text)

    found_skills = extract_skills(
        cleaned_text,
        skills
    )

    categorized = categorize_skills(
        found_skills
    )

    return {
        "resume_text": resume_text,
        "cleaned_text": cleaned_text,
        "words": words,
        "characters": characters,
        "lines": lines,
        "sections": sections,
        "found_skills": found_skills,
        "categorized": categorized
    }