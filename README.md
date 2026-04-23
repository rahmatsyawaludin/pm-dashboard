# 🏗️ PM Executive Dashboard — Companion App

> A live **Project Management Executive Dashboard** built with Streamlit, showcasing real PM skills: schedule tracking, budget variance analysis, and risk heat mapping.

**🔗 Live Demo:** [Open Dashboard](https://your-app.streamlit.app) &nbsp;|&nbsp; **Portfolio:** [rahmatsyawaludin.github.io/portfolio](https://rahmatsyawaludin.github.io/portfolio/) &nbsp;|&nbsp; **Notion:** [Project Brief](https://pewter-washer-791.notion.site/Community-Based-Offline-Learning-Companion-App-28c46416af218007b7aedb724117a71d)

---

## 📊 What's Inside

| Section | PM Skills Demonstrated |
|---|---|
| **KPI Cards** | Real-time budget, progress & risk metrics |
| **Gantt Chart** | `NETWORKDAYS`-equivalent scheduling with today-line |
| **Budget Ledger** | Variance analysis (Estimated vs Actual) |
| **Risk Heat Map** | Impact × Probability matrix with severity bands |
| **Phase Completion** | `AVERAGEIF`-style aggregation by project phase |
| **Team Workload** | Resource allocation across owners |

---

## 🚀 Run Locally

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/pm-dashboard.git
cd pm-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to **[share.streamlit.io](https://share.streamlit.io)** → **New app**
3. Select your repo, branch `main`, file `app.py`
4. Click **Deploy** — live in ~2 minutes ✅

No server setup, no Docker, completely free.

---

## 🗂️ Project Structure

```
pm-dashboard/
├── app.py              ← Main Streamlit dashboard
├── requirements.txt    ← Python dependencies
├── README.md           ← This file
└── assets/
    └── data.xlsx       ← Source Excel workbook (optional)
```

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io)** — Python-native web app framework
- **[Plotly](https://plotly.com/python/)** — Interactive Gantt, donut & heat map charts
- **[Pandas](https://pandas.pydata.org)** — Data aggregation & analysis
- **[NumPy](https://numpy.org)** — Matrix operations for risk grid

---

*Built by Rahmat Syawaludin as part of a PM Portfolio showcasing the Community-Based Offline Learning Companion App project.*
