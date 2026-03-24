import streamlit as st
import os
import tempfile
import json
from parser.docx_parser import parse_resume
from nlp.text_cleaner import clean_text
from nlp.skill_extractor import extract_skills
from nlp.job_matcher import predict_job_role, get_top_jobs
from nlp.resume_scorer import score_resume, get_project_suggestions
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
try:
    import streamlit_confetti as confetti
except ImportError:
    confetti = None

# Page config
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 3rem; color: #1f77b4; text-align: center; margin-bottom: 2rem;}
    .metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 10px;}
    .suggestion-box {background-color: #f0f2f6; padding: 1rem; border-left: 4px solid #1f77b4; margin: 0.5rem 0;}
    .skill-badge {background: #4CAF50; color: white; padding: 0.3rem 0.6rem; border-radius: 15px; margin: 0.2rem; font-size: 0.9rem;}
    .missing-skill {background: #f44336; color: white; padding: 0.3rem 0.6rem; border-radius: 15px; margin: 0.2rem; font-size: 0.9rem;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'last_application' not in st.session_state:
    st.session_state.last_application = None
if 'total_analyses' not in st.session_state:
    st.session_state.total_analyses = 0

# Sidebar
with st.sidebar:
    st.title("📊 AI Resume Analyzer")
    st.markdown("**Upload your resume (PDF/DOCX) and get instant analysis!**")
    st.markdown("### Features:")
    st.markdown("- Skills extraction & gap analysis")
    st.markdown("- Job role matching")
    st.markdown("- Resume scoring & suggestions")
    st.markdown("- Personalized project ideas")
    st.markdown("- One-click job applications")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🔍 Analyze Resume", "📈 Dashboard", "📝 Apply"])

with tab1:
    st.markdown('<h1 class="main-header">AI-Powered Resume Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("""
    ### Transform your resume in minutes!
    
    **What it does:**
    1. **Extracts** skills from your PDF/DOCX resume
    2. **Matches** you to top job roles (90%+ accuracy)
    3. **Scores** your resume (0-100)
    4. **Suggests** skills to learn & projects to build
    5. **Prepares** you for interviews
    
    **Supported Jobs:** Software Engineer, Data Scientist, ML Engineer, Frontend/Backend Dev, DevOps & more!
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.info("✅ Instant analysis")
        st.info("✅ Skills gap analysis")
        st.info("✅ Project recommendations")
    with col2:
        st.success("🚀 Boost your score")
        st.success("💼 Perfect job matches")
        st.success("📱 Mobile-friendly")

with tab2:
    st.header("📤 Upload & Analyze")
    
    col1, col2 = st.columns([2,1])
    
    with col1:
        resume_file = st.file_uploader("Choose your **Resume** (PDF or DOCX)", type=['pdf', 'docx'], key="resume")
        jd_text = st.text_area("**Job Description** (paste text or leave empty for general analysis)", height=150, key="jd")
    
    analyze_btn = st.button("🚀 **ANALYZE RESUME**", type="primary", use_container_width=True)
    
    if analyze_btn and resume_file:
        with st.spinner("Analyzing your resume... This takes ~10 seconds"):
            # Save temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf' if resume_file.name.endswith('.pdf') else '.docx') as tmp:
                tmp.write(resume_file.read())
                resume_path = tmp.name
            
            # Run pipeline
            try:
                resume_text = parse_resume(resume_path)
                if not resume_text.strip():
                    st.error("❌ Could not extract text from resume. Try another file.")
                    os.unlink(resume_path)
                    st.stop()
                
                cleaned = clean_text(resume_text)
                skills = extract_skills(cleaned)
                top_jobs = get_top_jobs(skills)
                predicted_job = predict_job_role(cleaned)
                st.info(f"""
🔍 **Pipeline Debug** 📊
• Raw text len: {len(resume_text)} chars (preview: {resume_text[:100].strip() or 'EMPTY'})
• Skills found: {len(skills)} → {skills[:8] if skills else 'NONE!'}
• Top jobs: {len(top_jobs)} → {[j.get('title','?')[:20] for j in top_jobs[:3]] if top_jobs else 'ERROR/EMPTY!'}
• Predicted: {predicted_job}
                """)
                
                score_val, suggestions, project_suggestions = score_resume(cleaned, skills, predicted_job)
                
                # Store results
                st.session_state.analysis_results = {
                    'score': score_val,
                    'skills': skills,
                    'predicted_job': predicted_job,
                    'top_jobs': top_jobs,
                    'suggestions': suggestions,
                    'project_suggestions': project_suggestions,
                    'resume_text': resume_text[:1500] + '...' if len(resume_text) > 1500 else resume_text
                }
                st.session_state.total_analyses += 1
                
                st.success("✅ Analysis complete!")
                
                # Cleanup
                os.unlink(resume_path)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                if 'resume_path' in locals():
                    os.unlink(resume_path)
    
    # Results
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        
        # Score
        col_score1, col_score2 = st.columns(2)
        with col_score1:
            st.metric("📊 Resume Score", f"{results['score']}/100", delta=None)
        with col_score2:
            gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = results['score'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Score"},
                delta = {'reference': 80},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps' : [
                        {'range': [0, 60], 'color': "lightgray"},
                        {'range': [60, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': 'red', 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            gauge.update_layout(height=300, font={'size': 18})
            st.plotly_chart(gauge, use_container_width=True)
        
        # Skills
        st.subheader("🛠️ Extracted Skills")
        skill_cols = st.columns(4)
        for i, skill in enumerate(results['skills'][:16]):
            with skill_cols[i % 4]:
                st.markdown(f'<span class="skill-badge">{skill.title()}</span>', unsafe_allow_html=True)
        if len(results['skills']) > 16:
            st.caption(f"... and {len(results['skills']) - 16} more")
        
        # Top Jobs
        st.subheader("💼 Top Job Matches")
        df_jobs = pd.DataFrame(results['top_jobs']) if results.get('top_jobs') else pd.DataFrame()
        if df_jobs.empty:
            st.warning(f"💡 **No strong job matches** (need >10% skill overlap).\\n**Predicted role:** {results.get('predicted_job', 'Unknown')}\\n**Tip:** Resumes need explicit skills e.g. 'Python', 'SQL', 'React'.")
        else:
            fig = px.bar(df_jobs.head(5), x='title', y='match_score', 
                         title="💼 Top Job Matches", color='match_score', 
                         color_continuous_scale='viridis',
                         height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            for idx, job in df_jobs.head(3).iterrows():
                with st.expander(f"**{job['title']}** ({job['match_score']}%)", expanded=False):
                    col_overlap, col_missing = st.columns(2)
                    with col_overlap:
                        st.markdown("**✅ You have:**")
                        for s in job['overlapping_skills'][:10]:
                            st.markdown(f'<span class="skill-badge">{s}</span>', unsafe_allow_html=True)
                    with col_missing:
                        st.markdown("**❌ To learn:**")
                        for s in job['missing_skills'][:10]:
                            st.markdown(f'<span class="missing-skill">{s}</span>', unsafe_allow_html=True)
        
        # Predictions & Suggestions
        if results['predicted_job']:
            st.info(f"🎯 **Predicted Role:** {results['predicted_job']}")
        
        with st.expander("💡 Improvement Suggestions"):
            for sug in results['suggestions']:
                st.markdown(f'<div class="suggestion-box">{sug}</div>', unsafe_allow_html=True)
        
        with st.expander("🔥 Project Ideas"):
            st.markdown(f"**For {results['predicted_job'] or 'your skills'}:**")
            for proj in results['project_suggestions'][:5]:
                st.markdown(f'• {proj}')

with tab3:
    st.header("📊 Dashboard")
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Analyses", st.session_state.total_analyses)
        with col2:
            st.metric("Latest Score", f"{results['score']}/100")
        with col3:
            st.metric("Skills Found", len(results['skills']))
        
        # Recent analysis
        recent_df = pd.DataFrame([{
            'Job': results.get('predicted_job', 'N/A'),
            'Score': results['score'],
            'Skills': len(results['skills']),
            'Date': 'Today'
        }])
        st.dataframe(recent_df, use_container_width=True)
        
        # Top roles pie
        if results['top_jobs']:
            top3 = results['top_jobs'][:3]
            fig_pie = px.pie(values=[j['match_score'] for j in top3], 
                            names=[j['title'] for j in top3], 
                            title="Top Job Matches Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("👆 Run an analysis first to see dashboard stats!")

with tab4:
    st.header("📋 Job Application")
    if st.session_state.analysis_results and st.session_state.analysis_results.get('top_jobs'):
        top_jobs = st.session_state.analysis_results['top_jobs']
        job_idx = st.selectbox("Select Job to Apply:", 
                              range(len(top_jobs)), 
                              format_func=lambda i: f"{top_jobs[i]['title']} ({top_jobs[i]['match_score']}%)")
        job = top_jobs[job_idx]
        
        with st.form("apply_form"):
            st.subheader(f"Apply for: **{job['title']}**")
            full_name = st.text_input("Full Name *", key="name")
            email = st.text_input("Email *", key="email")
            phone = st.text_input("Phone", key="phone")
            cover_letter = st.text_area("Cover Letter * (highlight why you fit this role)", height=200, key="cover")
            submitted = st.form_submit_button("🚀 Submit Application", use_container_width=True)
            
            if submitted:
                if full_name and email and cover_letter:
                    st.session_state.last_application = {
                        'job_title': job['title'],
                        'name': full_name,
                        'email': email,
                        'submitted': True
                    }
                    st.success(f"🎉 Thank you, **{full_name}**! Application for **{job['title']}** submitted successfully!")
                    if confetti:
                        confetti.confetti()
                else:
                    st.error("Please fill all required fields (*)")
            else:
                st.warning("👆 Complete an analysis first to unlock applications!")

# Footer
st.markdown("---")
st.markdown("*Built with ❤️ using Streamlit | v1.0*")

