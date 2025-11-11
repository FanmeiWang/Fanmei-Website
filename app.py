
# app.py
from flask import Flask, render_template, url_for
import os, json, re

app = Flask(__name__)

# ==========================
# Home / About
# ==========================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


# ==========================
# Education
# ==========================
education_data = [
    {
        "school": "Georgian College",
        "degree": "Post‑Graduate Certificate",
        "status": "Ongoing",
        "detail": "Artificial Intelligence – Architecture, Design, and Implementation",
        "logo": "georgian.png",
        "courses": [
            {"title": "Conversational AI", "status": "Completed"},
            {"title": "Machine Learning Programming", "status": "Completed"},
            {"title": "Artificial Intelligence Algorithms and Mathematics", "status": "Completed"},
            {"title": "Machine Learning Frameworks", "status": "Completed"},
            {"title": "Issues and Changes in Artificial Intelligence", "status": "Upcoming"},
            {"title": "Artificial Intelligence for Business Decision Making", "status": "Upcoming"},
            {"title": "Data Manipulation Techniques", "status": "Ongoing"},
            {"title": "Artificial Intelligence Infrastructure and Architecture", "status": "Ongoing"},
            {"title": "Vision Systems", "status": "Upcoming"},
            {"title": "Reinforcement Learning Programming", "status": "Upcoming"},
            {"title": "Neural Networks", "status": "Upcoming"},
            {"title": "Emerging Artificial Intelligence Technologies", "status": "Upcoming"},
            {"title": "Artificial Intelligence Project", "status": "Upcoming"},
            {"title": "Artificial Intelligence Robotics and Automation", "status": "Upcoming"},
        ],
    },
    {
        "school": "Peking University",
        "degree": "Ph.D. in Sociology",
        "status": "",
        "detail": "",
        "logo": "pku.png",
        "courses": [],
    },
    {
        "school": "Laurentian University",
        "degree": "M.A. in Sociology",
        "status": "",
        "detail": "",
        "logo": "laurentian.png",
        "courses": [],
    },
    {
        "school": "University of Science and Technology Beijing",
        "degree": "B.Eng in Business Administration",
        "status": "",
        "detail": "",
        "logo": "ustb.png",
        "courses": [],
    },
]

hrpa = {
    "status": "Completed",
    "logo": "HRPA.png",
    "courses": [
        "HR Management",
        "Compensation",
        "Labour Relations/Industrial Relations",
        "Finance & Accounting",
        "HR Planning",
        "Recruitment & Selection",
        "Training & Development",
        "Organizational Behaviour",
        "Occupational Health & Safety",
    ],
}

@app.route("/education")
def education():
    return render_template("education.html", edu_list=education_data, hrpa=hrpa)


# ==========================
# Publications
# ==========================
book_list = [
    {
        "title": "Affirmative Action – Historical Development and Social Influence ...",
        "role": "Book (Authored)",
        "cover": "affirmative-action.jpg",
        "cite": (
            "Wang, F.M. (2015). Affirmative Action – The Historical Development "
            "and Social Influence of Preferential Policies for Ethnic Minorities "
            "in the United States. Beijing: Social Sciences Academic Press. "
            "ISBN 9787509779606."
        ),
    },
    {
        "title": "Social Conflict: Escalation, Stalemate and Settlement (3rd ed.)",
        "role": "Book (Translator)",
        "cover": "social-conflict-cn.jpg",
        "cite": (
            "Pruitt, D.G. & Carnevale, P.J. (2021). Social Conflict (3rd ed.). "
            "Chinese translation by Fanmei Wang."
        ),
    },
]

