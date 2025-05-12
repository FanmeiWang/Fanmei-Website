from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  

@app.route("/about")                
def about():
    return render_template("about.html")

education_data = [
    {
        "school": "Georgian College",
        "degree": "Post-Graduate Certificate",
        "status": "Ongoing",
        "detail": "Artificial Intelligence – Architecture, Design, and Implementation",
        "logo": "georgian.png"
    },
    {
        "school": "Peking University",
        "degree": "Ph.D. in Sociology",
        "status": "",
        "detail": "",
        "logo": "pku.png"
    },
    {
        "school": "Laurentian University",
        "degree": "M.A. in Sociology",
        "status": "",
        "detail": "",
        "logo": "laurentian.png"
    },
    {
        "school": "University of Science and Technology Beijing",
        "degree": "B.Eng in Business Administration",
        "status": "",
        "detail": "",
        "logo": "ustb.png"
    },
]

@app.route("/education")
def education():
    return render_template("education.html", edu_list=education_data)

book_list = [
    {
        "title": "Affirmative Action – Historical Development and Social Influence ...",
        "role": "Book (Authored)",
        "cover": "affirmative-action.jpg",
        "cite": ("Wang, F.M. (2015). Affirmative Action – The Historical Development "
                 "and Social Influence of Preferential Policies for Ethnic Minorities "
                 "in the United States. Beijing: Social Sciences Academic Press. "
                 "ISBN 9787509779606.")
    },
    {
        "title": "Social Conflict: Escalation, Stalemate and Settlement (3rd ed.)",
        "role": "Book (Translator)",
        "cover": "social-conflict-cn.jpg",
        "cite": ("Pruitt, D.G. & Carnevale, P.J. (2021). *Social Conflict* (3rd ed.). "
                 "Chinese translation by Fanmei Wang.")
    },
]

article_list = [
    {
        "type": "Journal Article",
        "cite": ("Wang, F.M. (2019). Career Advancement for Tibetan Employees in Companies "
                 "in the Tibet Autonomous Region. *China: An International Journal*, 17(1), "
                 "194-222.")
    },
    {
        "type": "Journal Article",
        "cite": ("Wang, F.M.; Papia, K.; & Wang, Z.X. (2017). A Research on Economic Development "
                 "of Georgia Since the 1990s. *Journal of University of Science and Technology "
                 "Beijing (Social Sciences Edition)*, 33(1), 99-112.")
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. (2019). Career Advancement for Tibetan Employees in Companies in the Tibet Autonomous Region. *China: An International Journal*, 17(1), 194-222."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M., Papia, K. & Wang, Z.X. (2017). A Research on Economic Development of Georgia Since the 1990s. *Journal of University of Science and Technology Beijing (Social Sciences Edition)*, 33(1), 99-112."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. (2016). Research on Cultural Capital of Small- and Medium-Sized Private Enterprises in Tibetan Industries with Local Advantages. *Qinghai Journal of Ethnology*, 27(1), 166-171."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. (2015). Preferential Policies towards Minority Business Enterprise in the United States and What China Can Learn. *Social Science Front*, 6, 187-197."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. & Li, X.J. (2014). Educational Ideas in the Process of Internationalization. *J. USTB (Social Sciences)*, 30(6), 100-108."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. (2014). Career Development of Tibetan Employees in SMEs in Tibet. *Journal of Southwest University for Nationalities (Humanities & Social Science)*, 7, 53-58."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. (2014). Change in Education & Occupational Structure of African-American Labour Force. *Chinese Journal of Population Science*, 2, 84-95."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. & Huang, Z.Y. (2013). Performance Evaluation System of State-owned Cultural Enterprises. *J. USTB (Social Sciences)*, 29(3), 90-97."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M., Ma, X. & Xi, W.W. (2013). Performance Evaluation System of Chinese Restaurants. *Journal of South-Central University for Nationalities*, 33(5), 128-131."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. & Xi, W.W. (2012). Problems in Enterprise Salary Systems. *J. USTB (Social Sciences)*, 28(4), 124-133."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. (2012). Lessons from Western Ethnic Preferential Policy in Education – Example of U.S. Affirmative Action. *Northwestern Journal of Ethnology*, 2, 65-82 & 128."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. (2010). Historical Development of Affirmative Action in the United States. *Northwestern Journal of Ethnology*, 2, 45-80."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. (2010). Difficulties Encountered by Italian Americans in Affirmative Action. *Journal of Southwest University for Nationalities*, 5, 64-70."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. (2009). Power Analysis for Campaigns Related to Genetically Modified Technology. *J. USTB (Social Sciences)*, 25(4), 14-22."
    },
]

