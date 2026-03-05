import re

COMMON_SKILLS = {
    "python": ["python"],
    "fastapi": ["fastapi"],
    "django": ["django"],
    "flask": ["flask"],
    "mongodb": ["mongodb", "mongo", "mongo db"],
    "sql": ["sql", "mysql", "postgres"],
    "react": ["react", "reactjs", "react.js"],
    "node": ["node", "nodejs", "node.js"],
    "javascript": ["javascript", "js"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "docker": ["docker"],
    "aws": ["aws", "amazon web services"],
    "html": ["html"],
    "css": ["css"],
    "git": ["git"],
    "api": ["api", "rest api", "restful"]
}


def extract_skills(text):

    text = text.lower()
    found = set()

    for skill, variations in COMMON_SKILLS.items():
        for v in variations:
            if re.search(r"\b" + re.escape(v) + r"\b", text):
                found.add(skill)

    return list(found)