def calculate_ats_score(
    resume_text,
    resume_skills,
    job_skills,
    matching_skills,
    missing_skills
):

    score = 0

    # -----------------------------------------
    # 1. Resume Content Score
    # -----------------------------------------

    if len(resume_text) >= 500:
        score += 20

    elif len(resume_text) >= 250:
        score += 15

    elif len(resume_text) >= 100:
        score += 10


    # -----------------------------------------
    # 2. Skills Score
    # -----------------------------------------

    if len(resume_skills) >= 8:
        score += 20

    elif len(resume_skills) >= 5:
        score += 15

    elif len(resume_skills) >= 3:
        score += 10

    elif len(resume_skills) > 0:
        score += 5


    # -----------------------------------------
    # 3. Job Match Score
    # -----------------------------------------

    if job_skills:

        match_score = (
            len(matching_skills)
            / len(job_skills)
        ) * 40

        score += match_score

    else:

        score += 20


    # -----------------------------------------
    # 4. Missing Skills Penalty
    # -----------------------------------------

    if len(missing_skills) >= 5:
        score -= 10

    elif len(missing_skills) >= 3:
        score -= 5


    # -----------------------------------------
    # Keep Score Between 0 and 100
    # -----------------------------------------

    score = max(0, min(100, round(score)))

    return score


def get_score_message(score):

    if score >= 85:
        return "Excellent resume! 🚀"

    elif score >= 70:
        return "Good resume. A few improvements can make it stronger. 👍"

    elif score >= 50:
        return "Average resume. Several improvements are recommended. ⚠️"

    else:
        return "Your resume needs improvement. Focus on skills and job relevance. ❗"


def get_improvement_suggestions(
    resume_text,
    resume_skills,
    missing_skills
):

    suggestions = []


    # -----------------------------------------
    # Skills Suggestions
    # -----------------------------------------

    if missing_skills:

        suggestions.append(
            "Consider adding relevant missing skills: "
            + ", ".join(missing_skills)
        )


    # -----------------------------------------
    # Resume Length
    # -----------------------------------------

    if len(resume_text) < 500:

        suggestions.append(
            "Add more relevant details about your projects, "
            "experience, certifications, and achievements."
        )


    # -----------------------------------------
    # Skills Count
    # -----------------------------------------

    if len(resume_skills) < 5:

        suggestions.append(
            "Add more relevant technical skills that you actually know."
        )


    # -----------------------------------------
    # General Suggestions
    # -----------------------------------------

    suggestions.append(
        "Use clear section headings such as Skills, Education, "
        "Projects, Experience, and Certifications."
    )

    suggestions.append(
        "Use measurable achievements in project or experience descriptions "
        "whenever possible."
    )

    suggestions.append(
        "Keep the resume clean, readable, and relevant to the target job."
    )


    return suggestions