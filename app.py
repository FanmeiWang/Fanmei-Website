# app.py — clean merged
from flask import Flask, render_template, url_for, abort, request, jsonify
import os, json, re, difflib
from datetime import datetime, timezone


from openai import OpenAI   # 仅保留一次导入

app = Flask(__name__)

# ----------------------------- OpenAI Chat backend -----------------------------
# 仅保留一个客户端获取函数；避免应用启动时就因缺环境变量而崩溃
def get_openai_client():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        # 不让 SDK 在创建时才抛错；我们在接口里给出友好提示
        return None
    return OpenAI(api_key=key)

_ALLOWED = [
    "about", "education", "teaching", "projects", "publications",
    "azure", "azure architecture", "contact", "presentations"
]

def _is_allowed(q: str) -> bool:
    ql = (q or "").lower()
    return any(k in ql for k in _ALLOWED)

import re

PROFILE_FACTS_EN = (
    "Fanmei Wang holds a Ph.D. in Sociology from Peking University, "
    "an M.A. in Sociology from Laurentian University, and a B.Eng in Business Administration "
    "from the University of Science and Technology Beijing. "
    "She is currently completing a postgraduate AI certificate at Georgian College."
)

PROFILE_KEYWORDS = [
    "who is fanmei", "who is fanmei wang",
    "who are you", "tell me about yourself",
    "about fanmei", "your bio", "your profile",
    "education", "education background", "background",
    "degree", "degrees", "what did you study",
    "what is your major", "your major",
    "cv", "resume",
    "where did you study", "which university",
    "学位", "学历", "教育背景", "读的什么", "在哪读书"
]

def _looks_like_profile_question(q: str) -> bool:
    """Return True if the question is about Fanmei's identity / degrees / background."""
    q_norm = re.sub(r"\s+", " ", (q or "").lower()).strip()
    return any(key in q_norm for key in PROFILE_KEYWORDS)
    
@app.post("/api/chat")
def api_chat():
    data = request.get_json(silent=True) or {}
    q = (data.get("q") or data.get("message") or "").strip()
    if not q:
        return jsonify({"reply": "Please type a question about this site."}), 400

    # ① 简历/学历类问题：直接返回固定英文简介（不走 OpenAI）
    if _looks_like_profile_question(q):
        return jsonify({"reply": PROFILE_FACTS_EN})

    # ② 其他问题，再走 OpenAI：
    client = get_openai_client()
    if client is None:
        return jsonify({"reply": "Assistant is not configured (missing OPENAI_API_KEY)."}), 503

    system = (
        "You are the assistant for Fanmei Wang’s personal site. "
        "Answer briefly and helpfully about these sections only: "
        "About, Education, Teaching, Projects (including Azure Data & AI architecture), "
        "Publications, Presentations, and how to contact her. "
        "If the user asks for anything else, say you can only answer about the site."
    )

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.25,
            max_tokens=400,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": q},
            ],
        )
        reply = (resp.choices[0].message.content or "").strip()
        return jsonify({"reply": reply or "…"})
    except Exception as e:
        print("OpenAI error:", repr(e))
        return jsonify({"reply": "Sorry, I cannot reach the assistant right now."}), 502

@app.post("/api/ask")
def api_ask_compat():
    # 兼容老的前端：直接复用 /api/chat 的逻辑
    return api_chat()


# ----------------------------- Home / About -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# ----------------------------- Education -----------------------------
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
    {"school": "Peking University", "degree": "Ph.D. in Sociology", "status": "", "detail": "", "logo": "pku.png", "courses": []},
    {"school": "Laurentian University", "degree": "M.A. in Sociology", "status": "", "detail": "", "logo": "laurentian.png", "courses": []},
    {"school": "University of Science and Technology Beijing", "degree": "B.Eng in Business Administration", "status": "", "detail": "", "logo": "ustb.png", "courses": []},
]
hrpa = {
    "status": "Completed",
    "logo": "HRPA.png",
    "courses": [
        "HR Management","Compensation","Labour Relations/Industrial Relations","Finance & Accounting",
        "HR Planning","Recruitment & Selection","Training & Development","Organizational Behaviour","Occupational Health & Safety",
    ],
}

