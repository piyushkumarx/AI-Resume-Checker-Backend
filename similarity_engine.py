from sentence_transformers import SentenceTransformer, util

model = None


def get_model():
    global model

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


def calculate_match_score(resume_text, job_description):

    if not resume_text or not job_description:
        return 0

    model = get_model()

    embeddings = model.encode([resume_text, job_description])

    similarity = util.cos_sim(embeddings[0], embeddings[1])

    score = float(similarity[0][0]) * 100

    return round(score, 2)