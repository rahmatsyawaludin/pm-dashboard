import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, datetime
import numpy as np

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PM Dashboard · Companion App",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── DATA ──────────────────────────────────────────────────────────────────────
SHEET_ID = "12A3aiONTf4SEuEA2Ktont9nTV56xcXPEh2zJvF50xhs"

@st.cache_data(ttl=600)
def load_data():
    def get_url(sheet_name):
        return f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    
    # 1. Load WBS/Tasks
    tasks_df = pd.read_csv(get_url("WBS"))
    tasks_df = tasks_df.rename(columns={
        'Task ID': 'id',
        'Phase': 'phase',
        'Task Name': 'task',
        'Assigned To': 'owner',
        'Start Date': 'start',
        'End Date': 'end',
        'Status': 'status',
        '% Complete': 'pct',
        'Priority': 'priority'
    })
    
    # 2. Load Budget
    budget_df = pd.read_csv(get_url("Budget"))
    budget_df = budget_df.rename(columns={
        'Item ID': 'id',
        'Category': 'category',
        'Description': 'item',
        'Estimated ($)': 'est',   # Keep it 'est' to match your KPI logic
        'Actual ($)': 'act',      # Keep it 'act' to match your KPI logic
        'Status': 'status'
    })

    # Clean up dates and remove empty rows if any
    tasks_df = tasks_df.dropna(subset=['start', 'end'])
    tasks_df['start'] = pd.to_datetime(tasks_df['start']).dt.date
    tasks_df['end'] = pd.to_datetime(tasks_df['end']).dt.date
    
    return tasks_df, budget_df

# CRITICAL: This line assigns the data to the names your script expects
tasks, budget = load_data() 




# ─── COMPUTED METRICS ──────────────────────────────────────────────────────────
today = date.today()
total_budget   = budget["estimated"].sum()
total_spent    = budget["actual"].sum()
remaining      = total_budget - total_spent
tasks_done     = (tasks["status"] == "Completed").sum()
overall_pct    = tasks["pct"].mean()
launch_date    = date(2026, 9, 1)
days_to_launch = (launch_date - today).days
avg_risk       = risks["score"].mean()

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --navy:   #0f1f3d;
    --teal:   #0b7b74;
    --gold:   #d4a017;
    --cream:  #f8f5ef;
    --red:    #c0392b;
    --green:  #1a7a4a;
    --amber:  #d97706;
    --muted:  #6b7280;
    --card:   #ffffff;
    --border: #e5e0d8;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--cream) !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 2rem 2rem !important; max-width: 1400px; }

/* ── HEADER ── */
.dash-header {
    background: linear-gradient(135deg, #0f1f3d 0%, #0b7b74 100%);
    border-radius: 0 0 24px 24px;
    padding: 2.5rem 2.5rem 2rem;
    margin: -1rem -2rem 2rem -2rem;
    position: relative;
    overflow: hidden;
}
.dash-header::before {
    content: '';
    position: absolute; top: -60px; right: -60px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: rgba(212, 160, 23, 0.12);
}
.dash-header::after {
    content: '';
    position: absolute; bottom: -40px; left: 30%;
    width: 140px; height: 140px;
    border-radius: 50%;
    background: rgba(255,255,255, 0.05);
}
.header-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem; font-weight: 600;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: #d4a017; margin-bottom: 0.5rem;
}
.header-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem; font-weight: 400;
    color: #ffffff; line-height: 1.15;
    margin: 0 0 0.4rem;
}
.header-sub {
    font-size: 0.95rem; color: rgba(255,255,255,0.65);
    font-weight: 300; margin: 0;
}
.header-badge {
    display: inline-block;
    background: rgba(212,160,23,0.2);
    border: 1px solid rgba(212,160,23,0.5);
    color: #f5c842; border-radius: 20px;
    font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.08em; padding: 3px 12px;
    margin-top: 1rem;
}

