
import streamlit as st
import numpy as np

st.set_page_config(
    page_title="NFL AI Sports Lab",
    page_icon="🏈",
    layout="wide"
)

st.title("🏈 NFL AI SPORTS LAB")
st.subheader("Your Personal NFL Research Dashboard")
st.success("Dashboard Version 2.0 — Research Center")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Matchups",
    "🏥 Injuries",
    "🎯 Predictions",
    "📈 Simulations"
])

with tab1:
    st.header("Game Analysis")

    home = st.text_input("Home Team", "Houston Texans")
    away = st.text_input("Away Team", "Indianapolis Colts")

    st.subheader("Team Performance")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Home Team")
        home_off = st.number_input("Points scored per game", 0.0, 60.0, 25.0)
        home_def = st.number_input("Points allowed per game", 0.0, 60.0, 20.0)

    with col2:
        st.write("Away Team")
        away_off = st.number_input("Points scored per game", 0.0, 60.0, 23.0)
        away_def = st.number_input("Points allowed per game", 0.0, 60.0, 22.0)

    st.subheader("Recent Performance")
    st.write("Enter each team's average points from its last 5 games.")

    home_recent = st.number_input("Home last 5 average", 0.0, 60.0, 25.0)
    away_recent = st.number_input("Away last 5 average", 0.0, 60.0, 23.0)

with tab2:
    st.header("Injury Center")

    st.warning("Enter verified injury information manually for now.")

    st.subheader("Home Team")
    home_injuries = st.text_area("Home injury notes")

    st.subheader("Away Team")
    away_injuries = st.text_area("Away injury notes")

    st.subheader("Quarterback Status")
    qb_status = st.selectbox(
        "Starting QB availability",
        ["Both available", "Home QB questionable",
         "Away QB questionable", "Both questionable",
         "Home QB out", "Away QB out"]
    )

with tab3:
    st.header("Prediction Center")

    home_est = (home_off + away_def) / 2
    away_est = (away_off + home_def) / 2

    home_projection = (home_est * 0.6) + (home_recent * 0.4)
    away_projection = (away_est * 0.6) + (away_recent * 0.4)

    total_projection = home_projection + away_projection

    col1, col2, col3 = st.columns(3)

    col1.metric("Home projected points", round(home_projection, 1))
    col2.metric("Away projected points", round(away_projection, 1))
    col3.metric("Projected total", round(total_projection, 1))

    st.subheader("Moneyline Estimate")

    if home_projection > away_projection:
        st.write(f"Model favors **{home}**")
    elif away_projection > home_projection:
        st.write(f"Model favors **{away}**")
    else:
        st.write("Model sees an even matchup.")

    st.caption("These are preliminary estimates, not verified probabilities.")

    total_line = st.number_input("Kalshi game total line", 20.0, 80.0, 45.5)

    if total_projection > total_line:
        st.info("Model leans OVER")
    elif total_projection < total_line:
        st.info("Model leans UNDER")
    else:
        st.info("Model projection matches the line.")

with tab4:
    st.header("10,000 Game Simulations")

    st.write("Uses projected scores and a simplified scoring variation.")

    if st.button("Run 10,000 Simulations"):
        home_scores = np.random.normal(home_projection, 10, 10000)
        away_scores = np.random.normal(away_projection, 10, 10000)

        home_wins = np.sum(home_scores > away_scores)
        away_wins = np.sum(away_scores > home_scores)
        ties = 10000 - home_wins - away_wins

        st.metric(f"{home} win frequency", f"{home_wins / 100:.2f}%")
        st.metric(f"{away} win frequency", f"{away_wins / 100:.2f}%")
        st.metric("Tie frequency", f"{ties / 100:.2f}%")

        st.metric(
            "Average simulated total",
            round(np.mean(home_scores + away_scores), 1)
        )

st.divider()
st.header("Research Checklist")

tasks = [
    "Check latest injury reports",
    "Verify starting quarterbacks",
    "Analyze last 5 games",
    "Compare offensive rankings",
    "Compare defensive rankings",
    "Review current betting lines",
    "Confirm final starting lineups"
]

for task in tasks:
    st.checkbox(task)

st.caption("NFL AI Sports Lab | Research first. Bet responsibly.")