@app.route("/education")
def education():
    return render_template("education.html", edu_list=education_data, hrpa=hrpa)

# ----------------------------- Publications -----------------------------
book_list = [
    {
        "title": "Affirmative Action - The Historical Development and Social Influence of Preferential Policies for Ethnic Minorities in the United States",
        "role": "Book (Authored)",
        "cover": "affirmative-action.jpg",
        "cite": (
            "Wang, F.M. (2015). Affirmative Action – The Historical Development and Social Influence "
            "of Preferential Policies for Ethnic Minorities in the United States. Beijing: SSAP. "
            "ISBN 9787509779606."
        ),
    },
    {
        "title": "Social Conflict: Escalation, Stalemate and Settlement (3rd ed.)",
        "role": "Book (Translator)",
        "cover": "social-conflict-cn.jpg",
        "cite": ("Pruitt, D.G. & Carnevale, P.J. (2021). Social Conflict (3rd ed.). Chinese translation by Fanmei Wang."),
    },
]
article_list = [
    {"type": "Journal Article", "cite": "Wang, F.M. (2019). Career Advancement for Tibetan Employees in Companies in the Tibet Autonomous Region. *China: An International Journal*, 17(1), 194-222."},
    {"type": "Journal Article", "cite": "Wang, F.M.; Papia, K.; & Wang, Z.X. (2017). A Research on Economic Development of Georgia Since the 1990s. *Journal of University of Science and Technology Beijing (Social Sciences Edition)*, 33(1), 99-112."},
    {"type": "Journal Article", "cite": "Wang, F.M. (2016). Research on Cultural Capital of Small- and Medium-Sized Private Enterprises in Tibetan Industries with Local Advantages. *Qinghai Journal of Ethnology*, 27(1), 166-171."},
    {"type": "Journal Article", "cite": "Wang, F.M. (2015). The Preferential Policies towards Minority Business Enterprise in the United States and What China Can Learn from Them. *Social Science Front*, 6, 187-197."},
    {"type": "Journal Article", "cite": "Wang, F.M. & Li, X.J. (2014). The Educational Ideas and Thoughts in the Internationalization: A Study Based on the Literature Analysis. *Journal of University of Science and Technology Beijing (Social Sciences Edition)*, 30(6), 100-108."},
    {"type": "Journal Article", "cite": "Wang, F.M. (2014). Research on Career Development of Tibetan Employees in Middle- and Small- Sized Private Companies in Tibet. *Journal of Southwest University for Nationalities (Humanities and Social Science)*, 7, 53-58."},
    {"type": "Journal Article", "cite": "Wang, F.M. (2014). The Analysis of the Change in Education and Occupational Structure of African American Labour Force. *Chinese Journal of Population Science*, 2, 84-95."},
    {"type": "Journal Article", "cite": "Wang, F.M. & Huang, Z.Y. (2013). Research on the Performance Evaluation System of State-owned Cultural Enterprises - With BPA Company as an Example. *Journal of University of Science and Technology Beijing (Social Sciences Edition)*, 29(3), 90-97."},
    {"type": "Journal Article", "cite": "Wang, F.M., Ma, X. & Xi, W.W. (2013). Research on the Establishment of Performance Evaluation System of Chinese Restaurant. *J. South‑Central Univ. for Nationalities*, 33(5), 128-131."},
    {"type": "Journal Article", "cite": "Wang, F.M. & Xi, W.W. (2012). Investigation of the Problems in the Salary System in the Operation of Enterprises - Taking the RC Catering Company as a Case. *Journal of South-Central University for Nationalities (Humanities and Social Sciences)*, 28(4), 124-133."},
    {"type": "Journal Article", "cite": "Wang, F.M. (2012). Positive Experiences and Negative Lessons Brought by Western Racial or Ethnic Preferential Policy in Western Educational Field - An Example of Affirmative Action. *Northwestern Journal of Ethnology*, 2, 65-82 & 128."},
    {"type": "Journal Article", "cite": "Wang, F.M. (2010). The Historical Development of Affirmative Action in the United States), Northwestern Journal of Ethnology. *Northwestern Journal of Ethnology*, 2, 45-80."},
    {"type": "Journal Article", "cite": "Wang, F.M. (2010). The Difficulties Encountered by Italian Americans in Affirmative Action. *Journal of Southwest University for Nationalities (Humanities and Social Science) *, 5, 64-70."},
    {"type": "Journal Article", "cite": "Wang, F.M. (2010). How to Protect Traditional Culture in the Reform of Peking Opera *Journal of Southwest University for Nationalities (Humanities and Social Science) *, 30(3), 38-42."},
    {"type": "Journal Article", "cite": "Wang, F.M. (2009). Power Analysis for Campaigns Related to Genetically Modified Technology. *Journal of University of Science and Technology Beijing (Social Sciences Edition) *, 25(4), 14-22."},
]
@app.route("/publications")
def publications():
    return render_template("publications.html", books=book_list, articles=article_list)