article_list = [
    {
        "type": "Journal Article",
        "cite": (
            "Wang, F.M. (2019). Career Advancement for Tibetan Employees in Companies "
            "in the Tibet Autonomous Region. China: An International Journal, 17(1), 194-222."
        ),
    },
    {
        "type": "Journal Article",
        "cite": (
            "Wang, F.M.; Papia, K.; & Wang, Z.X. (2017). A Research on Economic Development "
            "of Georgia Since the 1990s. Journal of University of Science and Technology "
            "Beijing (Social Sciences Edition), 33(1), 99-112."
        ),
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. (2016). Research on Cultural Capital of Small- and Medium-Sized Private Enterprises in Tibetan Industries with Local Advantages. Qinghai Journal of Ethnology, 27(1), 166-171."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. (2015). Preferential Policies towards Minority Business Enterprise in the United States and What China Can Learn. Social Science Front, 6, 187-197."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. & Li, X.J. (2014). Educational Ideas in the Process of Internationalization. J. USTB (Social Sciences), 30(6), 100-108."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. (2014). Career Development of Tibetan Employees in SMEs in Tibet. Journal of Southwest University for Nationalities (Humanities & Social Science), 7, 53-58."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. (2014). Change in Education & Occupational Structure of African-American Labour Force. Chinese Journal of Population Science, 2, 84-95."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. & Huang, Z.Y. (2013). Performance Evaluation System of State-owned Cultural Enterprises. J. USTB (Social Sciences), 29(3), 90-97."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M., Ma, X. & Xi, W.W. (2013). Performance Evaluation System of Chinese Restaurants. Journal of South-Central University for Nationalities, 33(5), 128-131."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. & Xi, W.W. (2012). Problems in Enterprise Salary Systems. J. USTB (Social Sciences), 28(4), 124-133."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. (2012). Lessons from Western Ethnic Preferential Policy in Education – Example of U.S. Affirmative Action. Northwestern Journal of Ethnology, 2, 65-82 & 128."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. (2010). Historical Development of Affirmative Action in the United States. Northwestern Journal of Ethnology, 2, 45-80."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. (2010). Difficulties Encountered by Italian Americans in Affirmative Action. Journal of Southwest University for Nationalities, 5, 64-70."
    },
    {
        "type": "Journal Article",
        "cite": "Wang, F.M. (2009). Power Analysis for Campaigns Related to Genetically Modified Technology. J. USTB (Social Sciences), 25(4), 14-22."
    },
]

@app.route("/publications")
def publications():
    return render_template("publications.html", books=book_list, articles=article_list)


# ==========================
# Teaching
# ==========================
teaching_data = {
    "Undergraduate Courses": [
        {"course": "Human Resources Management", "level": "USTB · 2012 – 2017"},
        {"course": "Corporate Culture (English)", "level": "USTB · 2013 – 2017"},
        {"course": "Psychological Measurement & Selection", "level": "USTB · 2010 – 2017"},
        {"course": "Competency Development", "level": "USTB · 2012 – 2013"},
        {"course": "Management Communication", "level": "USTB · 2011 – 2012"},
        {"course": "Social Issues in Contemporary China (English)", "level": "IES Abroad · 2008"},
    ],
    "Graduate / MBA Courses": [
        {"course": "Human Resources Management", "level": "MBA / EMBA · USTB · 2010 – 2017"},
        {"course": "Corporate Culture (MBA)", "level": "USTB · 2013 – 2017"},
        {"course": "Organizational Behaviour", "level": "MBA / EMBA · USTB · 2011 – 2012"},
        {"course": "Chinese Economy & Industry (English)", "level": "Intl. students · USTB · 2011 – 2017"},
        {"course": "Research Methods & Thesis Writing (English)", "level": "Intl. students · USTB · 2010 – 2012"},
    ],
}

thesis_stats = {
    "bachelor": "43 Chinese + 3 international students",
    "master": "24 Chinese + 9 international students",
}

training_contract = [
    "“Corporate Culture” — MCC Sea Water Desalination Investment Co. · 2016",
    "“Performance Management” — Wuyang Iron & Steel · 2015",
    "“Human Resources Management” — Guangdong Topway Network · 2015",
    "“Corporate Culture” — Sinopec Corp. · 2014",
    "“Human Resources Management” — Shandong Gold Group · 2014",
    "“Corporate Culture” — BBMG Corporation · 2014",
    "“Performance Management” — HBIS Group · 2010–2015",
]

trainer_summary = (
    "Delivered in-house workshops for seven corporations, including "
    "Beijing Urban Construction Group and Jiangsu Xicheng Sanlian, "
    "covering performance evaluation, corporate culture, and communication management."
)

awards_data = [
    {
        "award": "Excellence in Teaching Award",
        "institution": "University of Science and Technology Beijing",
        "year": "2021",
        "desc": "Top university-wide teaching distinction presented annually.",
    },
    {
        "award": "Outstanding Graduate Instructor",
        "institution": "USTB School of Humanities & Social Sciences",
        "year": "2015",
        "desc": "For exceptional student evaluations and innovative pedagogy.",
    },
]

