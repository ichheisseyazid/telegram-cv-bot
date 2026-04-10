# cv_fields.py

CV_FIELDS = [
    {
        "key": "full_name",
        "question": "What is your full name?",
        "ai_generated": False,
    },
    {
        "key": "email",
        "question": "What is your email address?",
        "ai_generated": False,
    },
    {
        "key": "phone",
        "question": "What is your phone number?",
        "ai_generated": False,
    },
    {
        "key": "location",
        "question": "What is your city and country? (e.g. Algiers, Algeria)",
        "ai_generated": False,
    },
    {
        "key": "job_title",
        "question": "What is your current or desired job title? (e.g. AI Engineer)",
        "ai_generated": False,
    },
    {
        "key": "professional_summary",
        "question": None,  # AI will generate this
        "ai_generated": True,
        "ai_prompt": (
            "Write a professional CV summary for someone with the job title '{job_title}'. "
            "Make it 3 sentences, confident, and suitable for a chronological CV. "
            "Return only the summary text, nothing else."
        ),
    },
    {
        "key": "experience_company",
        "question": "What is the name of your most recent employer?",
        "ai_generated": False,
    },
    {
        "key": "experience_role",
        "question": "What was your role/position there?",
        "ai_generated": False,
    },
    {
        "key": "experience_duration",
        "question": "How long did you work there? (e.g. Jan 2022 – Mar 2024)",
        "ai_generated": False,
    },
    {
        "key": "experience_description",
        "question": None,  # AI will generate this
        "ai_generated": True,
        "ai_prompt": (
            "Write 3 bullet points describing responsibilities and achievements "
            "for a '{experience_role}' at '{experience_company}'. "
            "Make them action-verb led and results-focused. "
            "Return only the bullet points, nothing else."
        ),
    },
    {
        "key": "education_degree",
        "question": "What is your highest degree? (e.g. Master's in AI)",
        "ai_generated": False,
    },
    {
        "key": "education_school",
        "question": "Which university or institution did you attend?",
        "ai_generated": False,
    },
    {
        "key": "education_year",
        "question": "What year did you graduate?",
        "ai_generated": False,
    },
    {
        "key": "skills",
        "question": "List your top skills separated by commas. (e.g. Python, Machine Learning, SQL)",
        "ai_generated": False,
    },
    {
        "key": "languages",
        "question": "What languages do you speak and at what level? (e.g. Arabic - Native, English - Fluent)",
        "ai_generated": False,
    },
]

# Quick lookup: only questions the bot needs to ask the user
USER_FIELDS = [f for f in CV_FIELDS if not f["ai_generated"]]

# Quick lookup: only fields the AI needs to generate
AI_FIELDS = [f for f in CV_FIELDS if f["ai_generated"]]