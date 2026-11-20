import streamlit as st
from resume_parser import extract_text_from_pdf
from preprocessing import clean_text
from skill_extractor import load_skills, extract_skills
from recommendation import generate_recommendations
from resume_score import calculate_resume_score
from resume_statistics import resume_statistics

from skill_category import categorize_skills
from report_generator import generate_report
from job_recommender import recommend_jobs
from resume_strength import resume_strength
from llm_chat import ask_resume_ai
from chatbot import chat_with_resume
from interview_coach import generate_interview_questions
from services.resume_service import analyze_resume
from interview_evaluator import evaluate_answer
import re
from resume_rewriter import rewrite_resume_bullet
from resume_bullets import extract_resume_bullets
from resume_sections import extract_resume_sections


# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)
if "interview_scores" not in st.session_state:
    st.session_state.interview_scores = {}

if "interview_feedbacks" not in st.session_state:
    st.session_state.interview_feedbacks = {}

if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "interview_answers" not in st.session_state:
    st.session_state.interview_answers = {}

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
    # Analyze Resume
    # ------------------------------------------------
    analysis = analyze_resume(
        uploaded_file.name,
        skills
    )

    resume_text = analysis["resume_text"]
    cleaned_text = analysis["cleaned_text"]

    words = analysis["words"]
    characters = analysis["characters"]
    lines = analysis["lines"]

    sections = analysis["sections"]

    found_skills = analysis["found_skills"]

    categorized = analysis["categorized"]

    # ------------------------------------------------
    # Display Extracted Resume
    # ------------------------------------------------
    st.subheader("📄 Extracted Resume")

    st.text_area(
        "Resume Text",
        resume_text,
        height=250
    )

    # ------------------------------------------------
    # Resume Statistics
    # ------------------------------------------------
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
    st.subheader("🧹 Cleaned Resume")

    st.text_area(
        "Cleaned Resume",
        cleaned_text,
        height=250
    )

    # ------------------------------------------------
    # Resume Sections
    # ------------------------------------------------
    st.subheader("📑 Resume Sections")

    for section, present in sections.items():
        if present:
            st.success(f"✅ {section}")
        else:
            st.error(f"❌ {section}")

    # ------------------------------------------------
    # Detected Skills
    # ------------------------------------------------
    st.subheader("💻 Detected Skills")

    if found_skills:
        for skill in found_skills:
            st.success(skill)
    else:
        st.warning("No skills detected.")

    # ------------------------------------------------
    # Skill Categories
    # ------------------------------------------------
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

            # Generate AI Answer
            with st.chat_message("assistant"):

                with st.spinner("Analyzing your resume..."):

                    try:
                        answer, sources = chat_with_resume(
                            resume_text=cleaned_text,
                            job_description=cleaned_jd,
                            user_question=user_question
                        )

                        # Display answer
                        st.markdown(answer)

                        # Display sources
                        st.divider()
                        st.subheader("📚 Sources Used")

                        for source in sources:
                            st.caption(source)

                        # Save assistant response
                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": answer
                            }
                        )

                    except Exception as e:
                        st.error(f"Error: {e}")

        # ------------------------------------------------
        # AI Interview Coach
        # ------------------------------------------------
        st.divider()
        st.header("🎤 AI Interview Coach")

        st.subheader("⚙️ Interview Settings")

        interview_mode = st.selectbox(
            "Choose Interview Mode",
            [
                "Quick Interview",
                "Standard Interview",
                "Comprehensive Interview",
                "Company Simulation"
            ]
        )

        if interview_mode == "Quick Interview":
            num_questions = 5
        elif interview_mode == "Standard Interview":
            num_questions = 10
        elif interview_mode == "Comprehensive Interview":
            num_questions = 20
        else:
            num_questions = 30

        # -----------------------------
        # Generate Questions
        # -----------------------------
        if st.button("🎯 Generate Interview Questions"):

            with st.spinner("Generating Interview Questions..."):

                questions = generate_interview_questions(
                    cleaned_text,
                    cleaned_jd,
                    num_questions,
                    interview_mode
                )

                # Handle errors
                if questions.startswith("⚠️") or questions.startswith("❌"):
                    st.error(questions)

                else:

                    question_list = []

                    for line in questions.split("\n"):

                        line = line.strip()

                        if not line:
                            continue

                        if re.match(
                            r"^(Q?\d+[\.\)]|Question\s+\d+:)",
                            line,
                            re.IGNORECASE
                        ):
                            question_list.append(line)

                    # Fallback
                    if not question_list:
                        question_list = [
                            l.strip()
                            for l in questions.split("\n")
                            if l.strip()
                        ]

                    st.session_state.interview_questions = question_list
                    st.session_state.current_question = 0
                    st.session_state.interview_answers = {}
                    st.session_state.interview_feedbacks = {}
                    st.session_state.interview_scores = {}

        # -----------------------------
        # Display Current Question
        # -----------------------------
        if st.session_state.interview_questions:

            questions = st.session_state.interview_questions
            current = st.session_state.current_question

            # Progress Bar
            st.progress((current + 1) / len(questions))

            st.subheader(
                f"Question {current + 1} of {len(questions)}"
            )

            st.info(questions[current])

            # Restore previous answer if available
            answer = st.text_area(
                "✍️ Your Answer",
                value=st.session_state.interview_answers.get(current, ""),
                key=f"answer_box_{current}",
                height=180
            )

            # -----------------------------
            # Evaluate Current Answer
            # -----------------------------
            if st.button("✅ Evaluate Answer"):

                if answer.strip():

                    with st.spinner("Evaluating your answer..."):

                        # Save answer
                        st.session_state.interview_answers[current] = answer

                        # AI Evaluation
                        feedback = evaluate_answer(
                            cleaned_text,
                            cleaned_jd,
                            questions[current],
                            answer
                        )

                        # Save feedback
                        st.session_state.interview_feedbacks[current] = feedback

                        # Extract score
                        match = re.search(
                            r"Overall Score:\s*(\d+(?:\.\d+)?)\s*/\s*10",
                            feedback,
                            re.IGNORECASE
                        )

                        if match:
                            score = float(match.group(1))
                        else:
                            score = 0

                        st.session_state.interview_scores[current] = score

                else:
                    st.warning("Please enter your answer.")

            # -----------------------------
            # Show Previous Feedback
            # -----------------------------
            if current in st.session_state.interview_feedbacks:

                st.subheader("📊 AI Feedback")

                st.markdown(
                    st.session_state.interview_feedbacks[current]
                )

            # -----------------------------
            # Show Question Score
            # -----------------------------
            if current in st.session_state.interview_scores:

                st.metric(
                    "⭐ Question Score",
                    f"{st.session_state.interview_scores[current]}/10"
                )

            # -----------------------------
            # Navigation Buttons
            # -----------------------------
            col1, col2 = st.columns(2)

            with col1:

                if current > 0:

                    if st.button("⬅ Previous"):

                        st.session_state.interview_answers[current] = answer
                        st.session_state.current_question -= 1
                        st.rerun()

            with col2:

                if current < len(questions) - 1:

                    if st.button("Next ➡"):

                        st.session_state.interview_answers[current] = answer
                        st.session_state.current_question += 1
                        st.rerun()

                else:

                    st.success("🎉 Interview Completed!")

                    st.balloons()