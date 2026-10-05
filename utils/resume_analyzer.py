import re


# -----------------------------
# Extract Email
# -----------------------------
def extract_email(text):
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return "Not found"


# -----------------------------
# Extract Phone Number
# -----------------------------
def extract_phone(text):
    pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return "Not found"


# -----------------------------
# Extract Name
# -----------------------------
def extract_name(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if lines:
        first_line = lines[0]

        # Avoid treating email/phone as name
        if "@" not in first_line and not re.search(r"\d{5,}", first_line):
            return first_line

    return "Not found"


# -----------------------------
# Extract Skills
# -----------------------------
def extract_skills(text):
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

    text_lower = text.lower()

    for skill in skills_list:

        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills


# -----------------------------
# Extract Education
# -----------------------------
def extract_education(text):
    education_keywords = [
        "B.Tech",
        "B.E",
        "Bachelor",
        "M.Tech",
        "M.E",
        "Master",
        "B.Sc",
        "M.Sc",
        "BCA",
        "MCA",
        "Intermediate",
        "12th",
        "10th",
        "SSC"
    ]

    found_education = []

    for keyword in education_keywords:

        if keyword.lower() in text.lower():
            found_education.append(keyword)

    return found_education


# -----------------------------
# Extract Sections
# -----------------------------
def extract_section(text, section_names):

    lines = text.splitlines()

    collected = []

    collecting = False

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        if any(section.lower() in lower_line for section in section_names):
            collecting = True
            continue

        if collecting:

            # Stop when another common section starts
            stop_words = [
                "skills",
                "education",
                "experience",
                "projects",
                "certifications",
                "achievements",
                "languages",
                "interests"
            ]

            if any(word in lower_line for word in stop_words):
                break

            collected.append(clean_line)

    return collected


# -----------------------------
# Analyze Resume
# -----------------------------
def analyze_resume(text):

    result = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_section(
            text,
            ["experience", "work experience", "internship"]
        ),
        "projects": extract_section(
            text,
            ["projects", "academic projects"]
        )
    }

    return result