# ----------------------------- Teaching -----------------------------
teaching_data = {
    "Undergraduate Courses": [
        {"course": "Human Resources Management", "level": "USTB · 2012 – 2017"},
        {"course": "Corporate Culture (English)", "level": "USTB · 2013 – 2017"},
        {"course": "Psychometrics & Personnel Selection / Quantitative Methods", "level": "USTB · 2010 – 2017"},
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
thesis_stats = {"bachelor": "43 Chinese + 3 international students", "master": "24 Chinese + 9 international students"}
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
    "Delivered in-house workshops for seven corporations, including Beijing Urban Construction Group and "
    "Jiangsu Xicheng Sanlian, covering performance evaluation, corporate culture, and communication management."
)
awards_data = [
    {"award": "Excellence in Teaching Award", "institution": "University of Science and Technology Beijing", "year": "2021",
     "desc": "Top university-wide teaching distinction presented annually."},
    {"award": "Outstanding Graduate Instructor", "institution": "USTB School of Humanities & Social Sciences", "year": "2015",
     "desc": "For exceptional student evaluations and innovative pedagogy."},
]

def _list_teaching_photos():
    folder = os.path.join(app.static_folder, "img", "teaching")
    exts = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
    if os.path.isdir(folder):
        files = sorted({f for f in os.listdir(folder) if os.path.splitext(f)[1].lower() in exts}, key=str.lower)
        if files: return files
    return [f"teaching{i}.png" for i in range(1,10)]

@app.route("/teaching")
def teaching_overview():
    return render_template("teaching_overview.html", photos=_list_teaching_photos(), academic=teaching_data)

@app.route("/teaching/scroll")
def teaching_scroll():
    return render_template("teaching.html",
                           academic=teaching_data,
                           thesis=thesis_stats,
                           training_contract=training_contract,
                           trainer_summary=trainer_summary,
                           awards=awards_data,
                           photos=_list_teaching_photos())

@app.route("/teaching/academic")
def teaching_academic():
    return render_template("teaching_academic.html", academic=teaching_data)

@app.route("/teaching/corporate")
def teaching_corporate():
    return render_template("teaching_corporate.html", training_contract=training_contract)

@app.route("/teaching/awards")
def teaching_awards():
    nat = [{"year": "2015", "title": "China Top 100 Selected MBA Cases Award — China National MBA Education Supervisory Committee"}]
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
    candidates = [os.path.join(app.root_path, "data", "theses.json"), os.path.join(app.root_path, "theses.json")]
    data = {}
    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, encoding="utf-8") as f: data = json.load(f)
            except Exception:
                pass
            break
    ug = data.get("undergraduate") or data.get("undergrad") or data.get("ug") or []
    pg = data.get("graduate") or data.get("grad") or []
    return render_template("teaching_thesis.html", ug_theses=ug, grad_theses=pg)

