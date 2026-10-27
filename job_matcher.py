import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_job_roles(path="data/job_roles.csv"):
    return pd.read_csv(path)


def calculate_match_scores(resume_text, job_roles):

    documents = [resume_text]

    for _, row in job_roles.iterrows():
        documents.append(str(row["skills"]) + " " + str(row["description"]))

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    resume_vector = tfidf_matrix[0]

    job_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(
        resume_vector,
        job_vectors
    )[0]

    results = job_roles.copy()

    results["match_score"] = similarities * 100

    results["match_score"] = results["match_score"].round(2)

    results = results.sort_values(
        by="match_score",
        ascending=False
    ).reset_index(drop=True)

    return results


def get_required_skills(job_row):

    skills = str(job_row["skills"])

    return [
        skill.strip()
        for skill in skills.split(",")
        if skill.strip()
    ]


def calculate_skill_gap(found_skills, required_skills):

    found_lower = {
        skill.lower()
        for skill in found_skills
    }

    matched = []
    missing = []

    for skill in required_skills:

        if skill.lower() in found_lower:
            matched.append(skill)

        else:
            missing.append(skill)

    return matched, missing


def calculate_skill_match_percentage(found_skills, required_skills):

    if not required_skills:
        return 0

    found_lower = {
        skill.lower()
        for skill in found_skills
    }

    matched_count = 0

    for skill in required_skills:

        if skill.lower() in found_lower:
            matched_count += 1

    percentage = (
        matched_count / len(required_skills)
    ) * 100

    return round(percentage, 2)