import streamlit as st
from resume_parser import extract_text_from_pdf
from preprocessing import clean_text
from skill_extractor import load_skills, extract_skills
from recommendation import generate_recommendations
from resume_score import calculate_resume_score
from resume_statistics import resume_statistics
from resume_sections import detect_sections
from skill_category import categorize_skills
from report_generator import generate_report
from job_recommender import recommend_jobs
from resume_strength import resume_strength 
from llm_chat import ask_resume_ai

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------
st.sidebar.title("🤖 AI Resume Analyzer")

st.sidebar.markdown("""
### Features
- 📄 Resume Upload
- 🧹 Resume Cleaning
- 💻 Skill Extraction
- 📊 ATS Score
- ⭐ Resume Score
- 💡 AI Recommendations
""")

# ----------------------------------------------------
# Load Skills
# ----------------------------------------------------
skills = load_skills()

# ----------------------------------------------------
# Main Title
# ----------------------------------------------------
st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and compare it with a Job Description.")

# ----------------------------------------------------
# Upload Resume
# ----------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# ----------------------------------------------------
# Process Resume
# ----------------------------------------------------
if uploaded_file is not None:

    # Save uploaded file
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Resume uploaded successfully!")

    # ------------------------------------------------
    # Extract Resume Text
    # ------------------------------------------------
    resume_text = extract_text_from_pdf(uploaded_file.name)

    st.subheader("📄 Extracted Resume")
    st.text_area(
        "Resume Text",
        resume_text,
        height=250
    )
    # ------------------------------------------------
    # Resume Statistics
    # ------------------------------------------------
    words, characters, lines = resume_statistics(resume_text)

    st.subheader("📈 Resume Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Words", words)

    with col2:
        st.metric("Characters", characters)

    with col3:
        st.metric("Lines", lines)

    # ------------------------------------------------
    # Clean Resume
    # ------------------------------------------------
    cleaned_text = clean_text(resume_text)

    st.subheader("🧹 Cleaned Resume")

    st.text_area(
        "Cleaned Resume",
        cleaned_text,
        height=250
    )

    # ------------------------------------------------
    # Resume Sections
    # ------------------------------------------------
    sections = detect_sections(cleaned_text)

    st.subheader("📑 Resume Sections")

    for section, present in sections.items():
        if present:
            st.success(f"✅ {section}")
        else:
            st.error(f"❌ {section}")

    # ------------------------------------------------
    # Extract Skills
    # ------------------------------------------------
    found_skills = extract_skills(cleaned_text, skills)

    st.subheader("💻 Detected Skills")

    if found_skills:
        for skill in found_skills:
            st.success(skill)
    else:
        st.warning("No skills detected.")

    # ------------------------------------------------
    # Skill Categories
    # ------------------------------------------------
    categorized = categorize_skills(found_skills)

    st.subheader("📂 Skill Categories")

    for category, skill_list in categorized.items():

        if skill_list:

            st.markdown(f"### {category}")

            for skill in skill_list:
                st.success(skill)
    # ------------------------------------------------
    # Job Description
    # ------------------------------------------------
    st.subheader("📋 Job Description")

    job_description = st.text_area(
        "Paste Job Description",
        height=200
    )

    if job_description.strip():

        cleaned_jd = clean_text(job_description)

        job_skills = extract_skills(cleaned_jd, skills)

        st.subheader("🎯 Required Skills")

        if job_skills:
            for skill in job_skills:
                st.info(skill)
        else:
            st.warning("No skills found.")

               # ------------------------------------------------
        # ATS Score
        # ------------------------------------------------
        matched_skills = set(found_skills).intersection(set(job_skills))
        missing_skills = set(job_skills) - set(found_skills)

        if len(job_skills) > 0:
            ats_score = (
                len(matched_skills) / len(job_skills)
            ) * 100
        else:
            ats_score = 0

        # ------------------------------------------------
        # Skill Gap Analysis
        # ------------------------------------------------
        gap = len(missing_skills)

        st.subheader("📉 Skill Gap Analysis")

        st.metric(
            "Missing Skills Count",
            gap
        )

        # ------------------------------------------------
        # Resume Score
        # ------------------------------------------------
        resume_score = calculate_resume_score(
            ats_score,
            found_skills,
            missing_skills,
            cleaned_text
        )
        # ------------------------------------------------
        # Dashboard
        # ------------------------------------------------
        st.subheader("📊 Analysis Dashboard")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("📊 ATS Score", f"{ats_score:.2f}%")

        with c2:
            st.metric("⭐ Resume Score", f"{resume_score}/100")

        with c3:
            st.metric("💻 Skills Found", len(found_skills))

        st.progress(min(resume_score / 100, 1.0))

        # ------------------------------------------------
        # Matched Skills
        # ------------------------------------------------
        st.subheader("✅ Matched Skills")

        if matched_skills:
            for skill in sorted(matched_skills):
                st.success(skill)
        else:
            st.warning("No matched skills.")

        # ------------------------------------------------
        # Missing Skills
        # ------------------------------------------------
        st.subheader("❌ Missing Skills")

        if missing_skills:
            for skill in sorted(missing_skills):
                st.error(skill)
        else:
            st.success("Excellent! No missing skills.")

        # ------------------------------------------------
        # Recommendations
               # ------------------------------------------------
                # ------------------------------------------------
        # AI Resume Suggestions
        # ------------------------------------------------
        st.subheader("💡 AI Resume Suggestions")

        recommendations = generate_recommendations(missing_skills)

        for recommendation in recommendations:
            st.info(recommendation)

        # ------------------------------------------------
        # Recommended Job Roles
        # ------------------------------------------------
        st.subheader("💼 Recommended Job Roles")

        jobs = recommend_jobs(found_skills)

        if jobs:
            for job in jobs:
                st.success(job)
        else:
            st.warning("No suitable job recommendations found.")

        # ------------------------------------------------
        # Resume Strength
        # ------------------------------------------------
        strength = resume_strength(resume_score)

        st.subheader("💪 Resume Strength")
        st.success(strength)

        # ------------------------------------------------
        # Generate PDF Report
        # ------------------------------------------------
        generate_report(
            "Resume_Report.pdf",
            ats_score,
            resume_score,
            matched_skills,
            missing_skills,
            recommendations
        )

        # ------------------------------------------------
        # Download PDF Report
        # ------------------------------------------------
        with open("Resume_Report.pdf", "rb") as pdf_file:
            st.download_button(
                label="📥 Download Report",
                data=pdf_file,
                file_name="Resume_Report.pdf",
                mime="application/pdf"
            )
                    # ------------------------------------------------
                # ------------------------------------------------
        # AI Resume Chatbot
        # ------------------------------------------------
        st.divider()

        st.subheader("🤖 Chat with Your Resume")

        st.write(
            "Ask questions about your resume and the job description."
        )

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Clear Chat Button
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

        # Display previous messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User Question
        user_question = st.chat_input(
            "Ask a question about your resume..."
        )

        if user_question:

            # Save user question
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": user_question
                }
            )

            # Display user question
            with st.chat_message("user"):
                st.markdown(user_question)

            # Generate Gemini Answer
            with st.chat_message("assistant"):

                with st.spinner("Analyzing your resume..."):

                    try:
                        answer = ask_resume_ai(
                            resume_text,
                            job_description,
                            user_question
                        )

                        st.markdown(answer)

                        # Save successful Gemini response
                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": answer
                            }
                        )

                    except Exception as error:
                        st.error(
                            f"Unable to generate AI response: {error}"
                        )