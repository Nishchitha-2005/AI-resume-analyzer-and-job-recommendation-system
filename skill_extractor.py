import pandas as pd
import re

def load_skill_dictionary(path="data/skill_dictionary.csv"):
    return pd.read_csv(path)
    pass

def extract_skills(text, skill_dictionary):
    
    found_skills = []
    text_lower = text.lower()

    for _, row in skill_dictionary.iterrows():

        skill = str(row["skill"])
        skill_lower = skill.lower()

        # Escape special characters such as +, # and .
        pattern = r"(?<!\w)" + re.escape(skill_lower) + r"(?!\w)"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(found_skills)


def group_skills_by_category(found_skills, skill_dictionary):

    grouped = {}

    for _, row in skill_dictionary.iterrows():

        skill = str(row["skill"])
        category = str(row["category"])

        if skill in found_skills:

            if category not in grouped:
                grouped[category] = []

            grouped[category].append(skill)

    return grouped