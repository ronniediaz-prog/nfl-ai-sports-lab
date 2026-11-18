
import streamlit as st
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="NFL AI Sports Lab",
    page_icon="🏈",
    layout="wide"
)

# -----------------------------
# NFL AI SPORTS LAB VERSION 3.0
# -----------------------------

st.title("🏈 NFL AI SPORTS LAB")
st.subheader("Advanced NFL Research & Prediction Center")
st.success("Dashboard Version 3.0 — Development Edition")

st.info(
    "Research platform: manually entered projections are used "
    "until live NFL data integration is completed."
)

# Session storage
if "prediction_log" not in st.session_state:
    st.session_state.prediction_log = []

if "prop_log" not in st.session_state:
    st.session_state.prop_log = []

# Navigation
tabs = st.tabs([
    "📊 Matchups",
    "🏥 Injuries",
    "🎯 Predictions",
    "📈 Simulations",
    "👤 Player Props",
    "🎟️ Parlay Builder",
    "🔬 Research Center",
    "📋 Accuracy Tracker"
])

# -----------------------------
# MATCHUPS
# -----------------------------

with tabs[0]:
    st.header("Game Analysis")

    home = st.text_input("Home Team", "Houston Texans")
    away = st.text_input("Away Team", "Indianapolis Colts")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Home Team")
        home_off = st.number_input(
            "Home points scored per game", 0.0, 60.0, 25.0
        )
        home_def = st.number_input(
            "Home points allowed per game", 0.0, 60.0, 20.0
        )
        home_recent = st.number_input(
            "Home last 5 game average", 0.0, 60.0, 25.0
        )

    with col2:
        st.subheader("Away Team")
        away_off = st.number_input(
            "Away points scored per game", 0.0, 60.0, 23.0
        )
        away_def = st.number_input(
            "Away points allowed per game", 0.0, 60.0, 22.0
        )
        away_recent = st.number_input(
            "Away last 5 game average", 0.0, 60.0, 23.0
        )

    st.subheader("Game Research")
    st.write("Record additional matchup information.")

    weather = st.selectbox(
        "Weather conditions",
        ["Not entered", "Clear", "Rain", "Snow", "High wind", "Indoor"]
    )

    matchup_notes = st.text_area("Matchup notes")

# -----------------------------
# INJURIES
# -----------------------------

with tabs[1]:
    st.header("🏥 Injury Center")

    st.warning(
        "Injury information must be verified against current official reports."
    )

    home_injuries = st.text_area("Home team injury report")
    away_injuries = st.text_area("Away team injury report")

    qb_status = st.selectbox(
        "Quarterback availability",
        [
            "Both available",
            "Home QB questionable",
            "Away QB questionable",
            "Both questionable",
            "Home QB out",
            "Away QB out"
        ]
    )

    st.subheader("Player Availability")
    st.text_area("Important player absences and replacements")

# -----------------------------
# PREDICTIONS
# -----------------------------

with tabs[2]:
    st.header("🎯 Prediction Center")

    home_est = (home_off + away_def) / 2
    away_est = (away_off + home_def) / 2

    home_projection = home_est * 0.6 + home_recent * 0.4
    away_projection = away_est * 0.6 + away_recent * 0.4

    total_projection = home_projection + away_projection

    c1, c2, c3 = st.columns(3)

    c1.metric("Home projected points", round(home_projection, 1))
    c2.metric("Away projected points", round(away_projection, 1))
    c3.metric("Projected game total", round(total_projection, 1))

    if home_projection > away_projection:
        st.success(f"Model favors {home}")
    elif away_projection > home_projection:
        st.success(f"Model favors {away}")
    else:
        st.info("Model sees an even matchup.")

    total_line = st.number_input(
        "Game total betting line", 20.0, 80.0, 45.5
    )

    if total_projection > total_line:
        st.info("Preliminary projection leans OVER.")
    elif total_projection < total_line:
        st.info("Preliminary projection leans UNDER.")
    else:
        st.info("Projection matches the market line.")

    if st.button("Save Game Prediction"):
        st.session_state.prediction_log.append({
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Matchup": f"{away} @ {home}",
            "Projected Total": round(total_projection, 1),
            "Home Projection": round(home_projection, 1),
            "Away Projection": round(away_projection, 1),
            "Result": "Pending"
        })
        st.success("Prediction saved for this session.")

