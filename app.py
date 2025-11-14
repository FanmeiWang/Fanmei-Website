# app.py (clean merged)
from flask import Flask, render_template, url_for, abort, request, jsonify
import os, json, re, difflib

app = Flask(__name__)

# ---------------- Home / About ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# ---------------- Education ----------------
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

# ---------------- Publications ----------------
book_list = [
    {
        "title": "Affirmative Action – Historical Development and Social Influence ...",
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
    {"type": "Journal Article", "cite": "Wang, F.M. (2019). Career Advancement for Tibetan Employees in Companies in the Tibet Autonomous Region, China: An International Journal (SSCI), 17(1), 194-222."},
    {"type": "Journal Article", "cite": "Wang, F.M., Papia, K. & Wang, Z.X. (2017). 20 shiji 90 niandai yilai de Georgia jingji zhuangkuang yanjiu (A Research on Economic Development of Georgia Since the 1990s), Journal of University of Science and Technology Beijing (Social Sciences Edition), 33(1), 99-112."},
    {"type": "Journal Article", "cite": "Wang, F.M. (2016). Tibetan tese youshi chanye de zhongxiaoxing minying qiye wenhua ziben yanjiu (Research on Cultural Capital of Small- and Medium-Sized Private Enterprises in Tibetan Industries with Local Advantages), Qinghai Journal of Ethnology (CSSCI), 27(1),166-171."},
    {"type": "Journal Article", "cite": "Wang, F.M. (2015). America dui shaoshu qunti qiye de fuchixing cuoshi jiqi dui woguo de jiejian yiyi (The Preferential Policies towards Minority Business Enterprise in the United States and What China Can Learn from Them.), Social Science Front (CSSCI), 6, 187-197."},
    {"type": "Journal Article", "cite": "Wang, F.M. & Li, X.J. (2014). Guojihua huanjing xia de jiaoyu linian yu sikao: Jiyu wenxian fenxi de yanjiu (The Educational Ideas and Thoughts in the Internationalization: A Study Based on the Literature Analysis), Journal of University of Science and Technology Beijing (Social Sciences Edition), 30(6),100-108."},
    {"type": "Journal Article", "cite": "Wang, F.M. (2014). Tibetan yuangong zai Tibetan zhongxiaoxing minying qiye nei de zhiye fazhan yanjiu (Research on Career Development of Tibetan Employees in Middle- and Small- Sized Private Companies in Tibet), Journal of Southwest University for Nationalities (Humanities and Social Science) (CSSCI), 7, 53-58."},
    {"type": "Journal Article", "cite": "Wang, F.M. (2014). American heiren laodongli de jiaoyu he zhiye jiegou biandong zhuangkuang yanjiu (The Analysis of the Change in Education and Occupational Structure of African American Labour Force), Chinese Journal of Population Science (CSSCI), 2, 84-95."},
    {"type": "Journal Article", "cite": "Wang, F.M. & Huang, Z.Y. (2013). Guoyou wenhua qiye jixiao kaohe tixi yanjiu (Research on the Performance Evaluation System of State-owned Cultural Enterprises - With BPA Company as an Example), Journal of University of Science and Technology Beijing (Social Sciences Edition), 29(3), 90-97."},
    {"type": "Journal Article", "cite": "Wang, F.M., Ma, X. & Xi, W.W. (2013). Zhongcan liansuo qiye jixiao kaohe tixi de goujian yanjiu (Research on the Establishment of Performance Evaluation System of Chinese Restaurant), Journal of South-Central University for Nationalities (Humanities and Social Sciences) (CSSCI), 33(5),128-131."},
    {"type": "Journal Article", "cite": "Wang, F.M. & Xi, W.W. (2012). Qiye yunying zhong xinchou tixi wenti yanjiu (Investigation of the Problems in the Salary System in the Operation of Enterprises - Taking the RC Catering Company as a Case), Journal of University of Science and Technology Beijing (Social Sciences Edition), 28(4),124-133."},
    {"type": "Journal Article", "cite": "Wang, F.M. (2012). Xifang jiaoyu lingyu de zhongzu huo zuqun youhui zhengce duiyu woguo de jiejian yiyi – yi Affirmative Action of the United States weili (Positive Experiences and Negative Lessons Brought by Western Racial or Ethnic Preferential Policy in Western Educational Field - An Example of Affirmative Action), Northwestern Journal of Ethnology (CSSCI), 2, 65-82 &128."},
    {"type": "Journal Article", "cite": "Wang, F.M. (2010). Lishi yange Affirmative Action zai United States (The Historical Development of Affirmative Action in the United States), Northwestern Journal of Ethnology (CSSCI), 2, 45-80."},
    {"type": "Journal Article", "cite": "Wang, F.M. (2010). Shilun Italian Americans zai Affirmative Action zhong zaoyu de kunjing (The Difficulties Encountered by Italian Americans in Affirmative Action), Journal of Southwest University for Nationalities (Humanities and Social Science) (CSSCI), 5, 64-70."},
    {"type": "Journal Article", "cite": "Wang, F.M. (2010). Lun Jingju gaige zhong chuantong wenhua de baohu wenti (How to Protect Traditional Culture in the Reform of Peking Opera), Journal of South-Central University for Nationalities (Humanities and Social Sciences) (CSSCI), 30(3), 38-42."},
]

@app.route("/publications")
def publications():
    return render_template("publications.html", books=book_list, articles=article_list)

# ---------------- Teaching ----------------
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

thesis_stats = {"bachelor": "43 Chinese + 3 international students", "master": "24 Chinese + 9 international students"}

training_contract = [
    "“Corporate Culture” — MCC Sea Water Desalination Investment Company Ltd., Beijing, China· 2016",
    "“Performance Management” — Wuyang Iron & Steel, Wuyang, Henan· 2015",
    "“Human Resources Management” — Guangdong Topway Network Co., Ltd., Foshan, Guangdong, China· 2015",
    "“Corporate Culture” — Sinopec Corp. (China Petroleum & Chemical Corporation), Beijing, China· 2014",
    "“Human Resources Management” — Shandong Gold Group Co., Ltd., Beijing, China· 2014",
    "“Corporate Culture” — BBMG Corporation, Beijing, China· 2014",
    "“Performance Management” — MCC Sea Water Desalination Investment Company Ltd., Beijing, China· 2010–2015",
    "“Human Resources Management” — SHOUGANG (Shoudu Iron & Steel) Group, Beijing, China· 2012",
    "“Performance Management” — Tangshan Xinbaotai Iron & Steel Co., Ltd. Plant, Beijing, China· 2012",
    "“Performance Management” — HBIS (Hebei Iron & Steel) Group Co., Ltd., Shijiazhuang, Hebei, China· 2010, 2011 &2015",
    "“Human Resources Management” — Chengde Iron & Steel Group Co., Ltd., Chengde, Hebei, China· 2011&2012",
    "“Human Resources Management” — BBMG Corporation, Beijing, China· 2011&2012",
    "“Human Resources Management” — China National Tobacco Corporation, Hohhot, Inner Mongolia, China· 2010",
]

corporate_trainer = (
    "Served as a corporate trainer for seven corporations (i.e., Beijing Urban Construction Group Co., Ltd.; JiangSu Xicheng Sanlian Holding Group, etc.) among others."
    "Topics included on performance evaluation, corporate culture, and communication management."
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

# ---------------- Presentations（只保留一份） ----------------
@app.route("/presentations")
def presentations():
    talks = [
        {"title": "How to Conduct HRM‑Related Studies in China? (Chinese) Workshop “Research on Ethnic Minority Group Members in China”", "venue": "Zhejiang University", "city": "Hangzhou", "date": "Apr 28, 2019"},
        {"title": "Human Resource Management for Ethnic Minority Employees in Organizations in Chinese Minority- inhabited Regions: A Case Study in the Tibetan Autonomous Region” (in Chinese)", "venue": "Zhejiang University", "city": "Hangzhou", "date": "Apr 29, 2019"},
        {"title": "A New Perspective in Analyzing China Ethnic‑related Employment Issues (English)", "venue": "Harvard University", "city": "Boston, MA", "date": "May 1, 2018"},
        {"title": "Career Development for Ethnic Minority Employees: A Case Study in the Tibetan Autonomous Region", "venue": "Harvard University", "city": "Boston, MA", "date": "Apr 26, 2018"},
        {"title": "Chinese Ethnic Policies: An International Comparative Perspective (English)", "venue": "Tsinghua University", "city": "Beijing", "date": "Feb 2, 2017"},
        {"title": "Chinese Ethnic Issues in the Context of One belt, One Road Initiative (Chinese)", "venue": "Minzu University of China", "city": "Beijing", "date": "Dec 24, 2016"},
        {"title": "Affirmative Action – The Historical Development and Social Influence of Preferential Policies for Ethnic Minorities in the United States (Chinese)", "venue": "Tsinghua University", "city": "Beijing", "date": "Nov 6, 2016"},
        {"title": "Cross-Cultural Management (English)", "venue": "USTB", "city": "Beijing", "date": "Jun 9, 2016"},
    ]
    posters = ["Harvard_presentation_adv1.jpg", "Harvard_presentation_adv2.png"]
    left_photos  = ["presentation1.jpg", "presentation6.jpg", "presentation7.jpg"]
    right_photos = ["Harvard_presentation1.jpg", "Harvard_presentation2.jpg", "Harvard_presentation3.jpg"]
    return render_template("presentations.html", talks=talks, posters=posters, left_photos=left_photos, right_photos=right_photos)

# ---------------- Projects ----------------
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
            "summary": "12‑step lakehouse flow on Azure (sources → ADF/Synapse Link → Delta Lake → Databricks → Serverless SQL/Power BI/ML).",
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
    ]
    return render_template("projects_cards.html", page_title="AI Projects", projects=cards)

@app.route("/projects/ai/<slug>")
def project_video(slug):
    videos = {
        "presentation": {
            "title": "AIDI1003 – Final Presentation",
            "authors": "Fanmei Wang",
            "file": "video/Presentation_1.mp4",
            "poster": "img/covers/presentation_poster.jpg",
            "desc": "Course project overview and demo."
        }
    }
    v = videos.get(slug)
    if not v: abort(404)
    return render_template("project_video.html", title=v["title"], authors=v.get("authors"), desc=v.get("desc"), video=v)

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

# Azure Architecture demo（给 /projects/ai 里的卡片使用）
@app.route("/projects/azure-architecture")
@app.route("/projects/ai/azure-architecture")
def projects_azure_arch():
    return render_template("projects_azure_arch.html")

# Foundations & Engagements（保持一个 endpoint）
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

# ---------------- 站内聊天：只保留一个 /api/ask ----------------
def _norm(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9\s\-/]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def _sim(a: str, b: str) -> float:
    a, b = _norm(a), _norm(b)
    r = difflib.SequenceMatcher(None, a, b).ratio()
    ta, tb = set(a.split()), set(b.split())
    if ta and tb:
        r += 0.25 * (len(ta & tb) / max(len(ta), len(tb)))
    return r

ALIASES = {
    "about":        ["about", "who is fanmei", "profile", "bio", "fanmei wang"],
    "education":    ["education", "degree", "degrees", "diploma", "georgian", "phd", "m.a.", "ustb"],
    "teaching":     ["teaching", "course", "courses", "class", "mba", "emba", "supervision", "thesis"],
    "ai":           ["ai", "ai project", "demo", "azure architecture", "architecture demo", "animated"],
    "publications": ["publication", "publications", "paper", "papers", "book", "books", "article", "articles"],
    "contact":      ["contact", "email", "reach", "get in touch"],
}

QA_KB = [
    {"tag":"about", "patterns":["who is fanmei wang", "tell me about fanmei", "about fanmei", "简介", "自我介绍"],
     "answer":"I’m Fanmei Wang. See the About page for a short profile.", "endpoint":"about"},
    {"tag":"education", "patterns":["what degrees does fanmei hold","education background","degree","degrees","diploma","where did fanmei study"],
     "answer":"My programs and degrees are listed on the Education page.", "endpoint":"education"},
    {"tag":"teaching", "patterns":["what courses does fanmei teach","teaching","courses taught","mba","emba","thesis supervision"],
     "answer":"See Teaching & Training for academic courses, corporate training, awards, and thesis supervision.", "endpoint":"teaching_overview"},
    {"tag":"ai", "patterns":["ai projects","show me ai demos","azure architecture","animated architecture demo","where is the azure data & ai architecture demo"],
     "answer":"AI demos are in Projects → AI. The animated Azure Architecture demo is also under Projects.", "endpoint":"projects"},
    {"tag":"publications", "patterns":["publications","papers","book list","articles","著作","论文"],
     "answer":"Selected books and articles are on the Publications page.", "endpoint":"publications"},
    {"tag":"contact", "patterns":["contact","how can i contact you","email","get in touch","联系方式"],
     "answer":"Contact information is on the About page.", "endpoint":"about"},
]

def _best_kb_match(user_text: str):
    text = _norm(user_text)
    best, best_score = None, 0.0
    for item in QA_KB:
        alias_hits = sum(1 for w in ALIASES.get(item["tag"], []) if w in text)
        score = 0.15 * alias_hits
        pat_scores = [_sim(text, _norm(p)) for p in item["patterns"]]
        score += max(pat_scores or [0.0])
        if score > best_score:
            best, best_score = item, score
    return best, best_score

@app.post("/api/ask")
def api_ask():
    payload = request.get_json(silent=True) or {}
    q = (payload.get("q") or "").strip()
    if not q:
        return jsonify({"answer":"Ask about: About, Education, Teaching, Projects (incl. Azure Architecture), Publications, or how to contact Fanmei."})
    item, score = _best_kb_match(q)
    if item and score >= 0.55:
        return jsonify({"answer": item["answer"], "link": url_for(item["endpoint"]), "link_label":"Open →"})
    return jsonify({"answer": ("I can answer questions about this site: About, Education, Teaching, Projects "
                               "(incl. Azure Architecture), Publications, and how to contact Fanmei. "
                               "Try the quick buttons above.")})

# ---------------- Utilities ----------------
@app.route("/__routes")
def __routes():
    lines = []
    for rule in app.url_map.iter_rules():
        methods = ",".join(sorted(m for m in rule.methods if m in {"GET","POST"}))
        lines.append(f"{rule.rule:40s}  ->  {rule.endpoint}  [{methods}]")
    return "<pre>" + "\n".join(sorted(lines)) + "</pre>"

if __name__ == "__main__":
    app.run(debug=True)









