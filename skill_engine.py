
import re

COMMON_SKILLS = {
    "python": ["python"],
    "fastapi": ["fastapi"],
    "django": ["django"],
    "flask": ["flask"],
    "mongodb": ["mongodb", "mongo db"],
    "sql": ["sql", "structured query language"],
    "mysql": ["mysql"],
    "react": ["react", "reactjs", "react.js"],
    "node": ["node", "nodejs", "node.js"],
    "javascript": ["javascript", "java script", "js"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "docker": ["docker"],
    "aws": ["aws", "amazon web services"],
    "html": ["html"],
    "css": ["css"]
}




def extract_skills(text):

    text = text.lower()
    found_skills = []

    for main_skill, variations in COMMON_SKILLS.items():

        for variation in variations:
            pattern = r"\b" + re.escape(variation) + r"\b"

            if re.search(pattern, text):
                found_skills.append(main_skill)
                break   
    return found_skills