@app.route("/publications")
def publications():
    return render_template("publications.html",
                           books=book_list,
                           articles=article_list)

# ---------- Academic teaching data ----------
teaching_data = {
    "Undergraduate Courses": [
        {"course": "Human Resources Management",
         "level":  "USTB · 2012 – 2017"},
        {"course": "Corporate Culture (English)",
         "level":  "USTB · 2013 – 2017"},
        {"course": "Psychological Measurement & Selection",
         "level":  "USTB · 2010 – 2017"},
        {"course": "Competency Development",
         "level":  "USTB · 2012 – 2013"},
        {"course": "Management Communication",
         "level":  "USTB · 2011 – 2012"},
        {"course": "Social Issues in Contemporary China (English)",
         "level":  "IES Abroad · 2008"}
    ],
    "Graduate / MBA Courses": [
        {"course": "Human Resources Management",
         "level":  "MBA / EMBA · USTB · 2010 – 2017"},
        {"course": "Corporate Culture (MBA)",
         "level":  "USTB · 2013 – 2017"},
        {"course": "Organizational Behaviour",
         "level":  "MBA / EMBA · USTB · 2011 – 2012"},
        {"course": "Chinese Economy & Industry (English)",
         "level":  "Intl. students · USTB · 2011 – 2017"},
        {"course": "Research Methods & Thesis Writing (English)",
         "level":  "Intl. students · USTB · 2010 – 2012"}
    ]
}

# ---------- Thesis supervision summary ----------
thesis_stats = {
    "bachelor": "43 Chinese + 3 international students",
    "master":   "24 Chinese + 9 international students"
}

# ---------- Corporate-training records ----------
training_contract = [
    "“Corporate Culture” — MCC Sea Water Desalination Investment Co. · 2016",
    "“Performance Management” — Wuyang Iron & Steel · 2015",
    "“Human Resources Management” — Guangdong Topway Network · 2015",
    "“Corporate Culture” — Sinopec Corp. · 2014",
    "“Human Resources Management” — Shandong Gold Group · 2014",
    "“Corporate Culture” — BBMG Corporation · 2014",
    "“Performance Management” — HBIS Group · 2010–2015",
    # …其余条目…
]

trainer_summary = (
    "Delivered in-house workshops for seven corporations, including "
    "Beijing Urban Construction Group and Jiangsu Xicheng Sanlian, "
    "covering performance evaluation, corporate culture, and communication management."
)

# ---------- Teaching awards ----------
awards_data = [
    {"award": "Excellence in Teaching Award",
     "institution": "University of Science and Technology Beijing",
     "year": "2021",
     "desc": "Top university-wide teaching distinction presented annually."},
    {"award": "Outstanding Graduate Instructor",
     "institution": "USTB School of Humanities & Social Sciences",
     "year": "2015",
     "desc": "For exceptional student evaluations and innovative pedagogy."}
]

# ───────────────────────────
#  项 目 数据 重新整理
# ───────────────────────────

