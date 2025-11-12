import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime

# Page config
st.set_page_config(page_title="IT Career Guidance", page_icon="💼", layout="wide")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 'career'
if 'career' not in st.session_state:
    st.session_state.career = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'guidance' not in st.session_state:
    st.session_state.guidance = None

# Career options
CAREERS = [
    'Java Developer', 'MERN Stack Developer', 'Full Stack Web Developer',
    'Data Scientist', 'Machine Learning Engineer', 'Deep Learning Specialist',
    'Data Analyst', 'Cybersecurity Specialist', 'DevOps Engineer',
    'Cloud Engineer', 'Mobile App Developer', 'UI/UX Developer'
]

# Questions
COMMON_QUESTIONS = [
    {
        'q': "What's your current programming experience level?",
        'options': ["Beginner (0-1 year)", "Intermediate (1-3 years)", "Advanced (3+ years)", "Expert (5+ years)"]
    },
    {
        'q': "How much time can you dedicate weekly to learning?",
        'options': ["5-10 hours", "10-20 hours", "20-30 hours", "30+ hours"]
    },
    {
        'q': "What's your preferred learning style?",
        'options': ["Video tutorials", "Hands-on projects", "Reading documentation", "Interactive courses"]
    },
    {
        'q': "What's your target timeline to job-ready?",
        'options': ["3 months", "6 months", "1 year", "2+ years"]
    }
]

SPECIFIC_QUESTIONS = {
    'Java Developer': [
        {'q': "Experience with Java?", 'options': ["None", "Basic syntax", "OOP concepts", "Spring framework"]},
        {'q': "Database knowledge?", 'options': ["None", "SQL basics", "Advanced SQL", "NoSQL too"]}
    ],
    'MERN Stack Developer': [
        {'q': "JavaScript proficiency?", 'options': ["Beginner", "ES6 comfortable", "Advanced patterns", "Expert"]},
        {'q': "React experience?", 'options': ["None", "Basic components", "Hooks & state", "Advanced patterns"]}
    ],
    'Data Scientist': [
        {'q': "Python/R knowledge?", 'options': ["None", "Basic", "Libraries (Pandas/NumPy)", "Advanced"]},
        {'q': "Statistics background?", 'options': ["None", "Basic", "Intermediate", "Strong"]}
    ],
    'Machine Learning Engineer': [
        {'q': "ML algorithms understanding?", 'options': ["None", "Basics", "Implemented some", "Deep knowledge"]},
        {'q': "Framework experience?", 'options': ["None", "Scikit-learn", "TensorFlow/PyTorch", "All"]}
    ],
    'Cybersecurity Specialist': [
        {'q': "Network fundamentals?", 'options': ["None", "Basic", "Intermediate", "Advanced"]},
        {'q': "Security tools knowledge?", 'options': ["None", "Basic tools", "Pen-testing", "Advanced"]}
    ],
    'Full Stack Web Developer': [
        {'q': "Frontend experience?", 'options': ["None", "HTML/CSS", "JavaScript frameworks", "Expert"]},
        {'q': "Backend knowledge?", 'options': ["None", "Basic", "APIs & databases", "Microservices"]}
    ],
    'Data Analyst': [
        {'q': "Excel/SQL proficiency?", 'options': ["None", "Basic", "Intermediate", "Advanced"]},
        {'q': "Data visualization tools?", 'options': ["None", "Basic charts", "Tableau/PowerBI", "Expert"]}
    ]
}

def get_questions():
    career = st.session_state.career
    questions = COMMON_QUESTIONS.copy()
    if career in SPECIFIC_QUESTIONS:
        questions.extend(SPECIFIC_QUESTIONS[career])
    return questions

def generate_guidance():
    """Generate AI-powered career guidance using Google Gemini"""
    questions = get_questions()
    answers = st.session_state.answers
    career = st.session_state.career
    
    # Build prompt
    responses = '\n'.join([f"{questions[i]['q']}: {answers.get(i, 'N/A')}" for i in range(len(questions))])
    
    prompt = f"""You are a career guidance counselor. Analyze this student's profile and provide structured guidance.

Career Choice: {career}
Responses:
{responses}

Provide a comprehensive guidance plan in JSON format:
{{
  "competencyLevel": "Beginner/Intermediate/Advanced",
  "assessmentSummary": "Brief 2-3 sentence analysis",
  "learningRoadmap": [
    {{"phase": "Foundation", "duration": "X months", "topics": ["topic1", "topic2"], "goal": "what to achieve"}},
    {{"phase": "Intermediate", "duration": "X months", "topics": ["topic1", "topic2"], "goal": "what to achieve"}},
    {{"phase": "Advanced", "duration": "X months", "topics": ["topic1", "topic2"], "goal": "what to achieve"}}
  ],
  "recommendedCourses": [
    {{"name": "Course name", "platform": "Platform", "type": "Free/Paid"}}
  ],
  "projectIdeas": ["project1", "project2", "project3"],
  "certifications": ["cert1", "cert2"],
  "keySkills": ["skill1", "skill2", "skill3"],
  "resources": ["resource1", "resource2"]
}}

Respond ONLY with valid JSON, no additional text or markdown formatting."""
    
    try:
        # Configure Gemini API
        api_key = st.secrets.get("GEMINI_API_KEY", "")
        if not api_key:
            st.error("⚠️ Please add your GEMINI_API_KEY to Streamlit secrets!")
            return
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        with st.spinner('🤖 Model is analyzing your profile and generating personalized guidance...'):
            response = model.generate_content(prompt)
            
            # Extract and clean JSON
            content = response.text.strip()
            # Remove markdown code blocks if present
            content = content.replace('```json', '').replace('```', '').strip()
            
            guidance = json.loads(content)
            st.session_state.guidance = guidance
            st.session_state.step = 'results'
            st.rerun()
            
    except json.JSONDecodeError as e:
        st.error(f"⚠️ Error parsing AI response: {str(e)}")
        st.info("The AI response was not in valid JSON format. Please try again.")
    except Exception as e:
        st.error(f"⚠️ Error generating guidance: {str(e)}")
        st.info("💡 Make sure to add your Google Gemini API key in Streamlit secrets.")

