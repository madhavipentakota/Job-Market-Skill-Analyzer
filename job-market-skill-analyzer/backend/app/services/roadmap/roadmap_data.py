"""
Predefined roadmap templates (data-driven, editable).

Each roadmap is a list of stages. Each stage lists its topics, the skills
it teaches, a suggested project, an estimated time investment, and which
earlier stage titles are prerequisites.

This is the single source of truth used to SEED the database
(see backend/app/utils/seed_data.py). After seeding, roadmaps live in the
`career_roadmaps` / `roadmap_stages` tables and can be edited via the DB
or future admin endpoints without touching this file again.
"""

DATA_SCIENCE_ROADMAP = {
    "role_name": "Data Science",
    "description": "End-to-end path from Python fundamentals to a deployed ML application.",
    "stages": [
        {
            "title": "Stage 1: Python Fundamentals",
            "topics": ["Variables", "Data types", "Operators", "Conditions", "Loops",
                       "Functions", "Lists", "Tuples", "Sets", "Dictionaries",
                       "File handling", "Exception handling", "Basic OOP"],
            "skills": ["Python"],
            "suggested_project": "Expense Tracker",
            "estimated_hours": 40,
            "prerequisites": [],
        },
        {
            "title": "Stage 2: Mathematics for Data Science",
            "topics": ["Basic algebra", "Linear algebra basics", "Probability",
                       "Mean/Median/Mode", "Variance", "Standard deviation",
                       "Correlation", "Distributions", "Hypothesis testing"],
            "skills": ["Statistics"],
            "suggested_project": None,
            "estimated_hours": 25,
            "prerequisites": [],
        },
        {
            "title": "Stage 3: NumPy",
            "topics": ["Arrays", "Indexing", "Slicing", "Broadcasting",
                       "Mathematical operations", "Matrix operations"],
            "skills": ["NumPy"],
            "suggested_project": "Numerical Data Analysis",
            "estimated_hours": 12,
            "prerequisites": ["Stage 1: Python Fundamentals"],
        },
        {
            "title": "Stage 4: Pandas",
            "topics": ["Series", "DataFrames", "Data loading", "Data cleaning",
                       "Missing values", "Filtering", "GroupBy", "Merge", "Join",
                       "Aggregation"],
            "skills": ["Pandas"],
            "suggested_project": "Sales Data Analysis",
            "estimated_hours": 18,
            "prerequisites": ["Stage 3: NumPy"],
        },
        {
            "title": "Stage 5: Data Visualization",
            "topics": ["Bar charts", "Line charts", "Scatter plots", "Histograms",
                       "Box plots", "Heatmaps"],
            "skills": ["Matplotlib", "Seaborn"],
            "suggested_project": "Business Analytics Dashboard",
            "estimated_hours": 12,
            "prerequisites": ["Stage 4: Pandas"],
        },
        {
            "title": "Stage 6: SQL",
            "topics": ["SELECT", "WHERE", "GROUP BY", "ORDER BY", "HAVING", "JOIN",
                       "Subqueries", "Aggregate functions", "Window functions", "CTEs"],
            "skills": ["SQL"],
            "suggested_project": "Employee Database Analysis",
            "estimated_hours": 20,
            "prerequisites": [],
        },
        {
            "title": "Stage 7: Exploratory Data Analysis",
            "topics": ["Data cleaning", "Outlier detection", "Feature relationships",
                       "Correlation analysis", "Distribution analysis", "Feature engineering"],
            "skills": ["Pandas", "Statistics"],
            "suggested_project": "Real-world EDA Project",
            "estimated_hours": 15,
            "prerequisites": ["Stage 4: Pandas", "Stage 2: Mathematics for Data Science"],
        },
        {
            "title": "Stage 8: Machine Learning",
            "topics": ["Linear Regression", "Logistic Regression", "Decision Tree",
                       "Random Forest", "KNN", "SVM", "K-Means", "Hierarchical Clustering",
                       "PCA", "Accuracy", "Precision", "Recall", "F1 Score",
                       "Confusion Matrix", "MAE", "MSE", "RMSE", "R2"],
            "skills": ["Machine Learning", "Scikit-learn"],
            "suggested_project": "Customer Churn Prediction",
            "estimated_hours": 45,
            "prerequisites": ["Stage 7: Exploratory Data Analysis"],
        },
        {
            "title": "Stage 9: Advanced Data Science",
            "topics": ["Feature engineering", "Hyperparameter tuning", "Cross-validation",
                       "Ensemble learning", "Model pipelines", "Imbalanced datasets",
                       "Model interpretation"],
            "skills": ["Machine Learning"],
            "suggested_project": None,
            "estimated_hours": 25,
            "prerequisites": ["Stage 8: Machine Learning"],
        },
        {
            "title": "Stage 10: NLP",
            "topics": ["Text preprocessing", "Tokenization", "Stopwords", "Stemming",
                       "Lemmatization", "TF-IDF", "Text classification",
                       "Named Entity Recognition"],
            "skills": ["NLP"],
            "suggested_project": "Job Description Skill Extractor",
            "estimated_hours": 20,
            "prerequisites": ["Stage 8: Machine Learning"],
        },
        {
            "title": "Stage 11: Deployment",
            "topics": ["FastAPI", "REST APIs", "Git", "GitHub", "Docker basics",
                       "Cloud deployment basics"],
            "skills": ["FastAPI", "Git", "Docker"],
            "suggested_project": "End-to-End Data Science Application",
            "estimated_hours": 20,
            "prerequisites": ["Stage 8: Machine Learning"],
        },
    ],
}