# 1) Academic Research  (学术项目)
academic_projects = [
    {
        "title": "Mutual Embeddedness of Social Structure of Ethnic Groups",
        "funding": "IAS, Zhejiang University",
        "period":  "2020 – present",
        "amount":  "—",
        "cover":   "tibet.jpg"
    },
    {
        "title": "Ethnicity & HRM Practice in Minority Regions",
        "funding": "IAS, Zhejiang University",
        "period":  "2019",
        "amount":  "$17 000 CAD",
        "cover":   "minority_hrm.jpg"
    },
    {
        "title": "Career Development for Minority Employees (TAR)",
        "funding": "Fairbank Center, Harvard University",
        "period":  "2017 – 2018",
        "amount":  "$25 920 CAD",
        "cover":   "tar_career.jpg"
    },
    {
        "title": "Georgia & the New Silk Road Economic Belt",
        "funding": "China ODRC, CUFE",
        "period":  "2015 – 2016",
        "amount":  "$4 000 CAD",
        "cover":   "silkroad.jpg"
    }
]

# 2) Corporate Consulting  (企业咨询 / 调研)
consulting_projects = [
    {
        "title":  "HRM Optimisation – Power T&D Industry",
        "client": "Huabiao Power T&D Engineering",
        "period": "2016 – 2017",
        "amount": "$8 000 CAD",
        "cover":  "enterprise.jpg"
    },
    {
        "title":  "Teaching & Admin Staffing Study (Inner Mongolia)",
        "client": "Hohhot Victory Education",
        "period": "2016 – 2017",
        "amount": "$12 000 CAD",
        "cover":  "staff_study.jpg"
    },
    {
        "title":  "Performance Mgmt. & Corporate Culture – Hainan Hongta",
        "client": "Hainan Hongta Co.",
        "period": "2015 – 2016",
        "amount": "$16 000 CAD",
        "cover":  "hongta_perf.jpg"
    },
    {
        "title":  "HRM & Compensation System – Ri-Chang Catering",
        "client": "Beijing Ri-Chang Catering",
        "period": "2011 – 2013",
        "amount": "$4 000 CAD",
        "cover":  "ricang_hr.jpg"
    }
]

# 3) HR + AI Projects  (以视频为主)
ai_projects = [
    {
        "title": "Resume–Job Matching BERT Model",
        "desc":  "Fine-tuned bilingual BERT + BM25 on 20 k resumes and 5 k job posts.",
        "video": "resume_match.mp4"          # 本地 static/video/…
    },
    {
        "title": "Attrition Prediction Dashboard (Power BI)",
        "desc":  "Explainable XGBoost + SHAP, live scenario filtering via Power BI Service.",
        "video": "https://youtu.be/abcd1234"  # YouTube 链接
    },
    {
        "title": "HR Chatbot for Policy Q&A (Rasa + LLM)",
        "desc":  "Hybrid retrieval-augmented Rasa bot answering leave & benefits questions.",
        "video": "chatbot_demo.mp4"
    }
]
# ---------- Public-Service Analytics ① · 内部数据项目 ----------
gov_survey_projects = [
    {"title": "Service Request Mgmt. System – Request-Tracking Dashboard",
     "role":  "Lead Analyst", "period": "2024-ongoing"},
    {"title": "Qualitative Insights for HR Policy Team",
     "role":  "Analyst", "period": "2024-ongoing"},
    {"title": "Exit-Survey Trend Mining",
     "role":  "Analyst", "period": "2023-2024"},
    {"title": "Public-Service Employee Survey Deep Dive (2022-2023)",
     "role":  "Analyst", "period": "2023-2024"},
    {"title": "Employee Opinions on Management & Leadership",
     "role":  "Lead Analyst", "period": "2023-2024"},
    {"title": "Official-Language Team Ad-hoc Pulse (2020-2023)",
     "role":  "Lead Analyst", "period": "2023"},
    {"title": "Early-Intervention / Return-to-Work Info-Session Survey",
     "role":  "Lead Analyst (Acq-Card section)", "period": "2023"},
    {"title": "National Strike After-Action Feedback (Exec Cohort)",
     "role":  "Analyst", "period": "2023"},
]

