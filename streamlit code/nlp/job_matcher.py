import os
import pickle
import json

MODEL_PATH = os.path.join("models", "nlp_model.pkl")

model = None

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
        
else:
    print("Model file not found. Train the model first")
    
def predict_job_role(resume_text):
    if model is None:
        return "Model not Available"
    prediction = model.predict([resume_text])
    return prediction[0]

def get_top_jobs(resume_skills):
    job_roles_path = "data/job_roles.json"
    try:
        with open(job_roles_path, 'r') as f:
            jobs = json.load(f)
        
        # Ensure jobs is always list
        processed_jobs = []
        for title, skills_list in jobs.items():
            processed_jobs.append({
                'title': title,
                'required_skills': skills_list
            })
        
        job_scores = []
        for job in processed_jobs:
            from fuzzywuzzy import fuzz
            job_title = job['title']
            resume_text = ' '.join(resume_skills)  # Simple resume proxy
            
            # Fuzzy title match as fallback
            title_score = fuzz.partial_ratio(job_title.lower(), resume_text.lower())
            
            job_skills = set(job['required_skills'])
            if not job_skills:
                continue
            resume_set = set(resume_skills)
            overlap = len(resume_set & job_skills)
            skill_score = (overlap / len(job_skills)) * 100 if job_skills else 0
            
            # Combined score, lower threshold
            score = max(skill_score, title_score / 4, 5.0)  # Min 5%
            overlapping_skills = list(resume_set & job_skills)
            missing_skills = list(job_skills - resume_set)
            job_scores.append({
                'title': job_title,
                'match_score': round(score, 1),
                'overlapping_skills': overlapping_skills,
                'missing_skills': missing_skills,
                'total_required': len(job_skills)
            })
        
        job_scores.sort(key=lambda x: x['match_score'], reverse=True)
        return [j for j in job_scores if j['match_score'] >= 5][:5]  # Filter low scores
    except Exception as e:
        print(f"Error loading jobs: {e}")
        return []