@app.route("/teaching")
def teaching_overview():
    # 自动抓取 teaching 相册（如目录不存在则退回预设清单）
    folder = os.path.join(app.static_folder, "img", "teaching")
    exts = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
    if os.path.isdir(folder):
        photos = sorted(
            {f for f in os.listdir(folder) if os.path.splitext(f)[1].lower() in exts},
            key=str.lower,
        )
    else:
        photos = [
            "teaching1.png",
            "teaching2.png",
            "teaching3.png",
            "teaching4.png",
            "teaching5.png",
            "teaching6.png",
            "teaching7.png",
            "teaching8.png",
            "teaching9.png",
        ]
    return render_template("teaching_overview.html", photos=photos, academic=teaching_data)

@app.route("/teaching/scroll")
def teaching_scroll():
    photos = [
        "teaching1.png",
        "teaching2.png",
        "teaching3.png",
        "teaching4.png",
        "teaching5.png",
        "teaching6.png",
        "teaching7.png",
        "teaching8.png",
        "teaching9.png",
    ]
    return render_template(
        "teaching.html",
        academic=teaching_data,
        thesis=thesis_stats,
        training_contract=training_contract,
        trainer_summary=trainer_summary,
        awards=awards_data,
        photos=photos,
    )

@app.route("/teaching/academic")
def teaching_academic():
    return render_template("teaching_academic.html", academic=teaching_data)

@app.route("/teaching/corporate")
def teaching_corporate():
    return render_template("teaching_corporate.html", training_contract=training_contract)

@app.route("/teaching/awards")
def teaching_awards():
    nat = [
        {
            "year": "2015",
            "title": "China Top 100 Selected MBA Cases Award — China National MBA Education Supervisory Committee",
        }
    ]
    univ = [
        {"year": "2018", "title": "Undergraduate Teaching Award"},
        {"year": "2016", "title": "Best Undergraduate Class Advisor"},
        {"year": "2014", "title": "Best Project — 1st Teaching Demonstration Courses Taught in English"},
        {"year": "2014", "title": "Outstanding Instructor — Excellent Course Teaching Styles (Undergraduate Courses with Bright Stars)"},
        {"year": "2014", "title": "Best MBA Curriculum Award — School of Economics & Management"},
        {"year": "2013", "title": "Best MBA Curriculum Award — School of Economics & Management"},
        {"year": "2013", "title": "1st place — 6th Postgraduate Teaching Awards"},
        {"year": "2013", "title": "1st place — 13th Young Faculty Teaching Competition"},
        {"year": "2013", "title": "2nd place — 1st Micro‑lecture Teaching Competition"},
    ]
    return render_template("teaching_awards.html", nat=nat, univ=univ)

@app.route("/teaching/thesis")
def teaching_thesis():
    # 支持 data/theses.json 或根目录同名文件
    candidates = [
        os.path.join(app.root_path, "data", "theses.json"),
        os.path.join(app.root_path, "theses.json"),
    ]
    data = {}
    for p in candidates:
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                data = json.load(f)
            break

    ug = data.get("undergraduate") or data.get("undergrad") or data.get("ug") or []
    pg = data.get("graduate") or data.get("grad") or []
    return render_template("teaching_thesis.html", ug_theses=ug, grad_theses=pg)