# -----------------------------
# GAME SIMULATIONS
# -----------------------------

with tabs[3]:
    st.header("📈 Advanced Game Simulations")

    sim_count = st.selectbox(
        "Simulation count",
        [10000, 50000, 100000],
        index=1
    )

    if st.button("Run Game Simulations"):
        home_scores = np.random.normal(
            home_projection, 10, sim_count
        )
        away_scores = np.random.normal(
            away_projection, 10, sim_count
        )

        home_wins = np.sum(home_scores > away_scores)
        away_wins = np.sum(away_scores > home_scores)
        ties = sim_count - home_wins - away_wins

        st.subheader("Simulation Results")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            f"{home} win frequency",
            f"{home_wins / sim_count * 100:.2f}%"
        )
        c2.metric(
            f"{away} win frequency",
            f"{away_wins / sim_count * 100:.2f}%"
        )
        c3.metric(
            "Tie frequency",
            f"{ties / sim_count * 100:.2f}%"
        )

        st.metric(
            "Average simulated total",
            round(np.mean(home_scores + away_scores), 1)
        )

        st.caption(
            "Simplified simulation, not a calibrated NFL forecasting model."
        )

# -----------------------------
# PLAYER PROPS CENTER
# -----------------------------

with tabs[4]:
    st.header("👤 NFL Player Props Research Center")

    st.success("50,000 simulations available per player prop.")

    st.write(
        "Analyze individual player performance using your "
        "verified statistics and projections."
    )

    player = st.text_input("Player name", "Enter player name")

    team = st.text_input("Player's team", "")

    position = st.selectbox(
        "Player position",
        ["QB", "RB", "WR", "TE", "Defense"]
    )

    prop_type = st.selectbox(
        "Player prop market",
        [
            "Passing Yards",
            "Passing Touchdowns",
            "Pass Completions",
            "Interceptions",
            "Rushing Yards",
            "Rushing Attempts",
            "Receiving Yards",
            "Receptions",
            "Receiving Touchdowns",
            "Rushing Touchdowns",
            "Sacks",
            "Tackles"
        ]
    )

    st.subheader("Player Statistics")

    c1, c2 = st.columns(2)

    with c1:
        last5 = st.number_input(
            "Last 5 games average", 0.0, 1000.0, 75.0
        )
        last10 = st.number_input(
            "Last 10 games average", 0.0, 1000.0, 75.0
        )

    with c2:
        season_avg = st.number_input(
            "Season average", 0.0, 1000.0, 75.0
        )
        projection = st.number_input(
            "Your projected player statistic",
            0.0, 1000.0, 80.0
        )

    prop_line = st.number_input(
        "Prop betting line", 0.0, 1000.0, 75.0
    )

    variation = st.number_input(
        "Expected game-to-game variation",
        0.1, 300.0, 20.0
    )

    st.subheader("Opportunity Research")

    snap_share = st.slider("Snap share (%)", 0, 100, 75)
    opportunity = st.text_area(
        "Targets, carries, workload and matchup notes"
    )

    st.caption(
        "Enter verified player statistics. These fields do not "
        "automatically retrieve live NFL information."
    )

    if st.button("Run 50,000 Player Prop Simulations"):

        rng = np.random.default_rng()

        samples = rng.normal(
            projection, variation, 50000
        )

        over = np.sum(samples > prop_line)
        under = np.sum(samples < prop_line)
        push = 50000 - over - under

        over_pct = over / 50000 * 100
        under_pct = under / 50000 * 100

        st.subheader("Player Prop Results")

        c1, c2, c3 = st.columns(3)

        c1.metric("OVER probability", f"{over_pct:.2f}%")
        c2.metric("UNDER probability", f"{under_pct:.2f}%")
        c3.metric("Push frequency", f"{push / 50000 * 100:.2f}%")

        st.metric(
            "Average simulated statistic",
            round(np.mean(samples), 2)
        )

        st.metric(
            "Percentage of last 5 average",
            round(last5, 1)
        )

        if over_pct > under_pct:
            st.success("Simulation leans OVER.")
        elif under_pct > over_pct:
            st.info("Simulation leans UNDER.")
        else:
            st.warning("No clear simulation advantage.")

        st.session_state.prop_log.append({
            "Player": player,
            "Team": team,
            "Position": position,
            "Market": prop_type,
            "Line": prop_line,
            "Projection": projection,
            "Over %": round(over_pct, 2),
            "Under %": round(under_pct, 2),
            "Last 5": last5,
            "Last 10": last10,
            "Season Average": season_avg
        })

        st.success("Player prop research saved for this session.")

        st.caption(
            "These are model estimates based on entered assumptions, "
            "not verified betting probabilities."
        )

