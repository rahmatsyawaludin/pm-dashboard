# PM Dashboard

> **From a Notion plan to a live executive dashboard — this is what happens when an instructional designer learns to ship.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20Dashboard-4A90D9?style=for-the-badge)](https://rahmatsyawaludin-pm-dashboard.streamlit.app/)
[![Portfolio](https://img.shields.io/badge/Back%20to%20Portfolio-grey?style=for-the-badge)](https://rahmatsyawaludin.github.io/portfolio/)

---

## The Problem

Ideas are cheap. Execution is the hard part.

During my Master's at Monash University, I designed a full [Community-Based Offline Learning Companion App](https://pewter-washer-791.notion.site/Community-Based-Offline-Learning-Companion-App-28c46416af218007b7aedb724117a71d) — a strategic plan addressing critically low literacy and numeracy outcomes in rural Indonesia. It was awarded High Distinction (83/100). But it was still just a plan.

A plan sitting in Notion doesn't help anyone make a decision. A project manager needs to *see* the data — budget burn, team load, delivery risk, schedule drift — in one place, updated and actionable.

So I built it.

---

## The Solution

PM Dashboard is a live, interactive project management dashboard that transforms the static strategic plan into a real operational tool. It takes structured data from a spreadsheet, processes it with Python, and renders it as a fully interactive executive dashboard — the kind a project manager would actually use to brief leadership and drive weekly decisions.

This project bridges two worlds: **learning design thinking** (the original Notion plan) and **technical execution** (the dashboard you can open right now).

---

## Key Features

- **💰 Budget Tracking** — Planned vs. actual spend tracked per category with a budget split donut chart and a full budget ledger. Spot overruns before they become blockers — down to individual vendor line items (`FIN-` rows).

- **⚠️ Risk Register** — Active risks scored by impact × probability, displayed with severity colour coding and mitigation strategies. Keeps the risk register visible at a glance, not buried in a spreadsheet (`RSK-` rows).

- **📅 Gantt Timeline** — A live Gantt chart showing planned vs. actual progress per task, with a today-line marker showing exactly where the project stands against the schedule right now.

- **👥 Team Workload** — Task count and completion rate visualised per team member. Spot overloaded contributors before burnout hits the delivery timeline.

- **✅ Phase Completion & WBS** — Work Breakdown Structure table plus a phase-by-phase completion bar chart — so every stakeholder can see delivery progress at both the task level and the phase level.

- **📊 KPI Summary Row** — A top-level executive view: total tasks, completion %, on-time rate, and budget variance — the four numbers a project sponsor needs in under 30 seconds.

---

## From Plan to Product — The Journey

```
Notion Doc          →    Spreadsheet         →    Python / Pandas      →    Streamlit Dashboard
(Strategic Plan)         (Structured Data)         (Data Processing)         (Live Execution View)
```

The original Monash project was a rigorous design exercise — co-designed with community members, grounded in Stanford D.school and Double Diamond methodology. But methodology alone doesn't ship.

This dashboard is proof that the thinking and the building don't have to live in separate worlds.

---

## Tech Stack

| Layer | Tech |
|-------|------|
| Language | Python |
| Dashboard Framework | Streamlit |
| Data Processing | Pandas |
| Visualisation | Plotly |
| Data Source | Google Sheets (live via CSV export API, refreshed every 5 min) |
| Hosting | Streamlit Cloud |

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/rahmatsyawaludin/pm-dashboard.git

# Navigate into the project
cd pm-dashboard

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

Or skip setup entirely and **[open the live dashboard](https://rahmatsyawaludin-pm-dashboard.streamlit.app/)**.

---

## The Bigger Picture

This project sits at the intersection of two things I care about: designing with rigour and building with purpose. The Notion plan showed I can think strategically. The dashboard shows I can execute technically.

Both matter. Neither is enough alone.

| Project | What It Demonstrates |
|---------|---------------------|
| [Notion — Original Plan](https://pewter-washer-791.notion.site/Community-Based-Offline-Learning-Companion-App-28c46416af218007b7aedb724117a71d) | Strategic design thinking · Co-design · HD 83/100 |
| [PM Dashboard](https://rahmatsyawaludin-pm-dashboard.streamlit.app/) ← **you are here** | Technical execution · Data pipeline · Live product |
| [EquiLearn](https://rahmatsyawaludin-equilearn.streamlit.app/) | Educational equity analytics · Data ethics in action |
| [EduPulse](https://rahmatsyawaludin.github.io/edupulse/) | Instructional design meets frontend product |
| [Human Firewall](https://rahmatsyawaludin.github.io/case-study-human-firewall/) | Gamified L&D case study · Behaviour change at scale |

---

## About the Author

**Rahmat Syawaludin** — Learning Designer · Instructional Designer · MEd Digital Learning, Monash University (LPDP Scholar)

📧 rahmatsywldn@gmail.com
🌐 [Portfolio](https://rahmatsyawaludin.github.io/portfolio/)
💼 [LinkedIn](https://linkedin.com/in/rahmat-syawaludin)