# ==========================
# Presentations
# ==========================
@app.route("/presentations")
def presentations():
    talks = [
        {
            "title": "How to Conduct Human Resources Management-Related Studies in China? (Chinese)",
            "venue": "Workshop “Research on Ethnic Minority Group Members in China”, Department of Sociology, Zhejiang University",
            "city": "Hangzhou, Zhejiang, China",
            "date": "Apr 28, 2019",
        },
        {
            "title": "Human Resource Management for Ethnic Minority Employees in Organizations in Chinese Minority‑inhabited Regions: A Case Study in the Tibetan Autonomous Region (Chinese)",
            "venue": "Institute for Advanced Study in Humanities & Social Sciences, Zhejiang University",
            "city": "Hangzhou, Zhejiang, China",
            "date": "Apr 29, 2019",
        },
        {
            "title": "A New Perspective in Analyzing China Ethnic‑related Employment Issues (English)",
            "venue": "Fairbank Center Visiting Scholar Presentations, Fairbank Center for Chinese Studies, Harvard University",
            "city": "Boston, MA",
            "date": "May 1, 2018",
        },
        {
            "title": "Career Development for Ethnic Minority Employees: A Case Study in the Tibetan Autonomous Region (English)",
            "venue": "Affiliate Presentations, Fairbank Center for Chinese Studies, Harvard University",
            "city": "Boston, MA",
            "date": "Apr 26, 2018",
        },
        {
            "title": "Chinese Ethnic Policies: An International Comparative Perspective (English)",
            "venue": "Ethics in Public Affair and Corporate Decision‑Making seminar course, Schwarzman College, Tsinghua University",
            "city": "Beijing, China",
            "date": "Feb 2, 2017",
        },
        {
            "title": "Chinese Ethnic Issues in the Context of One Belt, One Road Initiative (Chinese)",
            "venue": "“Cultural Diversity and Construction of One Belt, One Road”, Institute of Global Ethnology and Anthropology, Minzu University of China",
            "city": "Beijing, China",
            "date": "Dec 24, 2016",
        },
        {
            "title": "Affirmative Action – The Historical Development and Social Influence of Preferential Policies for Ethnic Minorities in the United States (Chinese)",
            "venue": "Department of Policies and Regulations, State Ethnic Affairs Commission of China",
            "city": "Beijing, China",
            "date": "Nov 6, 2016",
        },
        {
            "title": "Cross‑Cultural Management (English)",
            "venue": "MBA seminar, Manchester Metropolitan University Business School, School of Economics and Management, USTB",
            "city": "Beijing, China",
            "date": "Jun 9, 2016",
        },
        {
            "title": "Race and Ethnicity in America (Chinese)",
            "venue": "American Culture and Society Seminar Series, American Studies Center, Peking University",
            "city": "Beijing, China",
            "date": "Feb 29, 2013",
        },
        {
            "title": 'Panel Discussant: “(De)Constructing Myths of Migration”',
            "venue": "Harvard East Asia Society Conference 2018, 21st Annual Conference: (De)Constructing Boundaries, Harvard University",
            "city": "Boston, MA",
            "date": "Feb 9, 2018",
        },
    ]

    def classify_type(t):
        txt = (t.get("title", "") + " " + t.get("venue", "")).lower()
        if "panel" in txt or "discussant" in txt:
            return "Panel"
        if "workshop" in txt:
            return "Workshop"
        return "Invited Talk"

    typed_talks = []
    for t in talks:
        x = t.copy()
        x["type"] = classify_type(t)
        typed_talks.append(x)

    posters = ["Harvard_presentation_adv1.jpg", "Harvard_presentation_adv2.png"]
    left_photos = ["presentation1.jpg", "presentation6.jpg", "presentation7.jpg"]
    right_photos = ["Harvard_presentation1.jpg", "Harvard_presentation2.jpg", "Harvard_presentation3.jpg"]

    return render_template(
        "presentations.html",
        talks=typed_talks,
        posters=posters,
        left_photos=left_photos,
        right_photos=right_photos,
    )


# ==========================
# Projects
# ==========================
# 总览页（四宫格）
@app.route("/projects")
def projects():
    return render_template("projects.html")

# Academic research
academic_funded = [
    {
        "title": "The Development of Mutual Embeddedness of Social Structure of Ethnic Groups in Multiethnic Countries",
        "org": "Dept. of Sociology & IAS, Zhejiang University (Zhejiang, China)",
        "period": "2020 – present",
        "amount": "",
        "note": "PI: Zhixiang Jian",
    },
    {
        "title": "Ethnicity and Human Resources Management Practice in Chinese Minority‑inhabited Regions",
        "org": "IAS, Zhejiang University (Zhejiang, China)",
        "period": "2019",
        "amount": "$17,000 CAD (Fellowship grant)",
        "note": "",
    },
    {
        "title": "Career Development for Ethnic Minority Employees in Organizations in Chinese Ethnic Areas",
        "org": "Fairbank Center for Chinese Studies, Harvard University (funded by China Scholarship Council)",
        "period": "2017 – 2018",
        "amount": "$25,920 CAD",
        "note": "",
    },
    {
        "title": "Georgia in the Context of the New Silk Road Economic Belt",
        "org": "China Overseas Development Research Center, CUFE",
        "period": "2015 – 2016",
        "amount": "$4,000 CAD",
        "note": "",
    },
    {
        "title": "Career Development of Minority Ethnic Group Members in Tibet Autonomous Region",
        "org": "State Ethnic Affairs Commission of China (Beijing, China)",
        "period": "2013 – 2014",
        "amount": "$4,000 CAD",
        "note": "",
    },
    {
        "title": "Development of and Financial Support for Tibetan Industries with Local Advantages",
        "org": "China Tibetology Research Center (Beijing, China)",
        "period": "2013",
        "amount": "",
        "note": "PI: Shiding Liu",
    },
    {
        "title": "Tibetan Thangka Industry Development Research",
        "org": "China Tibetology Research Center (Beijing, China)",
        "period": "2012",
        "amount": "",
        "note": "PI: Danzeng‑Lunzhu",
    },
]

