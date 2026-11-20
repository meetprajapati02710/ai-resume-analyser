def calculate_resume_score(
    ats_score,
    resume_skills,
    missing_skills,
    resume_text
):
    score = 0

    # ATS Score (50 Marks)
    score += ats_score * 0.5

    # Skills Count (20 Marks)
    if len(resume_skills) >= 15:
        score += 20
    elif len(resume_skills) >= 10:
        score += 15
    elif len(resume_skills) >= 5:
        score += 10
    else:
        score += 5

    # Missing Skills (20 Marks)
    if len(missing_skills) == 0:
        score += 20
    elif len(missing_skills) <= 2:
        score += 15
    elif len(missing_skills) <= 5:
        score += 10
    else:
        score += 5

    # Resume Length (10 Marks)
    words = len(resume_text.split())

    if words >= 300:
        score += 10
    elif words >= 200:
        score += 8
    elif words >= 100:
        score += 5
    else:
        score += 2

    return round(score, 2)