# ---------- Public-Service Analytics ② · 内部咨询项目 ----------
gov_consulting_projects = [
    {"title": "ITB OKR 1.3 Cognitive-Workload Survey",
     "role": "Questionnaire Reviewer", "period": "2024"},
    {"title": "Official-Language Minority Communities Employee Survey",
     "role": "Questionnaire Reviewer", "period": "2024"},
    {"title": "National Leadership-Learning Intake Survey",
     "role": "Questionnaire Reviewer", "period": "2024"},
    {"title": "PSES 2022-2023 – Methodology Pack for Branch Clients",
     "role": "Lead Consultant", "period": "2023"},
    {"title": "Management Orientation – Slido & Feedback Form",
     "role": "Questionnaire Reviewer", "period": "2023"},
    {"title": "Data-Literacy Baseline Survey",
     "role": "Methodology Lead", "period": "2023"},
    {"title": "Early-Intervention / RTW Info-Session Survey",
     "role": "Methodology Lead", "period": "2023"},
    {"title": "Service-Culture Survey",
     "role": "Methodology Lead", "period": "2023"},
]

@app.route("/projects")
def projects():          # ← endpoint = "projects"
    return render_template("projects.html")

@app.route("/projects/academic")
def projects_academic():
    return render_template("projects_academic.html",
                           projects=academic_projects)

@app.route("/projects/consulting")
def projects_consulting():
    return render_template("projects_consulting.html",
                           projects=consulting_projects)

@app.route("/projects/ai")
def projects_ai():
    return render_template("projects_ai.html",
                           projects=ai_projects)

@app.route("/projects/federal-analytics")
def projects_public_service():
    return render_template("projects_public_service.html",
                           surveys=gov_survey_projects,
                           consults=gov_consulting_projects)@app.route("/projects/ai")
teaching_photos = [
    "teaching1.png", "teaching2.png", "teaching3.png",
    "teaching4.png", "teaching5.png", "teaching6.png",
    "teaching7.png", "teaching8.png", "teaching9.png"
]

# 2️⃣ 把 photos=teaching_photos 传给模板
@app.route("/teaching")
def teaching_overview():
    return render_template(
        "teaching_overview.html",
        photos=teaching_photos        # ← 关键
    )
@app.route("/teaching/scroll")
def teaching_scroll():
    return render_template("teaching.html",
                           academic=teaching_data,
                           thesis=thesis_stats,
                           training_contract=training_contract,
                           trainer_summary=trainer_summary,
                           awards=awards_data,
                           photos=teaching_photos)
@app.route("/teaching/academic")
def teaching_academic():
    return render_template("teaching_academic.html",
                           academic=teaching_data)

@app.route("/teaching/corporate")
def teaching_corporate():
    return render_template("teaching_corporate.html",
                           training_contract=training_contract)

@app.route("/teaching/awards")
def teaching_awards():
    return render_template("teaching_awards.html",
                           awards=awards_data)

@app.route("/teaching/thesis")
def teaching_thesis():
    return render_template("teaching_thesis.html",
                           thesis=thesis_stats)

# 放在所有路由定义之后
from flask import redirect, url_for

# ---------- Presentation & Media ----------
presentation_data = [
    {
        "title": "Innovation, AI and HR Analytics",
        "venue": "Harvard University Fairbank Center",
        "date":  "2023-11-18",
        "type":  "Keynote",
        "link":  "https://fairbank.fas.harvard.edu/event/ai-hr-analytics/",   # 视频或网页
        "cover": "harvard_ai_talk.jpg"   # static/images/harvard_ai_talk.jpg
    },
    {
        "title": "Ethnicity & HRM Practice in Minority Regions",
        "venue": "Zhejiang University IAS",
        "date":  "2024-03-12",
        "type":  "Invited Talk",
        "link":  "https://ias.zju.edu.cn/talk/67890",
        "cover": "zju_ethnicity.jpg"
    },
    {
        "title": "Public-Service Employee Survey Deep Dive",
        "venue": "Treasury Board of Canada",
        "date":  "2024-05-02",
        "type":  "Internal Webinar",
        "link":  "",          # 只有列表，没有公开视频
        "cover": ""           # 没有图片
    },
    # ……其余条目……
]
@app.route("/presentations")
def presentations():
    return render_template("presentations.html",
                           talks=presentation_data)
if __name__ == "__main__":
    app.run(debug=True)
