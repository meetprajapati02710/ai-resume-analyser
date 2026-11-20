from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(
    filename,
    ats_score,
    resume_score,
    matched_skills,
    missing_skills,
    recommendations
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Resume Analysis Report</b>", styles["Title"]))

    story.append(Paragraph(f"ATS Score : {ats_score:.2f}%", styles["Normal"]))
    story.append(Paragraph(f"Resume Score : {resume_score}/100", styles["Normal"]))

    story.append(Paragraph("<br/><b>Matched Skills</b>", styles["Heading2"]))

    for skill in matched_skills:
        story.append(Paragraph(skill, styles["Normal"]))

    story.append(Paragraph("<br/><b>Missing Skills</b>", styles["Heading2"]))

    for skill in missing_skills:
        story.append(Paragraph(skill, styles["Normal"]))

    story.append(Paragraph("<br/><b>Recommendations</b>", styles["Heading2"]))

    for recommendation in recommendations:
        story.append(Paragraph(recommendation, styles["Normal"]))

    doc.build(story)