categories = {
    "Programming": [
        "python",
        "java",
        "c",
        "c++",
        "sql"
    ],

    "Machine Learning": [
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "numpy",
        "pandas"
    ],

    "Web Development": [
        "html",
        "css",
        "javascript",
        "react",
        "flask",
        "fastapi",
        "streamlit"
    ],

    "Cloud & DevOps": [
        "aws",
        "azure",
        "docker",
        "git",
        "github",
        "linux"
    ]
}


def categorize_skills(found_skills):
    result = {}

    lower_skills = [skill.lower() for skill in found_skills]

    for category, skills in categories.items():
        result[category] = []

        for skill in skills:
            if skill in lower_skills:
                result[category].append(skill.title())

    return result
