import streamlit as st
import plotly.graph_objects as go
import random

st.set_page_config(
    page_title="Dad Analytics™",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

if "achievement" not in st.session_state:
    st.session_state.achievement = ""

# -----------------------------
# Helper Functions
# -----------------------------

def calculate_score(gaming, tv, nap, work):

    productive = work * 10

    distractions = (
        gaming * 6 +
        tv * 5 +
        nap * 3
    )

    score = 10 + productive - distractions

    return max(0, min(100, round(score)))


def get_rank(score):

    if score >= 90:
        return "🏆 Productivity Legend"

    elif score >= 75:
        return "😌 Responsible Adult"

    elif score >= 50:
        return "📋 Average Human"

    elif score >= 25:
        return "🛋️ Senior Leisure Engineer"

    else:
        return "👑 Chief Sofa Officer"


def get_review(score):

    if score >= 75:
        return """
### Excellent Performance

Management is pleased to report that meaningful productive activity was detected.

**Strengths**
- Demonstrated initiative
- Limited entertainment dependency
- Positive contribution to society

**Recommendation**
Continue current operations.
"""

    elif score >= 40:
        return """
### Mixed Results

A balanced day with some evidence of productivity.

**Strengths**
- Remained conscious for extended periods
- Occasionally interacted with reality

**Areas for Improvement**
- Entertainment consumption remains elevated
- Productivity could be more consistent

**Recommendation**
Attempt to outperform the television tomorrow.
"""
    elif score <= 10:
        return """
### Audit Failure

Management was unable to verify any meaningful activity.

The employee appears to have spent the day
optimizing leisure operations.

Recommendation:
Try doing literally anything tomorrow.
"""

    else:
        return """
### Critical Productivity Event

Management found little evidence of productive activity.

**Strengths**
- Exceptional leisure consistency
- Strong sofa engagement metrics

**Areas for Improvement**
- Work

**Recommendation**
Please locate reality and interact with it.
"""


ACHIEVEMENTS = [
    "🛋️ Achievement Unlocked: Professional Sofa Occupant",
    "🎮 Achievement Unlocked: Controller Commander",
    "📺 Achievement Unlocked: Television Operations Director",
    "😴 Achievement Unlocked: Executive Nap Strategist",
    "👑 Achievement Unlocked: Chief Leisure Architect"
]

# -----------------------------
# Header
# -----------------------------

st.title("📊 Dad Analytics™")
st.caption("Daily Performance Review Dashboard")

st.divider()

# -----------------------------
# Inputs
# -----------------------------

col1, col2 = st.columns(2)

with col1:

    gaming_hours = st.slider(
        "🎮 Strategic Gaming Operations",
        0.0, 12.0, 0.0, 0.5
    )

    tv_hours = st.slider(
        "📺 Television Research",
        0.0, 12.0, 0.0, 0.5
    )

with col2:

    nap_hours = st.slider(
        "😴 Scheduled Maintenance",
        0.0, 8.0, 0.0, 0.5
    )

    work_hours = st.slider(
        "💼 Actual Work (if any)",
        0.0, 12.0, 0.0, 0.5
    )

st.divider()

# -----------------------------
# Analyze Button
# -----------------------------

if st.button("🔍 Analyze Performance", use_container_width=True):

    st.session_state.analyzed = True
    st.session_state.achievement = random.choice(ACHIEVEMENTS)

# -----------------------------
# Dashboard
# -----------------------------

if st.session_state.analyzed:

    score = calculate_score(
        gaming_hours,
        tv_hours,
        nap_hours,
        work_hours
    )

    rank = get_rank(score)
    total_activity = (
        gaming_hours +
        tv_hours +
        nap_hours +
        work_hours
    )

    if total_activity == 0:

        st.error("🚨 Audit Failure")

        st.markdown("""
        ## Too Lazy To Make The Input?

        Management requested activity data.

        No activity data was provided.

        After careful review, we have concluded
        that the employee was too lazy to even
        complete the audit form.

        Please move at least one slider.
        """)

        st.stop()
    # KPI Cards

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric("Productivity Score", f"{score}/100")

    with k2:
        st.metric("TV Hours", tv_hours)

    with k3:
        st.metric("Gaming Hours", gaming_hours)

    with k4:
        st.metric("Work Hours", work_hours)

    st.divider()

    # Gauge

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "Productivity Index"},
        gauge={
            "axis": {"range": [0, 100]},
            "steps": [
                {"range": [0, 30], "color": "lightcoral"},
                {"range": [30, 70], "color": "khaki"},
                {"range": [70, 100], "color": "lightgreen"},
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    # Classification

    st.subheader("🏅 Employee Classification")
    st.success(rank)

    # Review

    st.subheader("📋 Corporate Performance Review")
    st.markdown(get_review(score))

    # KPIs

    st.subheader("📈 Key Performance Indicators")

    sofa_rate = min(
        100,
        round(
            ((gaming_hours + tv_hours + nap_hours) / 24) * 100
        )
    )

    reality_rate = min(
        100,
        round((work_hours / 12) * 100)
    )

    st.write(f"🛋️ Sofa Occupancy Rate: **{sofa_rate}%**")
    st.write(f"🌎 Reality Interaction Rate: **{reality_rate}%**")
    st.write(f"📺 Entertainment Consumption: **{gaming_hours + tv_hours:.1f} hrs**")

    st.divider()

    # Achievement

    st.subheader("🎖 Achievement")
    st.info(st.session_state.achievement)

    # Excuse Generator

    st.subheader("📝 Official Justification")

    if st.button("Generate Excuse"):

        excuses = [
            f"The {gaming_hours:.1f} hours of gaming were dedicated to advanced leadership training.",
            f"The {tv_hours:.1f} hours of television viewing constituted ongoing geopolitical research.",
            f"The {nap_hours:.1f} hour nap was scheduled infrastructure maintenance.",
            f"The {gaming_hours + tv_hours:.1f} hours of entertainment improved organizational morale.",
            "Productivity was intentionally deferred to preserve long-term sustainability.",
            "The sofa session was a strategic planning retreat."
        ]

        st.session_state.excuse = random.choice(excuses)

    if "excuse" in st.session_state:
        st.warning(st.session_state.excuse)

    st.divider()

    # Certificate

    st.subheader("📜 Certificate of Strategic Laziness")

    st.success(
f"""
🏅 CERTIFICATE OF COMPLETION

This certifies that today's activities were successfully optimized for maximum leisure.

Productivity Score: {score}/100

Rank: {rank}

Approved By:
Dad Analytics™ Performance Review Board
"""
)
