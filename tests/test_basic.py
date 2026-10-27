from text_cleaner import clean_text
from skill_extractor import extract_skills

def test_cleaning():
    assert "python" in clean_text("Python   SQL!!!")

def test_skill_extraction():
    skills = extract_skills("I know Python, SQL and Pandas.")
    assert "Python" in skills
    assert "SQL" in skills