def reset():
    """Reset the application"""
    st.session_state.step = 'career'
    st.session_state.career = None
    st.session_state.answers = {}
    st.session_state.current_q = 0
    st.session_state.guidance = None
    st.rerun()

# Header
st.title("💼 IT Career Guidance System")
st.markdown("### AI-powered personalized career roadmap for university students")
st.divider()

# Career Selection
if st.session_state.step == 'career':
    st.subheader("🎯 Select Your Career Path")
    st.markdown("Choose the IT career you're interested in pursuing:")
    
    cols = st.columns(3)
    for idx, career in enumerate(CAREERS):
        with cols[idx % 3]:
            if st.button(career, key=f"career_{idx}", use_container_width=True):
                st.session_state.career = career
                st.session_state.step = 'assessment'
                st.rerun()

# Assessment
elif st.session_state.step == 'assessment':
    questions = get_questions()
    current_idx = st.session_state.current_q
    
    # Progress bar
    progress = (current_idx + 1) / len(questions)
    st.progress(progress)
    st.caption(f"Question {current_idx + 1} of {len(questions)} ({int(progress * 100)}%)")
    
    st.divider()
    
    # Display current question
    st.subheader(f"📋 {questions[current_idx]['q']}")
    
    # Answer options
    for option in questions[current_idx]['options']:
        if st.button(option, key=f"opt_{current_idx}_{option}", use_container_width=True):
            st.session_state.answers[current_idx] = option
            
            if current_idx < len(questions) - 1:
                st.session_state.current_q += 1
                st.rerun()
            else:
                generate_guidance()

# Results
elif st.session_state.step == 'results':
    guidance = st.session_state.guidance
    
    if guidance:
        # Action buttons
        col1, col2 = st.columns([6, 1])
        with col1:
            st.subheader("✨ Your Personalized Career Guidance")
        with col2:
            if st.button("🔄 Start Over"):
                reset()
        
        st.divider()
        
        # Career and competency level
        st.info(f"**Career:** {st.session_state.career}  \n**Competency Level:** {guidance['competencyLevel']}")
        
        # Assessment Summary
        st.markdown("### 📊 Assessment Summary")
        st.write(guidance['assessmentSummary'])
        
        # Learning Roadmap
        st.markdown("### 🗺️ Learning Roadmap")
        for phase in guidance['learningRoadmap']:
            with st.expander(f"**{phase['phase']}** ({phase['duration']})", expanded=True):
                st.markdown(f"**Goal:** {phase['goal']}")
                st.markdown("**Topics to Learn:**")
                for topic in phase['topics']:
                    st.markdown(f"- {topic}")
        
        # Two columns for courses and projects
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📚 Recommended Courses")
            for course in guidance['recommendedCourses']:
                st.markdown(f"**{course['name']}**")
                st.caption(f"{course['platform']} • {course['type']}")
        
        with col2:
            st.markdown("### 💡 Project Ideas")
            for idx, project in enumerate(guidance['projectIdeas'], 1):
                st.markdown(f"{idx}. {project}")
        
        # Key Skills and Certifications
        st.markdown("### 🎯 Key Skills to Develop")
        st.write(", ".join(guidance['keySkills']))
        
        st.markdown("### 🏆 Recommended Certifications")
        for cert in guidance['certifications']:
            st.markdown(f"- {cert}")
        
        # Download button
        st.divider()
        report = f"""
IT CAREER GUIDANCE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

CAREER PATH: {st.session_state.career}
COMPETENCY LEVEL: {guidance['competencyLevel']}

ASSESSMENT SUMMARY:
{guidance['assessmentSummary']}

LEARNING ROADMAP:
{''.join([f"\n{i+1}. {p['phase']} ({p['duration']})\n   Goal: {p['goal']}\n   Topics: {', '.join(p['topics'])}\n" for i, p in enumerate(guidance['learningRoadmap'])])}

RECOMMENDED COURSES:
{''.join([f"{i+1}. {c['name']} ({c['platform']}) - {c['type']}\n" for i, c in enumerate(guidance['recommendedCourses'])])}

PROJECT IDEAS:
{''.join([f"{i+1}. {p}\n" for i, p in enumerate(guidance['projectIdeas'])])}

KEY SKILLS: {', '.join(guidance['keySkills'])}

CERTIFICATIONS:
{''.join([f"- {c}\n" for c in guidance['certifications']])}
        """
        
        st.download_button(
            label="📥 Download Guidance Report",
            data=report,
            file_name=f"{st.session_state.career.replace(' ', '_')}_Guidance.txt",
            mime="text/plain",
            use_container_width=True
        )

# Footer
st.divider()
st.caption("Made by Team RAJINDER")