# Lighter-weight placeholder roadmaps for the other careers named in the spec.
# Fill these out with the same {topics, skills, project, hours, prerequisites}
# structure as Data Science above.
DATA_ANALYST_ROADMAP = {
    "role_name": "Data Analyst",
    "description": "Path focused on SQL, Excel, and BI-tool driven analysis.",
    "stages": [
        {"title": "Stage 1: Excel & Spreadsheets", "topics": ["Formulas", "Pivot tables", "Charts"],
         "skills": ["Excel"], "suggested_project": "Sales Report", "estimated_hours": 10, "prerequisites": []},
        {"title": "Stage 2: SQL", "topics": ["SELECT", "JOIN", "GROUP BY", "Window functions"],
         "skills": ["SQL"], "suggested_project": "Retail Database Analysis", "estimated_hours": 20, "prerequisites": []},
        {"title": "Stage 3: Python for Analysis", "topics": ["Pandas", "NumPy", "Data cleaning"],
         "skills": ["Python", "Pandas"], "suggested_project": "Sales Data Analysis", "estimated_hours": 25,
         "prerequisites": ["Stage 1: Excel & Spreadsheets"]},
        {"title": "Stage 4: Statistics", "topics": ["Descriptive stats", "Correlation", "Hypothesis testing"],
         "skills": ["Statistics"], "suggested_project": None, "estimated_hours": 15, "prerequisites": []},
        {"title": "Stage 5: BI Tools", "topics": ["Dashboards", "DAX basics", "Data storytelling"],
         "skills": ["Power BI", "Tableau"], "suggested_project": "Business Dashboard", "estimated_hours": 15,
         "prerequisites": ["Stage 2: SQL"]},
    ],
}

PYTHON_DEVELOPER_ROADMAP = {
    "role_name": "Python Developer",
    "description": "Backend-focused Python engineering path.",
    "stages": [
        {"title": "Stage 1: Python Fundamentals", "topics": ["Syntax", "OOP", "File I/O", "Exceptions"],
         "skills": ["Python"], "suggested_project": "CLI Tool", "estimated_hours": 30, "prerequisites": []},
        {"title": "Stage 2: Data Structures & Algorithms", "topics": ["Lists", "Dicts", "Sorting", "Searching"],
         "skills": ["Python"], "suggested_project": None, "estimated_hours": 20,
         "prerequisites": ["Stage 1: Python Fundamentals"]},
        {"title": "Stage 3: Web Frameworks", "topics": ["FastAPI basics", "REST APIs", "Django basics"],
         "skills": ["FastAPI", "Django"], "suggested_project": "Task Manager API", "estimated_hours": 25,
         "prerequisites": ["Stage 2: Data Structures & Algorithms"]},
        {"title": "Stage 4: Databases", "topics": ["SQL", "ORMs", "Migrations"],
         "skills": ["SQL"], "suggested_project": None, "estimated_hours": 15,
         "prerequisites": ["Stage 3: Web Frameworks"]},
        {"title": "Stage 5: Deployment & Tools", "topics": ["Git", "Docker", "Cloud basics"],
         "skills": ["Git", "Docker", "AWS"], "suggested_project": "Deployed REST API", "estimated_hours": 15,
         "prerequisites": ["Stage 4: Databases"]},
    ],
}