# ----------------------------- Presentations -----------------------------
@app.route("/presentations")
def presentations():
    talks = [
        {"title": "How to Conduct HRM‑Related Studies in China? (Chinese)", "venue": "Zhejiang University", "city": "Hangzhou", "date": "Apr 28, 2019"},
        {"title": "Human Resource Management for Ethnic Minority Employees in Organizations in Chinese Minority- inhabited Regions: A Case Study in the Tibetan Autonomous Region (Chinese)", "venue": "Zhejiang University", "city": "Hangzhou", "date": "Apr 29, 2019"},
        {"title": "A New Perspective in Analyzing China Ethnic‑related Employment Issues (English)", "venue": "Fairbank Center for Chinese Studies, Harvard University", "city": "Boston, MA", "date": "May 1, 2018"},
        {"title": "Career Development for Ethnic Minority Employees: A Case Study in the Tibetan Autonomous Region (English)", "venue": "Fairbank Center for Chinese Studies, Harvard University", "city": "Boston, MA", "date": "Apr 26, 2018"},
        {"title": "Chinese Ethnic Policies: An International Comparative Perspective (English)", "venue": "Schwarzman College, Tsinghua University", "city": "Beijing", "date": "Feb 2, 2017"},
        {"title": "Chinese Ethnic Issues in the Context of One belt, One Road Initiative (Chinese)", "venue": "Central Minzu University of China", "city": "Beijing", "date": "Dec 24, 2016"},
        {"title": "Cross-Cultural Management (English)", "venue": "School of Economics and Management, University of Science and Technology Beijing", "city": "Beijing", "date": "Jun 9, 2016"},
    ]
    posters = ["Harvard_presentation_adv1.jpg", "Harvard_presentation_adv2.png"]
    left_photos  = ["presentation1.jpg", "presentation6.jpg", "presentation7.jpg"]
    right_photos = ["Harvard_presentation1.jpg", "Harvard_presentation2.jpg", "Harvard_presentation3.jpg"]
    return render_template("presentations.html", talks=talks, posters=posters, left_photos=left_photos, right_photos=right_photos)

# ----------------------------- Projects -----------------------------
@app.route("/projects")
def projects():
    return render_template("projects.html")

