from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from pathlib import Path

from database import resumes_collection
from temp_resume import parse_pdf, parse_docx
from similarity_engine import calculate_match_score
from skill_engine import extract_skills
from firebase_auth import verify_firebase_token

app = FastAPI()


origins = [
    "http://localhost:5173",
    "https://airesumecheckerbykhushi.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)



class JobRequest(BaseModel):
    job_description: str




UPLOAD_FOLDER = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB




@app.post("/upload-resume")
def upload_resume(
    file: UploadFile = File(...),
    user=Depends(verify_firebase_token)
):


    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

   
    content = file.file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")

 
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in [".pdf", ".docx"]:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX allowed")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # file save 
    with open(file_path, "wb") as f:
        f.write(content)


    try:
        if file_extension == ".pdf":
            text_data = parse_pdf(file_path)
        else:
            text_data = parse_docx(file_path)
    except Exception:
        raise HTTPException(status_code=500, detail="Error parsing resume")

    
    resumes_collection.delete_many({
        "file_name": file.filename,
        "user_id": user["uid"]
    })

 
    resumes_collection.insert_one({
        "file_name": file.filename,
        "content": text_data,
        "user_id": user["uid"]
    })

    return {
        "message": "Resume uploaded successfully",
        "file_name": file.filename
    }



@app.delete("/clear-resumes")
def clear_resumes(user=Depends(verify_firebase_token)):

    result = resumes_collection.delete_many({
        "user_id": user["uid"]
    })

    return {
        "message": "All resumes deleted successfully",
        "deleted_count": result.deleted_count
    }




@app.post("/rank-resumes")
def rank_resumes(
    request: JobRequest,
    user=Depends(verify_firebase_token)
):

    job_description = request.job_description.strip()

    if not job_description:
        raise HTTPException(status_code=400, detail="Job description cannot be empty")


    all_resumes = list(
        resumes_collection.find({"user_id": user["uid"]})
    )

    if not all_resumes:
        return {
            "total_candidates": 0,
            "ranked_results": []
        }

    ranking_list = []
    job_skills = extract_skills(job_description)

    for resume in all_resumes:

        resume_text = resume.get("content", "")

   
        text_score = calculate_match_score(resume_text, job_description)


        resume_skills = extract_skills(resume_text)

        matched_skills = list(set(resume_skills) & set(job_skills))
        missing_skills = list(set(job_skills) - set(resume_skills))


        skill_score = (
            (len(matched_skills) / len(job_skills)) * 100
            if job_skills else 0
        )

    
        final_score = (0.7 * skill_score) + (0.3 * text_score)

       
        if final_score >= 75:
            fit_label = "Strong Fit"
        elif final_score >= 40:
            fit_label = "Moderate Fit"
        else:
            fit_label = "Weak Fit"

      
        suggestions = []

        if missing_skills:
            suggestions.append(f"Improve in: {', '.join(missing_skills)}")

        if final_score < 40:
            suggestions.append("Low overall match with job description.")

        if final_score >= 75:
            suggestions.append("Highly suitable candidate for this role.")

        ranking_list.append({
            "file_name": resume.get("file_name"),
            "match_score": round(final_score, 2),
            "skill_score": round(skill_score, 2),
            "text_score": round(text_score, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "fit_label": fit_label,
            "suggestions": suggestions,
            "resume_preview": resume_text[:500]
        })

    # Sort by highest score
    ranking_list.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return {
        "total_candidates": len(ranking_list),
        "ranked_results": ranking_list
    }


