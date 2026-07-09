def generate_recommendations(missing_skills):

    recommendations = []

    if not missing_skills:
        recommendations.append(
            "Excellent! Your resume matches the job requirements."
        )
    else:
        recommendations.append(
            "Consider adding these skills to improve your ATS score:"
        )

        for skill in sorted(missing_skills):
            recommendations.append(f"• {skill}")

    return recommendations