def recommend_jobs(found_skills):

    skills = [skill.lower() for skill in found_skills]

    jobs = []

    if "machine learning" in skills or "tensorflow" in skills:
        jobs.append("Machine Learning Engineer")

    if "deep learning" in skills or "pytorch" in skills:
        jobs.append("Deep Learning Engineer")

    if "python" in skills and "pandas" in skills:
        jobs.append("Data Scientist")

    if "sql" in skills:
        jobs.append("Data Analyst")

    if "fastapi" in skills or "flask" in skills:
        jobs.append("AI Backend Developer")

    if "streamlit" in skills:
        jobs.append("ML Application Developer")

    if "docker" in skills or "aws" in skills:
        jobs.append("MLOps Engineer")

    return list(set(jobs))