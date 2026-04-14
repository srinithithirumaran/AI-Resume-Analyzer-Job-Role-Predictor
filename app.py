from flask import Flask, render_template, request

app = Flask(__name__)

# Keyword dictionary for simple NLP-like extraction.
# Keys are canonical skills, values are keyword variants checked in text.
SKILL_KEYWORDS = {
    "python": ["python"],
    "machine learning": ["machine learning", "ml"],
    "sql": ["sql", "mysql", "postgresql", "sqlite"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "javascript": ["javascript", "js"],
    "flask": ["flask"],
    "django": ["django"],
    "data analysis": ["data analysis", "data analytics", "analytics"],
    "excel": ["excel", "spreadsheets"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "tensorflow": ["tensorflow"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "deep learning": ["deep learning"],
    "nlp": ["nlp", "natural language processing"],
    "git": ["git", "github"],
}

SKILLS = list(SKILL_KEYWORDS.keys())

# Role profile uses core and bonus skills for weighted scoring.
ROLE_PROFILES = {
    "Data Scientist": {
        "core": {
            "python",
            "machine learning",
            "sql",
            "data analysis",
            "pandas",
            "numpy",
        },
        "bonus": {
            "tensorflow",
            "scikit-learn",
            "deep learning",
            "nlp",
            "tableau",
        },
    },
    "Web Developer": {
        "core": {
            "html",
            "css",
            "javascript",
            "python",
            "flask",
        },
        "bonus": {
            "django",
            "git",
            "sql",
        },
    },
    "Data Analyst": {
        "core": {
            "sql",
            "excel",
            "power bi",
            "tableau",
            "data analysis",
        },
        "bonus": {
            "python",
            "pandas",
            "numpy",
        },
    },
}

# Suggestions for improving resume by missing skills
IMPROVEMENT_TIPS = {
    "python": "Add at least one Python project with measurable impact.",
    "machine learning": "Mention ML models you built and the metrics achieved.",
    "sql": "Include SQL tasks such as joins, aggregations, or query optimization.",
    "html": "Highlight front-end work that used HTML in real applications.",
    "css": "Include responsive design or UI work where you used CSS.",
    "javascript": "Mention JS frameworks or interactive features you implemented.",
    "flask": "Add a backend API or web app project built using Flask.",
    "django": "Add any full-stack project where Django was used.",
    "data analysis": "Describe analysis work and outcomes using real numbers.",
    "excel": "Mention advanced Excel usage like pivot tables or dashboards.",
    "power bi": "Add BI dashboard examples with insights generated.",
    "tableau": "Include Tableau dashboards and business impact.",
    "pandas": "Show data cleaning or transformation tasks done with Pandas.",
    "numpy": "Mention numerical computing work using NumPy.",
    "tensorflow": "Add TensorFlow model implementations and outcomes.",
    "scikit-learn": "Mention scikit-learn pipelines, model selection, and evaluation.",
    "deep learning": "Add deep learning use cases and frameworks used.",
    "nlp": "Mention NLP tasks such as text classification or extraction.",
    "git": "Include collaboration workflows using Git and version control.",
}


def extract_skills(resume_text: str):
    """Extract skills from resume text using keyword variants and canonical mapping."""
    text = (resume_text or "").lower()
    matched = []
    for canonical_skill, keyword_variants in SKILL_KEYWORDS.items():
        if any(keyword in text for keyword in keyword_variants):
            matched.append(canonical_skill)
    return sorted(set(matched))


def get_role_scores(extracted_skills):
    """Return weighted role scores using core and bonus skills."""
    extracted_set = set(extracted_skills)
    scores = {}

    for role, profile in ROLE_PROFILES.items():
        core = profile["core"]
        bonus = profile["bonus"]

        matched_core = len(extracted_set.intersection(core))
        matched_bonus = len(extracted_set.intersection(bonus))

        core_score = (matched_core / len(core)) * 70 if core else 0
        bonus_score = (matched_bonus / len(bonus)) * 30 if bonus else 0
        percentage = round(core_score + bonus_score)

        matched_count = matched_core + matched_bonus
        total_count = len(core) + len(bonus)

        scores[role] = {
            "matched": matched_count,
            "total": total_count,
            "percentage": percentage,
        }

    return scores


def suggest_roles(role_scores):
    """Suggest roles sorted by highest score first."""
    ordered = sorted(
        role_scores.items(), key=lambda item: item[1]["percentage"], reverse=True
    )
    return ordered


def get_improvement_suggestions(extracted_skills, top_role, max_items=5):
    """Suggest missing skills for the top matched role with practical tips."""
    if not top_role:
        return ["Add more technical skills and project details to improve matching."]

    extracted_set = set(extracted_skills)
    role_profile = ROLE_PROFILES[top_role]
    role_skill_pool = role_profile["core"].union(role_profile["bonus"])
    missing = [skill for skill in role_skill_pool if skill not in extracted_set]

    suggestions = []
    for skill in missing:
        tip = IMPROVEMENT_TIPS.get(skill, f"Consider adding evidence of {skill} experience.")
        suggestions.append(f"{skill.title()}: {tip}")
        if len(suggestions) >= max_items:
            break

    if not suggestions:
        suggestions.append("Great match. Add quantified achievements to make your resume stronger.")

    return suggestions


@app.route("/", methods=["GET", "POST"])
def index():
    resume_text = ""
    extracted_skills = []
    role_scores = {}
    sorted_roles = []
    top_role = ""
    match_score = 0
    suggestions = []

    if request.method == "POST":
        resume_text = request.form.get("resume_text", "")
        extracted_skills = extract_skills(resume_text)
        role_scores = get_role_scores(extracted_skills)
        sorted_roles = suggest_roles(role_scores)

        if sorted_roles:
            top_role = sorted_roles[0][0]
            match_score = sorted_roles[0][1]["percentage"]

        suggestions = get_improvement_suggestions(extracted_skills, top_role)

    return render_template(
        "index.html",
        resume_text=resume_text,
        extracted_skills=extracted_skills,
        role_scores=role_scores,
        sorted_roles=sorted_roles,
        top_role=top_role,
        match_score=match_score,
        suggestions=suggestions,
    )


if __name__ == "__main__":
    app.run(debug=True)
