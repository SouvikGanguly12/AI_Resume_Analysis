def score_resume(resume_text, skills, predicted_job):
    score = 0
    suggestion = []
    
    skill_count = len(skills)
    
    if skill_count >= 8:
        score += 40
    elif skill_count >= 5:
        score += 30
    elif skill_count >= 3:
        score += 20
        suggestion.append("Add more relevant skills to your resume.")
    else:
        score += 10
        suggestion.append("Your resume has very few skills. Add more technical skills")
        
    word_count = len(resume_text.split())
    
    if word_count > 300:
        score += 30
    elif word_count > 150:
        score += 20
    else:
        score += 10
        suggestion.append("Your resume content is too short. Add more project and experience details.")
        
    if predicted_job:
        score += 20
        
    keywords = ["project", "experience", "internship", "development", "analysis"]
    keywords_found = sum(1 for word in keywords if word in resume_text.lower())
    
    score += keywords_found*2
    
    if "project" not in resume_text.lower():
        suggestion.append("Add project experience.")
    if "experience" not in resume_text.lower():
        suggestion.append("Add work experience or internship.")
    if "education" not in resume_text.lower():
        suggestion.append("Include education details.")

    project_suggestions = get_project_suggestions(predicted_job)
        
    return score, suggestion, project_suggestions

PROJECT_IDEAS = {
    "Data Scientist": [
        "Build a customer churn prediction model using pandas and scikit-learn (Kaggle dataset)",
        "Create an EDA dashboard for sales data using Streamlit and Plotly",
        "Develop a movie recommendation system with collaborative filtering"
    ],
    "Machine Learning Engineer": [
        "Deploy a computer vision model (image classification) using TensorFlow Serving",
        "Build and optimize an NLP sentiment analysis pipeline with HuggingFace Transformers",
        "Create a real-time ML inference API with FastAPI and Docker"
    ],
    "Software Engineer": [
        "Build a full-stack task management app with Flask/React and PostgreSQL",
        "Create a REST API for a blog platform with JWT authentication",
        "Develop a CLI tool for file organization using Python Click library"
    ],
    "Frontend Developer": [
        "Build a responsive portfolio website with React and Tailwind CSS",
        "Create an interactive data visualization dashboard with D3.js or Chart.js",
        "Develop a PWA e-commerce product page with service workers"
    ],
    "Backend Developer": [
        "Build a scalable microservice with FastAPI, Redis caching, and Docker",
        "Create a real-time chat API using Flask-SocketIO and PostgreSQL",
        "Implement a user authentication system with OAuth and JWT"
    ],
    "DevOps Engineer": [
        "Set up CI/CD pipeline for a Python app using GitHub Actions and Docker",
        "Deploy a Kubernetes cluster on AWS EKS with Terraform infrastructure",
        "Build a monitoring dashboard with Prometheus, Grafana, and ELK stack"
    ],
    "Full Stack Developer": [
        "Build end-to-end e-commerce platform with MERN stack (MongoDB, Express, React, Node)",
        "Create a SaaS dashboard with Next.js, Prisma, and Stripe payments",
        "Develop a collaborative code editor with Socket.io real-time features"
    ],
    "Data Analyst": [
        "Create Power BI/Tableau dashboard for business metrics analysis",
        "Build SQL data pipeline with Apache Airflow for daily reports",
        "Develop Excel VBA automation tool for financial reporting"
    ],
    "NLP Engineer": [
        "Build question-answering system using BERT fine-tuning",
        "Create text summarization app with T5/HuggingFace pipeline",
        "Develop named entity recognition tool for resume parsing"
    ],
    "Cloud Architect": [
        "Design multi-region serverless architecture on AWS Lambda + API Gateway",
        "Set up hybrid cloud solution with Azure Arc and Kubernetes",
        "Build cost-optimized data lake architecture with GCP BigQuery"
    ],
    "Python Developer": [
        "Create Python package for data validation and publish to PyPI",
        "Build async web scraper with asyncio and BeautifulSoup",
        "Develop Discord bot with discord.py and SQLite database"
    ],
    "React Developer": [
        "Build custom React hooks library for state management",
        "Create Next.js app with SSR/SSG and Vercel deployment",
        "Develop React Native mobile app prototype with Expo"
    ]
}

def get_project_suggestions(predicted_job):
    return PROJECT_IDEAS.get(predicted_job, ["Build personal projects showcasing your top matching skills on GitHub"])
