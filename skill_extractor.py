import pandas as pd
import os

def load_skills():
    file_path = os.path.join(
        os.path.dirname(__file__),
        "data",
        "skills.csv"
    )

    skills = pd.read_csv(file_path)

    return skills["skill"].str.lower().tolist()


def extract_skills(text, skill_list):

    text = text.lower()

    found = []

    for skill in skill_list:
        if skill in text:
            found.append(skill.title())

    return sorted(set(found))