/* ── KPI CARDS ── */
.kpi-wrap {
    background: var(--card);
    border-radius: 16px;
    border: 1px solid var(--border);
    padding: 1.2rem 1.4rem 1.1rem;
    height: 110px;
    position: relative;
    overflow: hidden;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.kpi-wrap:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(15,31,61,0.1);
}
.kpi-accent {
    position: absolute; top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 16px 0 0 16px;
}
.kpi-label {
    font-size: 0.68rem; font-weight: 600;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--muted); margin-bottom: 0.35rem;
}
.kpi-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem; color: var(--navy);
    line-height: 1; margin-bottom: 0.25rem;
}
.kpi-sub {
    font-size: 0.72rem; color: var(--muted); font-weight: 300;
}

/* ── SECTION TITLES ── */
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem; color: var(--navy);
    margin: 2rem 0 1rem;
    display: flex; align-items: center; gap: 0.6rem;
}
.section-title::after {
    content: ''; flex: 1;
    height: 1px; background: var(--border);
}

/* ── TABLES ── */
.styled-table {
    width: 100%; border-collapse: separate;
    border-spacing: 0; font-size: 0.85rem;
}
.styled-table thead th {
    background: var(--navy); color: white;
    font-size: 0.7rem; font-weight: 600;
    letter-spacing: 0.1em; text-transform: uppercase;
    padding: 10px 14px; text-align: left;
}
.styled-table thead th:first-child { border-radius: 10px 0 0 0; }
.styled-table thead th:last-child  { border-radius: 0 10px 0 0; }
.styled-table tbody tr:nth-child(even) td { background: #f9f7f3; }
.styled-table tbody tr:nth-child(odd) td  { background: #ffffff; }
.styled-table tbody td {
    padding: 9px 14px; border-bottom: 1px solid var(--border);
    color: #374151;
}
.styled-table tbody tr:last-child td:first-child { border-radius: 0 0 0 10px; }
.styled-table tbody tr:last-child td:last-child  { border-radius: 0 0 10px 0; }

/* ── STATUS BADGES ── */
.badge {
    display: inline-block; padding: 3px 10px;
    border-radius: 20px; font-size: 0.72rem;
    font-weight: 600; letter-spacing: 0.04em;
}
.badge-done     { background:#d1fae5; color:#065f46; }
.badge-progress { background:#fef3c7; color:#92400e; }
.badge-pending  { background:#f1f5f9; color:#475569; }
.badge-high     { background:#fee2e2; color:#991b1b; }
.badge-medium   { background:#fef9c3; color:#854d0e; }
.badge-low      { background:#dcfce7; color:#166534; }
.badge-critical { background:#fee2e2; color:#991b1b; }
.badge-partial  { background:#fef3c7; color:#92400e; }

/* ── PROGRESS BARS ── */
.progress-outer {
    height: 7px; background: #e5e7eb;
    border-radius: 99px; overflow: hidden;
}
.progress-inner {
    height: 100%; border-radius: 99px;
    background: linear-gradient(90deg, #0b7b74, #0f1f3d);
    transition: width 0.4s ease;
}

/* ── RISK MATRIX LABELS ── */
.risk-critical { color: #c0392b; font-weight: 700; }
.risk-high     { color: #d97706; font-weight: 700; }
.risk-low      { color: #1a7a4a; font-weight: 700; }

/* ── FOOTER ── */
.dash-footer {
    margin-top: 3rem; padding: 1.5rem 0;
    border-top: 1px solid var(--border);
    text-align: center;
    font-size: 0.78rem; color: var(--muted);
}
.dash-footer a { color: var(--teal); text-decoration: none; font-weight: 500; }
.dash-footer a:hover { text-decoration: underline; }

/* Plotly chart backgrounds */
.js-plotly-plot .plotly { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ─── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="dash-header">
    <div class="header-tag">PM Portfolio · Rahmat Syawaludin</div>
    <h1 class="header-title">Community-Based Offline<br>Learning Companion App</h1>
    <p class="header-sub">Executive Project Dashboard — Live metrics across schedule, budget & risk</p>
    <span class="header-badge">🟢 &nbsp;PROJECT ACTIVE · Updated {datetime.now().strftime('%d %b %Y')}</span>
</div>
""", unsafe_allow_html=True)

# ─── KPI ROW ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5, k6, k7 = st.columns(7)

kpis = [
    (k1, "TOTAL BUDGET",    f"${total_budget:,.0f}",  "Allocated",           "#0f1f3d"),
    (k2, "SPENT TO DATE",   f"${total_spent:,.0f}",   f"${remaining:,.0f} left", "#c0392b"),
    (k3, "BUDGET HEALTH",   f"{(remaining/total_budget)*100:.0f}%", "Remaining", "#1a7a4a"),
    (k4, "TASKS DONE",      f"{tasks_done}/{len(tasks)}", "Completed",        "#0b7b74"),
    (k5, "OVERALL PROGRESS",f"{overall_pct*100:.0f}%", "Avg completion",      "#2563eb"),
    (k6, "AVG RISK SCORE",  f"{avg_risk:.1f}",         "Out of 25",           "#d97706"),
    (k7, "DAYS TO LAUNCH",  str(max(days_to_launch, 0)), f"Target: {launch_date.strftime('%d %b %Y')}", "#6b21a8"),
]

for col, label, value, sub, accent in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-wrap">
            <div class="kpi-accent" style="background:{accent}"></div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── ROW 1: GANTT + BUDGET DONUT ───────────────────────────────────────────────
col_gantt, col_donut = st.columns([3, 1.4])

with col_gantt:
    st.markdown('<div class="section-title">📅 Project Timeline (Gantt)</div>', unsafe_allow_html=True)

    phase_colors = {
        "Discovery":   "#0b7b74",
        "Design":      "#2563eb",
        "Development": "#7c3aed",
        "Content":     "#d97706",
        "QA/Testing":  "#dc2626",
        "Deployment":  "#059669",
        "Support":     "#64748b",
    }

    fig_gantt = go.Figure()

    for _, row in tasks.iterrows():
        color = phase_colors.get(row["phase"], "#94a3b8")
        start_dt = datetime.combine(row["start"], datetime.min.time())
        end_dt   = datetime.combine(row["end"],   datetime.min.time())

        # Full bar (faded)
        fig_gantt.add_trace(go.Bar(
            x=[(end_dt - start_dt).days],
            y=[f"{row['id']} · {row['task'][:38]}"],
            base=[start_dt.timestamp() * 1000],
            orientation='h',
            marker=dict(color=color, opacity=0.22, line=dict(width=0)),
            showlegend=False, hoverinfo='skip',
        ))
        # Progress fill
        progress_days = (end_dt - start_dt).days * row["pct"]
        if progress_days > 0:
            fig_gantt.add_trace(go.Bar(
                x=[progress_days],
                y=[f"{row['id']} · {row['task'][:38]}"],
                base=[start_dt.timestamp() * 1000],
                orientation='h',
                marker=dict(color=color, opacity=0.9, line=dict(width=0)),
                showlegend=False,
                customdata=[[row["task"], row["owner"], row["status"], f"{row['pct']*100:.0f}%", row["end"].strftime("%d %b")]],
                hovertemplate="<b>%{customdata[0]}</b><br>Owner: %{customdata[1]}<br>Status: %{customdata[2]}<br>Progress: %{customdata[3]}<br>Due: %{customdata[4]}<extra></extra>",
            ))

    # Today line
    today_ts = datetime.combine(today, datetime.min.time()).timestamp() * 1000
    fig_gantt.add_vline(x=today_ts, line_width=2, line_dash="dot", line_color="#d4a017",
                        annotation_text="Today", annotation_font_color="#d4a017",
                        annotation_font_size=10)

    fig_gantt.update_layout(
        barmode='overlay',
        height=420,
        margin=dict(l=0, r=10, t=10, b=30),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="DM Sans", size=11, color="#374151"),
        xaxis=dict(
            type='date', showgrid=True,
            gridcolor='rgba(0,0,0,0.06)', gridwidth=1,
            tickformat="%b '%y", tickfont=dict(size=10),
            zeroline=False,
        ),
        yaxis=dict(showgrid=False, tickfont=dict(size=10)),
        showlegend=False,
    )
    st.plotly_chart(fig_gantt, use_container_width=True, config={"displayModeBar": False})

with col_donut:
    st.markdown('<div class="section-title">💰 Budget Split</div>', unsafe_allow_html=True)

    by_cat = budget.groupby("category")[["estimated","actual"]].sum().reset_index()

    fig_donut = go.Figure(go.Pie(
        labels=by_cat["category"],
        values=by_cat["actual"],
        hole=0.62,
        textinfo='label+percent',
        textfont=dict(family="DM Sans", size=11),
        marker=dict(colors=["#0f1f3d","#0b7b74","#2563eb","#7c3aed","#d97706","#dc2626","#64748b","#059669"],
                    line=dict(color='#f8f5ef', width=2)),
        hovertemplate="<b>%{label}</b><br>Actual: $%{value:,.0f}<extra></extra>",
    ))
    fig_donut.add_annotation(
        text=f"<b>${total_spent:,.0f}</b><br><span style='font-size:10px'>Total Spent</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=14, family="DM Serif Display", color="#0f1f3d"),
        align="center",
    )
    fig_donut.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(family="DM Sans"),
    )
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

    # Budget health mini bars
    for _, row in by_cat.iterrows():
        var = row["actual"] - row["estimated"]
        pct_bar = min(row["actual"] / row["estimated"], 1.4) * 100 if row["estimated"] > 0 else 0
        color = "#c0392b" if var > 0 else "#1a7a4a"
        st.markdown(f"""
        <div style="margin-bottom:8px">
            <div style="display:flex;justify-content:space-between;font-size:0.72rem;color:#6b7280;margin-bottom:3px">
                <span>{row['category']}</span>
                <span style="color:{color};font-weight:600">{'+' if var > 0 else ''}${var:,.0f}</span>
            </div>
            <div class="progress-outer">
                <div class="progress-inner" style="width:{min(pct_bar,100)}%;background:{'#c0392b' if var > 0 else '#0b7b74'}"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─── ROW 2: TASK TABLE + RISK MATRIX ───────────────────────────────────────────
col_tasks, col_risk = st.columns([1.8, 1])

with col_tasks:
    st.markdown('<div class="section-title">📋 Work Breakdown Structure</div>', unsafe_allow_html=True)

    status_badge = {
        "Completed":   '<span class="badge badge-done">✓ Done</span>',
        "In Progress": '<span class="badge badge-progress">◎ Active</span>',
        "Not Started": '<span class="badge badge-pending">○ Pending</span>',
    }
    priority_badge = {
        "High":   '<span class="badge badge-high">High</span>',
        "Medium": '<span class="badge badge-medium">Med</span>',
        "Low":    '<span class="badge badge-low">Low</span>',
    }

    rows_html = ""
    for _, r in tasks.iterrows():
        days_left = (r["end"] - today).days
        days_str = "Done" if r["status"] == "Completed" else ("⚠ Overdue" if days_left < 0 else f"{days_left}d")
        days_color = "#c0392b" if (days_left < 0 and r["status"] != "Completed") else "#374151"
        bar_w = int(r["pct"] * 100)
        rows_html += f"""
        <tr>
            <td style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#0b7b74;font-weight:600">{r['id']}</td>
            <td style="font-weight:500">{r['task']}</td>
            <td style="color:#6b7280">{r['owner']}</td>
            <td>{status_badge.get(r['status'],'')}</td>
            <td>
                <div style="display:flex;align-items:center;gap:6px">
                    <div class="progress-outer" style="width:60px">
                        <div class="progress-inner" style="width:{bar_w}%"></div>
                    </div>
                    <span style="font-size:0.75rem;color:#6b7280">{bar_w}%</span>
                </div>
            </td>
            <td>{priority_badge.get(r['priority'],'')}</td>
            <td style="font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:{days_color};font-weight:600">{days_str}</td>
        </tr>"""

    st.markdown(f"""
    <div style="overflow-x:auto">
    <table class="styled-table">
        <thead><tr>
            <th>ID</th><th>Task</th><th>Owner</th><th>Status</th>
            <th>Progress</th><th>Priority</th><th>Days Left</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

with col_risk:
    st.markdown('<div class="section-title">⚠️ Risk Register</div>', unsafe_allow_html=True)

    # Heatmap
    matrix = np.zeros((5, 5))
    risk_positions = []
    for _, r in risks.iterrows():
        i = r["impact"] - 1
        p = r["prob"] - 1
        matrix[i][p] += r["score"]
        risk_positions.append((p, i, r["id"], r["score"]))

    fig_heat = go.Figure()

    # Background zones
    for y in range(5):
        for x in range(5):
            score = (y+1) * (x+1)
            color = "#fee2e2" if score >= 15 else ("#fef3c7" if score >= 8 else "#dcfce7")
            fig_heat.add_shape(type="rect",
                x0=x-0.5, x1=x+0.5, y0=y-0.5, y1=y+0.5,
                fillcolor=color, line=dict(color="white", width=1.5))
            fig_heat.add_annotation(x=x, y=y, text=str(score),
                showarrow=False, font=dict(size=9, color="#9ca3af", family="JetBrains Mono"))

    # Risk dots
    for (px, py, rid, score) in risk_positions:
        dot_color = "#c0392b" if score >= 15 else ("#d97706" if score >= 8 else "#1a7a4a")
        fig_heat.add_trace(go.Scatter(
            x=[px], y=[py], mode="markers+text",
            marker=dict(size=28, color=dot_color, line=dict(color="white", width=2)),
            text=[rid[-3:]], textfont=dict(size=9, color="white", family="JetBrains Mono"),
            textposition="middle center",
            name=rid,
            hovertemplate=f"<b>{rid}</b><br>Score: {score}<extra></extra>",
        ))

    fig_heat.update_layout(
        height=260,
        margin=dict(l=30, r=10, t=10, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis=dict(tickvals=list(range(5)), ticktext=["P1","P2","P3","P4","P5"],
                   title=dict(text="Probability →", font=dict(size=10)), range=[-0.5,4.5], zeroline=False),
        yaxis=dict(tickvals=list(range(5)), ticktext=["I1","I2","I3","I4","I5"],
                   title=dict(text="Impact ↑", font=dict(size=10)), range=[-0.5,4.5], zeroline=False),
        font=dict(family="DM Sans"),
    )
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})

    # Risk list
    level_cls = {"Critical":"risk-critical","High":"risk-high","Low":"risk-low"}
    level_icon = {"Critical":"🔴","High":"🟡","Low":"🟢"}
    for _, r in risks.iterrows():
        cls = level_cls.get(r["level"],"")
        icon = level_icon.get(r["level"],"")
        st.markdown(f"""
        <div style="padding:10px 14px;background:white;border-radius:10px;
                    border:1px solid #e5e0d8;margin-bottom:8px">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
                <span style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;
                             color:#0b7b74;font-weight:600">{r['id']}</span>
                <span class="{cls}" style="font-size:0.72rem">{icon} {r['level']} · {r['score']}</span>
            </div>
            <div style="font-size:0.83rem;color:#374151;font-weight:500;margin-bottom:3px">{r['desc']}</div>
            <div style="font-size:0.75rem;color:#9ca3af">↳ {r['mitigation']}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── ROW 3: PHASE PROGRESS + BUDGET TABLE ──────────────────────────────────────
col_phase, col_budget = st.columns([1, 1.6])

with col_phase:
    st.markdown('<div class="section-title">📈 Phase Completion</div>', unsafe_allow_html=True)

    phase_summary = tasks.groupby("phase").agg(
        total=("id","count"), avg_pct=("pct","mean")
    ).reset_index()

    fig_phase = go.Figure()
    fig_phase.add_trace(go.Bar(
        x=phase_summary["avg_pct"] * 100,
        y=phase_summary["phase"],
        orientation='h',
        marker=dict(
            color=phase_summary["avg_pct"],
            colorscale=[[0,"#f1f5f9"],[0.5,"#0b7b74"],[1,"#0f1f3d"]],
            line=dict(width=0),
        ),
        text=[f"{v*100:.0f}%" for v in phase_summary["avg_pct"]],
        textposition='outside',
        textfont=dict(size=11, family="DM Sans"),
        hovertemplate="<b>%{y}</b><br>Avg Progress: %{x:.1f}%<extra></extra>",
    ))
    fig_phase.update_layout(
        height=280,
        margin=dict(l=0, r=50, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[0,120], showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, tickfont=dict(size=11)),
        showlegend=False,
        font=dict(family="DM Sans", color="#374151"),
    )
    st.plotly_chart(fig_phase, use_container_width=True, config={"displayModeBar": False})

    # Team workload
    st.markdown('<div class="section-title" style="margin-top:0.5rem">👥 Team Workload</div>', unsafe_allow_html=True)
    by_owner = tasks.groupby("owner").agg(tasks_count=("id","count"), avg_pct=("pct","mean")).reset_index()
    for _, r in by_owner.iterrows():
        bar_w = int(r["avg_pct"] * 100)
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
            <div style="width:36px;height:36px;border-radius:50%;
                        background:linear-gradient(135deg,#0b7b74,#0f1f3d);
                        display:flex;align-items:center;justify-content:center;
                        color:white;font-weight:700;font-size:0.85rem;flex-shrink:0">
                {r['owner'][0]}
            </div>
            <div style="flex:1">
                <div style="display:flex;justify-content:space-between;font-size:0.82rem;margin-bottom:4px">
                    <span style="font-weight:500;color:#374151">{r['owner']}</span>
                    <span style="color:#6b7280">{r['tasks_count']} tasks · {bar_w}%</span>
                </div>
                <div class="progress-outer">
                    <div class="progress-inner" style="width:{bar_w}%"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_budget:
    st.markdown('<div class="section-title">💳 Budget Ledger</div>', unsafe_allow_html=True)

    status_budget_badge = {
        "Paid":    '<span class="badge badge-done">Paid</span>',
        "Partial": '<span class="badge badge-partial">Partial</span>',
        "Pending": '<span class="badge badge-high">Pending</span>',
    }

    budget_rows = ""
    for _, r in budget.iterrows():
        var = r["actual"] - r["estimated"]
        var_color = "#c0392b" if var > 0 else "#1a7a4a"
        var_str   = f"+${var:,.0f}" if var > 0 else f"-${abs(var):,.0f}" if var < 0 else "$0"
        budget_rows += f"""
        <tr>
            <td style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#0b7b74;font-weight:600">{r['id']}</td>
            <td><span class="badge badge-pending" style="font-size:0.68rem">{r['category']}</span></td>
            <td style="font-weight:500">{r['desc']}</td>
            <td style="text-align:right;font-family:'JetBrains Mono',monospace">${r['estimated']:,.0f}</td>
            <td style="text-align:right;font-family:'JetBrains Mono',monospace">${r['actual']:,.0f}</td>
            <td style="text-align:right;font-family:'JetBrains Mono',monospace;color:{var_color};font-weight:700">{var_str}</td>
            <td>{status_budget_badge.get(r['status'],'')}</td>
        </tr>"""

    # Totals row
    total_var = total_spent - total_budget
    var_color_total = "#c0392b" if total_var > 0 else "#1a7a4a"
    var_str_total   = f"+${total_var:,.0f}" if total_var > 0 else f"-${abs(total_var):,.0f}"
    budget_rows += f"""
    <tr style="border-top:2px solid #0f1f3d">
        <td colspan="3" style="font-weight:700;color:#0f1f3d;font-size:0.88rem">TOTAL</td>
        <td style="text-align:right;font-family:'JetBrains Mono',monospace;font-weight:700">${total_budget:,.0f}</td>
        <td style="text-align:right;font-family:'JetBrains Mono',monospace;font-weight:700">${total_spent:,.0f}</td>
        <td style="text-align:right;font-family:'JetBrains Mono',monospace;font-weight:700;color:{var_color_total}">{var_str_total}</td>
        <td></td>
    </tr>"""

    st.markdown(f"""
    <div style="overflow-x:auto">
    <table class="styled-table">
        <thead><tr>
            <th>ID</th><th>Category</th><th>Description</th>
            <th style="text-align:right">Estimated</th>
            <th style="text-align:right">Actual</th>
            <th style="text-align:right">Variance</th>
            <th>Status</th>
        </tr></thead>
        <tbody>{budget_rows}</tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="dash-footer">
    Built by <a href="https://rahmatsyawaludin.github.io/portfolio/" target="_blank">Rahmat Syawaludin</a>
    &nbsp;·&nbsp;
    <a href="https://pewter-washer-791.notion.site/Community-Based-Offline-Learning-Companion-App-28c46416af218007b7aedb724117a71d" target="_blank">Project Notion Page</a>
    &nbsp;·&nbsp; PM Portfolio · Community-Based Offline Learning Companion App
    &nbsp;·&nbsp; Dashboard refreshed {datetime.now().strftime('%d %b %Y, %H:%M')}
</div>
""", unsafe_allow_html=True)