# Academic research pages
academic_funded = [
    {"title": "Mutual Embeddedness of Social Structure of Ethnic Groups", "org": "IAS, Zhejiang University", "period": "2020 – present", "amount": "", "note": "PI: Zhixiang Jian"},
    {"title": "Ethnicity and HRM Practice in Minority‑inhabited Regions", "org": "IAS, Zhejiang University", "period": "2019", "amount": "$17,000 CAD", "note": ""},
    {"title": "Career Development for Ethnic Minority Employees in Chinese Ethnic Areas", "org": "Harvard University / CSC", "period": "2017 – 2018", "amount": "$25,920 CAD", "note": ""},
    {"title": "Georgia in the Context of the New Silk Road", "org": "China ODRC, CUFE", "period": "2015 – 2016", "amount": "$4,000 CAD", "note": ""},
    {"title": "Career Development in TAR", "org": "State Ethnic Affairs Commission of China", "period": "2013 – 2014", "amount": "$4,000 CAD", "note": ""},
]
academic_international = [
    {"title": "Strategic Management Teaching Project", "org": "SAFEA (with Maurice Yolles / Paul Iles)", "period": "2015 – 2017", "amount": "$6,000 (2015–2016); $10,000 (2017)", "note": ""},
    {"title": "Cultural Management and Leadership", "org": "SAFEA (with M.R.S. Green, UCC)", "period": "2016 – 2017", "amount": "$6,000 (annually)", "note": ""},
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

# AI projects cards
@app.route("/projects/ai")
def projects_ai():
    cards = [
        {
            "title": "Azure Data & AI Architecture",
            "summary": "12‑step lakehouse flow on Azure (sources → ADF/Synapse Link → Delta Lake → Databricks → Serverless SQL/Power BI/ML @Fanmei Wang).",
            "cover": "img/covers/Azure_Architecture.png",
            "href": url_for("projects_azure_arch"),
            "badge": "Azure"
        },
        {
            "title": "Text Classification Demo (video)",
            "summary": "Course project overview and demo video.",
            "cover": "img/covers/reddit_project_FanmeiHongan.png",
            "href": url_for("project_video", slug="presentation"),
            "badge": "Video"
        },
        {
    "title": "AI Translation Tool (Azure) – Accessible Demo",
    "summary": (
        "Video demo of a non-production AI translation tool built on Azure Translator, "
        "showing visual accessibility choices such as dark mode, high-contrast theme, "
        "adjustable font and line spacing, and a screen-reader friendly status message.@Fanmei Wang"
    ),
    "cover": "img/covers/translator_demo_poster.jpg",
    "href": url_for("project_video", slug="translator-demo"),
    "badge": "Video"
},

    ]
    return render_template("projects_cards.html", page_title="My AI & Education Product Lab", projects=cards)

@app.route("/projects/ai/<slug>")
def project_video(slug):
    videos = {
        "presentation": {
            "title": "Classifying Canadian Immigration Topics on Reddit with DistilBERT",
            "authors": "Fanmei Wang & Hongan Lai",
            "file": "video/Presentation_web.mp4",
            "poster": "img/covers/presentation_poster.jpg",
            "desc": "Small team project (postgraduate). I built the end‑to‑end pipeline on 10k+ Reddit submissions, designed 8 topic labels, curated ~1.1k human‑verified samples, and fine‑tuned DistilBERT (test accuracy ≈ 78.6%). Hongan supported text cleaning, contributed to manual verification, prepared several baseline models, implemented a small Flask demo, and recorded the video. The classifier is used to examine topic shifts on Reddit before and after the May 31, 2023 policy."
        },
        "translator-demo": {
            "title": "AI Translator (Azure) – screen demo",
            "authors": "Fanmei Wang",
            "file": "video/translator_demo.mp4",          # <— 对应你刚放进去的文件
            "poster": "img/covers/translator_demo_poster.jpg",  # 没有海报可以先去掉本行
            "desc": "Screen-recorded walkthrough of a Streamlit MVP built on Azure Translator."
        },
    }
    v = videos.get(slug)
    if not v:
        abort(404)
    return render_template(
        "project_video.html",
        title=v["title"],
        authors=v.get("authors"),
        desc=v.get("desc"),
        video=v,
    )

# Public‑Service Analytics (按年聚合)
surveys = [
    {"title": "Service Request Mgmt. System – Request-Tracking Dashboard", "role": "Lead Analyst", "period": "2024-ongoing"},
    {"title": "Qualitative Insights for HR Policy Team", "role": "Analyst", "period": "2024-ongoing"},
    {"title": "Exit-Survey Trend Mining", "role": "Analyst", "period": "2023-2024"},
    {"title": "PSES Deep Dive (2022-2023)", "role": "Analyst", "period": "2023-2024"},
]
consults = [
    {"title": "ITB OKR 1.3 Cognitive‑Workload Survey", "role": "Questionnaire Reviewer", "period": "2024"},
    {"title": "National Leadership‑Learning Intake Survey", "role": "Questionnaire Reviewer", "period": "2024"},
    {"title": "PSES 2022‑2023 – Methodology Pack", "role": "Lead Consultant", "period": "2023"},
]

def _extract_year(period: str) -> int:
    years = [int(y) for y in re.findall(r'(?:19|20)\d{2}', period or "")]
    return max(years) if years else 0

def _group_by_year(items):
    enriched = []
    for p in items:
        it = dict(p); it["year"] = _extract_year(p.get("period","")); enriched.append(it)
    enriched.sort(key=lambda x: x["year"], reverse=True)
    groups = {}
    for it in enriched: groups.setdefault(it["year"], []).append(it)
    return sorted(groups.items(), key=lambda kv: kv[0], reverse=True)

@app.route("/projects/public-service")
def projects_public_service():
    return render_template("projects_public_service.html",
                           survey_groups=_group_by_year(surveys),
                           consult_groups=_group_by_year(consults))

# Azure Architecture demo（供 /projects/ai 卡片使用）
@app.route("/projects/azure-architecture")
@app.route("/projects/ai/azure-architecture")
def projects_azure_arch():
    return render_template("projects_azure_arch.html")

# Foundations & Engagements
@app.route("/projects/foundations", endpoint="foundations_engagements")
def foundations_engagements_page():
    page = {
        "title": "Foundations & Engagements",
        "blurb": "A consolidated view of research/advisory work shaping how I approach data & AI.",
        "scope": "Spanning 2010–2020 (research) and 2011–2017 (advisory), with occasional pro bono since."
    }
    research = ["D&I in employment", "Fieldwork & mixed‑methods", "Graduate‑level methods teaching"]
    advisory = ["Org & HR systems", "Culture & change", "Employee listening & surveys", "Analytics & dashboards", "Pro bono toolkits"]
    bridge = ("These foundations inform current Public‑Service Data & AI work—from privacy‑first data engineering to applied NLP/ML.")
    return render_template("foundations_engagements.html", page=page, research=research, advisory=advisory, bridge=bridge)

# ----------------------------- Utilities -----------------------------
@app.route("/__routes")
def __routes():
    lines = []
    for rule in app.url_map.iter_rules():
        methods = ", ".join(sorted(m for m in rule.methods if m in {"GET", "POST"}))
        lines.append(f"{rule.rule:40s}  ->  {rule.endpoint}  [{methods}]")
    return "<pre>" + "\n".join(sorted(lines)) + "</pre>"

# NEW ▸ Detail page for the Translator demo
@app.route("/projects/ai/translator")
def projects_ai_translator():
    page = {
        "title": "AI Translator (Azure)",
        "desc": "Lightweight Flask demo using Azure Translator for EN↔ZH, built for bilingual learning with privacy guardrails. OpenAI can be enabled optionally for rewriting or tone.",
    }
    features = [
        "EN↔ZH translation, optional glossary / term‑highlighting",
        "Safe defaults: client‑side truncation, input length hints, PII caution banner",
        "Tone & style toggles (formal / plain), quick rewrite presets (optional via OpenAI)",
        "No prompt logging; secrets only via environment (.env)"
    ]
    arch = [
        "Browser → Flask route (/projects/ai/translator) → Azure Translator (REST)",
        "Optional: Flask → OpenAI (chat completions) for rewrite/tone",
        "Config via .env (.env.example committed; real .env kept local/host‑only)",
        "No keys in repo; .env is git‑ignored"
    ]
    links = [
        # 没有线上地址就先删掉或注释
        # {"text": "Open live demo", "href": "https://<your-demo-url>"},
        # {"text": "View source on GitHub", "href": "https://github.com/<you>/<repo>/tree/main/apps/translator"},
    ]
    return render_template(
        "projects_ai_translator.html",
        page=page, features=features, arch=arch, links=links
    )
@app.context_processor
def inject_now():
    from datetime import datetime
    return {"current_year": datetime.utcnow().year}

if __name__ == "__main__":
    # 本地调试启动
    app.run(debug=True)

