FULL_STACK_ROADMAP = {
    "role_name": "Full Stack Developer",
    "description": "Frontend + backend + database path.",
    "stages": [
        {"title": "Stage 1: HTML/CSS/JavaScript", "topics": ["DOM", "Flexbox/Grid", "ES6"],
         "skills": ["JavaScript"], "suggested_project": "Portfolio Site", "estimated_hours": 25, "prerequisites": []},
        {"title": "Stage 2: React", "topics": ["Components", "Hooks", "Routing", "State management"],
         "skills": ["React"], "suggested_project": "Todo App", "estimated_hours": 30,
         "prerequisites": ["Stage 1: HTML/CSS/JavaScript"]},
        {"title": "Stage 3: Backend with Node/FastAPI", "topics": ["REST APIs", "Auth", "Middleware"],
         "skills": ["Node.js", "FastAPI"], "suggested_project": "Blog API", "estimated_hours": 25,
         "prerequisites": ["Stage 2: React"]},
        {"title": "Stage 4: Databases", "topics": ["SQL", "Schema design"],
         "skills": ["SQL"], "suggested_project": None, "estimated_hours": 15,
         "prerequisites": ["Stage 3: Backend with Node/FastAPI"]},
        {"title": "Stage 5: Deployment", "topics": ["Git", "Docker", "CI/CD basics"],
         "skills": ["Git", "Docker"], "suggested_project": "Deployed Full-Stack App", "estimated_hours": 15,
         "prerequisites": ["Stage 4: Databases"]},
    ],
}

MACHINE_LEARNING_ROADMAP = {
    "role_name": "Machine Learning",
    "description": "Focused path into ML engineering.",
    "stages": [
        {"title": "Stage 1: Python & Math Foundations", "topics": ["Python", "Linear algebra", "Probability"],
         "skills": ["Python", "Statistics"], "suggested_project": None, "estimated_hours": 30, "prerequisites": []},
        {"title": "Stage 2: Core ML", "topics": ["Regression", "Classification", "Clustering", "Evaluation metrics"],
         "skills": ["Machine Learning", "Scikit-learn"], "suggested_project": "Customer Churn Prediction",
         "estimated_hours": 35, "prerequisites": ["Stage 1: Python & Math Foundations"]},
        {"title": "Stage 3: Deep Learning", "topics": ["Neural networks", "CNNs", "RNNs basics"],
         "skills": ["Deep Learning", "TensorFlow", "PyTorch"], "suggested_project": "Image Classifier",
         "estimated_hours": 40, "prerequisites": ["Stage 2: Core ML"]},
        {"title": "Stage 4: MLOps Basics", "topics": ["Model serving", "Docker", "Monitoring basics"],
         "skills": ["Docker", "FastAPI"], "suggested_project": "Deployed ML Model API", "estimated_hours": 20,
         "prerequisites": ["Stage 3: Deep Learning"]},
    ],
}

AI_ENGINEER_ROADMAP = {
    "role_name": "AI Engineer",
    "description": "Applied AI systems path, building on ML foundations.",
    "stages": [
        {"title": "Stage 1: ML Foundations", "topics": ["Python", "Statistics", "Core ML"],
         "skills": ["Python", "Machine Learning"], "suggested_project": None, "estimated_hours": 40,
         "prerequisites": []},
        {"title": "Stage 2: Deep Learning", "topics": ["Neural networks", "Transformers basics"],
         "skills": ["Deep Learning", "PyTorch"], "suggested_project": "Text Classifier", "estimated_hours": 40,
         "prerequisites": ["Stage 1: ML Foundations"]},
        {"title": "Stage 3: NLP & LLMs", "topics": ["Tokenization", "Embeddings", "Prompting basics"],
         "skills": ["NLP"], "suggested_project": "Job Description Skill Extractor", "estimated_hours": 25,
         "prerequisites": ["Stage 2: Deep Learning"]},
        {"title": "Stage 4: Deployment & APIs", "topics": ["FastAPI", "Docker", "Cloud basics"],
         "skills": ["FastAPI", "Docker", "AWS"], "suggested_project": "Deployed AI Service", "estimated_hours": 20,
         "prerequisites": ["Stage 3: NLP & LLMs"]},
    ],
}

ALL_ROADMAPS = [
    DATA_SCIENCE_ROADMAP,
    DATA_ANALYST_ROADMAP,
    PYTHON_DEVELOPER_ROADMAP,
    FULL_STACK_ROADMAP,
    MACHINE_LEARNING_ROADMAP,
    AI_ENGINEER_ROADMAP,
]
