import streamlit as st
import os
import mysql.connector
from pyresparser import ResumeParser
from PIL import Image
from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos

# ------------------ Page Config ------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.sidebar.image("logo/logo.png", use_container_width=True)
st.sidebar.title("AI Resume Analyzer")
st.sidebar.write("Upload your resume to get personalized insights!")

# ------------------ Database Insert Function ------------------


import mysql.connector
import streamlit as st

def insert_into_db(data, filename):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ommni@123",
            database="resume_analyzer_db"
        )
        cursor = conn.cursor()

        sql = """
        INSERT INTO resume_data (name, email, phone, degree, experience, skills, filename)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        # Ensure all list fields are converted to strings
        def safe_string(value):
            if isinstance(value, list):
                return ', '.join(map(str, value))
            return str(value) if value is not None else ''

        values = (
            safe_string(data.get('name')),
            safe_string(data.get('email')),
            safe_string(data.get('mobile_number')),
            safe_string(data.get('degree')),
            safe_string(data.get('total_experience')),
            safe_string(data.get('skills')),
            filename
        )

        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        st.error(f"❌ Database error: {str(e)}")

# ------------------ Scoring Function ------------------
def calculate_resume_score(data):
    score = 0

    # Basic fields (10 points each)
    if data.get("name"): score += 10
    if data.get("email"): score += 10
    if data.get("mobile_number"): score += 10

    # Degree (optional - 10 points)
    if data.get("degree"): score += 10

    # Experience (up to 20 points)
    experience = data.get("total_experience", 0)
    if experience:
        try:
            exp = float(experience)
            if exp >= 5:
                score += 20
            elif exp >= 2:
                score += 10
            else:
                score += 5
        except:
            score += 5

    # Skills (up to 40 points)
    skills = data.get("skills", [])
    if skills:
        score += min(len(skills) * 4, 40)  # max 10 skills * 4 = 40

    return min(score, 100)

# ------------------ Resume Upload ------------------
st.header("📄 Upload Your Resume")
uploaded_file = st.file_uploader("Choose your resume (PDF/DOCX)", type=["pdf", "docx"])

# ------------------ Video Sections ------------------
with st.expander("🎥 Resume Building Videos"):
    for link in resume_videos:
        st.video(link)

with st.expander("🎤 Interview Preparation Videos"):
    for link in interview_videos:
        st.video(link)

# ------------------ Resume Analysis ------------------
if uploaded_file is not None:
    if st.button("Analyze Resume"):
        with st.spinner("Analyzing your resume..."):
            save_path = os.path.join("Uploaded_Resumes", uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            try:
                data = ResumeParser(save_path).get_extracted_data()

                if data:
                    insert_into_db(data, uploaded_file.name)
                    st.success("✅ Resume Analyzed Successfully!")

                    # 🎯 Resume Score
                    score = calculate_resume_score(data)
                    st.subheader("📈 Resume Score")
                    st.metric(label="Score", value=f"{score}/100")

                    if score >= 80:
                        st.success("🟢 Excellent Resume!")
                    elif score >= 50:
                        st.info("🟡 Decent Resume. Can be improved.")
                    else:
                        st.warning("🔴 Weak Resume. Needs significant improvement.")

                    # 👤 Candidate Info
                    st.subheader("👤 Candidate Information")
                    st.write(f"*Name:* {data.get('name', 'N/A')}")
                    st.write(f"*Email:* {data.get('email', 'N/A')}")
                    st.write(f"*Phone:* {data.get('mobile_number', 'N/A')}")
                    st.write(f"*Degree:* {data.get('degree', 'N/A')}")
                    st.write(f"*Experience:* {data.get('total_experience', 'N/A')} years")
                    st.write(f"*Skills:* {', '.join(data.get('skills', []))}")

                    # 🎯 Course Recommendations
                    st.subheader("🎯 Recommended Courses")
                    skills = [skill.lower() for skill in data.get("skills", [])]

                    def display_courses(title, courses):
                        st.markdown(f"{title}")
                        for name, link in courses:
                            st.markdown(f"- [{name}]({link})")

                    if any(skill in skills for skill in ['ml', 'machine learning', 'data science', 'python']):
                        display_courses("📊 Data Science / ML Courses", ds_course)
                    if any(skill in skills for skill in ['html', 'css', 'javascript', 'django', 'react']):
                        display_courses("🌐 Web Development Courses", web_course)
                    if any(skill in skills for skill in ['android', 'kotlin', 'flutter']):
                        display_courses("📱 Android Development Courses", android_course)
                    if any(skill in skills for skill in ['ios', 'swift', 'objective-c']):
                        display_courses("🍏 iOS Development Courses", ios_course)
                    if any(skill in skills for skill in ['ui', 'ux', 'design']):
                        display_courses("🎨 UI/UX Courses", uiux_course)
                else:
                    st.error("⚠ Failed to extract data. Try another file.")
            except Exception as e:
                st.error(f"🚨 Error: {str(e)}")# app.py - AI Resume Analyzer

# Your Streamlit app code goes here...