# -----------------------------
# PARLAY BUILDER
# -----------------------------

with tabs[5]:
    st.header("🎟️ AI Parlay Builder")

    st.write(
        "Build a research shortlist from your saved player prop analyses."
    )

    if st.session_state.prop_log:
        props = st.session_state.prop_log

        st.dataframe(props, use_container_width=True)

        st.subheader("Combined Probability Estimate")

        selections = st.multiselect(
            "Choose player prop legs",
            list(range(len(props))),
            format_func=lambda i: (
                f"{props[i]['Player']} — {props[i]['Market']}"
            )
        )

        if st.button("Calculate Parlay Probability"):
            if selections:
                probability = 1.0

                for i in selections:
                    probability *= (
                        max(props[i]["Over %"], props[i]["Under %"]) / 100
                    )

                st.metric(
                    "Illustrative combined probability",
                    f"{probability * 100:.2f}%"
                )

                st.warning(
                    "This assumes independent selections and uses each "
                    "leg's stronger side. Actual combined probability "
                    "requires the chosen direction and correlation analysis."
                )
            else:
                st.warning("Select at least one leg.")
    else:
        st.info("Run player prop research to populate this section.")

# -----------------------------
# RESEARCH CENTER
# -----------------------------

with tabs[6]:
    st.header("🔬 Advanced Research Center")

    st.subheader("Player Matchup Analyzer")
    st.text_area("Opponent defensive matchup notes")

    st.subheader("Player Usage Tracker")
    st.write(
        "Track targets, carries, receptions, snap share, "
        "red-zone touches and workload."
    )

    st.subheader("Weather Impact Analyzer")
    st.selectbox(
        "Game environment",
        ["Not entered", "Indoor", "Clear", "Rain", "Snow", "High wind"]
    )

    st.subheader("Historical Matchup Research")
    st.text_area("Previous meetings and historical performance")

    st.subheader("First Half / Second Half Research")
    st.text_area("First-half and second-half projections")

    st.subheader("AI Research Assistant")
    research_question = st.text_area(
        "What would you like to research?"
    )

    if st.button("Prepare Research Request"):
        if research_question:
            st.info(
                "Research request saved for analysis. "
                "Automated AI research integration is a future upgrade."
            )

# -----------------------------
# ACCURACY TRACKER
# -----------------------------

with tabs[7]:
    st.header("📋 Prediction Accuracy Tracker")

    st.subheader("Saved Game Predictions")

    if st.session_state.prediction_log:
        st.dataframe(
            st.session_state.prediction_log,
            use_container_width=True
        )
    else:
        st.info("No saved game predictions yet.")

    st.subheader("Saved Player Prop Research")

    if st.session_state.prop_log:
        st.dataframe(
            st.session_state.prop_log,
            use_container_width=True
        )
    else:
        st.info("No saved player prop analyses yet.")

    st.caption(
        "Current records are session-based. Permanent history "
        "and automatic grading will be added in a later upgrade."
    )

# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.header("Research Checklist")

tasks = [
    "Verify official injury reports",
    "Confirm starting quarterbacks",
    "Review last 5 games",
    "Review last 10 games",
    "Compare offensive rankings",
    "Compare defensive rankings",
    "Check player usage and workload",
    "Analyze player matchups",
    "Check weather conditions",
    "Review betting lines",
    "Verify final starting lineups"
]

for task in tasks:
    st.checkbox(task)

st.caption(
    "NFL AI Sports Lab Version 3.0 | Research first. Bet responsibly."
)