academic_international = [
    {
        "title": "Strategic Management Teaching Project",
        "org": (
            "State Administration of Foreign Experts Affairs of China — "
            "Joint with Maurice Yolles (LJMU, 2015–2016) and Paul Iles (GCU, 2017)"
        ),
        "period": "2015 – 2017",
        "amount": "$6,000 CAD (annually, 2015–2016); $10,000 (2017)",
        "note": "",
    },
    {
        "title": "Cultural Management and Leadership",
        "org": (
            "State Administration of Foreign Experts Affairs of China — "
            "Joint with Michael Robin Sebastian Green (University College Cork)"
        ),
        "period": "2016 – 2017",
        "amount": "$6,000 CAD (annually)",
        "note": "",
    },
]

@app.route("/projects/academic")
def projects_academic():
    return render_template("projects_academic.html", funded=academic_funded, intl=academic_international)

# Corporate consulting
consulting_projects = [
    {"title": "HRM Optimisation – Power T&D Industry", "client": "Huabiao Power T&D Engineering", "period": "2016 – 2017", "amount": "$8 000 CAD", "cover": "enterprise.jpg"},
    {"title": "Teaching & Admin Staffing Study (Inner Mongolia)", "client": "Hohhot Victory Education", "period": "2016 – 2017", "amount": "$12 000 CAD", "cover": "staff_study.jpg"},
    {"title": "Performance Mgmt. & Corporate Culture – Hainan Hongta", "client": "Hainan Hongta Co.", "period": "2015 – 2016", "amount": "$16 000 CAD", "cover": "hongta_perf.jpg"},
    {"title": "HRM & Compensation System – Ri-Chang Catering", "client": "Beijing Ri-Chang Catering", "period": "2011 – 2013", "amount": "$4 000 CAD", "cover": "ricang_hr.jpg"},
]

@app.route("/projects/consulting")
def projects_consulting():
    return render_template("projects_consulting.html", projects=consulting_projects)

# ---------- AI / ML 项目列表（数据） ----------
ai_projects = [
    {
        "title": "Azure Data & AI Architecture",
        "desc":  "12-step end‑to‑end lakehouse flow on Azure "
                 "(sources → ADF/Synapse Link → Delta Lake → Databricks "
                 "→ Serverless SQL/Power BI/ML).",
        "cover": "img/covers/Azure_Architecture.png",
        "endpoint": "projects_azure_arch",
        "category": "AI"
    },
    {
        "title": "Project Overview & Demo (Video)",
        "desc":  "5‑min walkthrough covering goals, design choices, and a short demo.",
        "cover": "img/covers/Azure_Architecture.png",
        "video": "video/Presentation.mp4",
        "category": "AI"
    },
    {
        "title": "Resume–Job Matching BERT Model",
        "desc":  "Fine‑tuned bilingual BERT + BM25 on 20k resumes and 5k job posts.",
        "video": "videos/resume_match.mp4",
        "category": "ML/DL"
    },
    {
        "title": "Attrition Prediction Dashboard (Power BI)",
        "desc":  "Explainable XGBoost + SHAP with live scenario filtering.",
        "video": "https://youtu.be/abcd1234",
        "category": "Analytics"
    },
]

# ---------- 通用项目卡片页（一个模板吃多个类别） ----------
from flask import abort

@app.route("/projects/ai")
def projects_ai():
    cards = [
        {
            "title": "Azure Data & AI Architecture",
            "summary": "12‑step end‑to‑end lakehouse flow on Azure (sources → ADF/Synapse Link → Delta Lake → Databricks → Serverless SQL/Power BI/ML).",
            "cover": "img/covers/Azure_Architecture.png",
            "href": url_for("projects_azure_arch"),
            "badge": "Azure"
        },
        {
            "title": "Text Classification Demonstration: Exploring Canada’s Immigration Discourse (video)",
            "summary": "Course project overview and demo video.",
            "cover": "img/covers/reddit_project_FanmeiHongan.png",
            "href": url_for("project_video", slug="presentation"),
            "badge": "Video"
        },
    ]
    return render_template("projects_cards.html",
                           page_title="AI Projects",
                           projects=cards)

