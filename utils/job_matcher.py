import re


def extract_job_skills(job_description):

    skills_list = [
        "Python",
        "Java",
        "C",
        "C++",
        "SQL",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Machine Learning",
        "Deep Learning",
        "Data Science",
        "Data Analytics",
        "Artificial Intelligence",
        "Excel",
        "Power BI",
        "Tableau",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "NLP",
        "Git",
        "GitHub",
        "Streamlit"
    ]

    found_skills = []

    text = job_description.lower()

    for skill in skills_list:

        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


def calculate_match(resume_skills, job_skills):

    resume_set = {
        skill.lower()
        for skill in resume_skills
    }

    job_set = {
        skill.lower()
        for skill in job_skills
    }

    if not job_set:
        return 0, [], []

    matching_skills = resume_set.intersection(job_set)

    missing_skills = job_set - resume_set

    match_percentage = (
        len(matching_skills) / len(job_set)
    ) * 100

    matching_skills = [
        skill for skill in job_skills
        if skill.lower() in matching_skills
    ]

    missing_skills = [
        skill for skill in job_skills
        if skill.lower() in missing_skills
    ]

    return (
        round(match_percentage, 2),
        matching_skills,
        missing_skills
    )