@app.route("/projects/ml")
def projects_ml():
    cards = []
    return render_template("projects_cards.html",
                           page_title="ML / DL Projects",
                           projects=cards)

# 简单的视频详情页（把视频文件放到 static/video/Presentation.mp4）
@app.route("/projects/ai/<slug>")
def project_video(slug):
    videos = {
        "presentation": {
            "title": "AIDI1003 – Final Presentation",
            "file": "video/Presentation.mp4"  # static/video/Presentation.mp4
        }
    }
    v = videos.get(slug)
    if not v:
        abort(404)
    return render_template("project_video.html", video=v)

# 公共服务分析
surveys = [
    {"title": "Service Request Mgmt. System – Request-Tracking Dashboard", "role": "Lead Analyst", "period": "2024-ongoing"},
    {"title": "Qualitative Insights for HR Policy Team", "role": "Analyst", "period": "2024-ongoing"},
    {"title": "Exit-Survey Trend Mining", "role": "Analyst", "period": "2023-2024"},
    {"title": "Public-Service Employee Survey Deep Dive (2022-2023)", "role": "Analyst", "period": "2023-2024"},
    {"title": "Employee Opinions on Management & Leadership", "role": "Lead Analyst", "period": "2023-2024"},
    {"title": "Official-Language Team Ad-hoc Pulse (2020-2023)", "role": "Lead Analyst", "period": "2023"},
    {"title": "Early-Intervention / Return-to-Work Info-Session Survey", "role": "Lead Analyst (Acq-Card section)", "period": "2023"},
    {"title": "National Strike After-Action Feedback (Exec Cohort)", "role": "Analyst", "period": "2023"},
]
consults = [
    {"title": "ITB OKR 1.3 Cognitive‑Workload Survey", "role": "Questionnaire Reviewer", "period": "2024"},
    {"title": "Official‑Language Minority Communities Employee Survey", "role": "Questionnaire Reviewer", "period": "2024"},
    {"title": "National Leadership‑Learning Intake Survey", "role": "Questionnaire Reviewer", "period": "2024"},
    {"title": "PSES 2022‑2023 – Methodology Pack for Branch Clients", "role": "Lead Consultant", "period": "2023"},
    {"title": "Management Orientation – Slido & Feedback Form", "role": "Questionnaire Reviewer", "period": "2023"},
    {"title": "Data‑Literacy Baseline Survey", "role": "Methodology Lead", "period": "2023"},
    {"title": "Early‑Intervention / RTW Info‑Session Survey", "role": "Methodology Lead", "period": "2023"},
    {"title": "Service‑Culture Survey", "role": "Methodology Lead", "period": "2023"},
]

def _extract_year(period: str) -> int:
    if not period:
        return 0
    years = [int(y) for y in re.findall(r'(?:19|20)\d{2}', period)]
    return max(years) if years else 0

def _group_by_year(items):
    enriched = []
    for p in items:
        it = dict(p)
        it["year"] = _extract_year(p.get("period", ""))
        enriched.append(it)
    enriched.sort(key=lambda x: x["year"], reverse=True)

    groups = {}
    for it in enriched:
        groups.setdefault(it["year"], []).append(it)

    return sorted(groups.items(), key=lambda kv: kv[0], reverse=True)

@app.route("/projects/public-service")
def projects_public_service():
    survey_groups = _group_by_year(surveys)
    consult_groups = _group_by_year(consults)
    return render_template(
        "projects_public_service.html",
        survey_groups=survey_groups,
        consult_groups=consult_groups,
    )

# ==========================
# Azure Data & AI Architecture (Animated)
# ==========================
@app.route("/projects/ai/azure-architecture")
@app.route("/projects/azure-architecture")
def projects_azure_arch():
    # 模板名：templates/projects_azure_arch.html
    return render_template("projects_azure_arch.html")


# ==========================
# 调试：查看当前所有路由
# ==========================
@app.route("/__routes")
def __routes():
    lines = []
    for rule in app.url_map.iter_rules():
        methods = ",".join(sorted(m for m in rule.methods if m in {"GET", "POST"}))
        lines.append(f"{rule.rule:40s}  ->  {rule.endpoint}  [{methods}]")
    return "<pre>" + "\n".join(sorted(lines)) + "</pre>"


if __name__ == "__main__":
    # 开发模式自动重载
    app.run(debug=True)






