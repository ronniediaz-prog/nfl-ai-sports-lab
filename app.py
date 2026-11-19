
import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="NFL AI Sports Lab",
    page_icon="🏈",
    layout="wide"
)

# ==================================================
# NFL AI SPORTS LAB VERSION 3.1
# ==================================================

st.title("🏈 NFL AI SPORTS LAB")
st.subheader("Advanced NFL Research & Prediction Center")
st.success("Dashboard Version 3.2 — Prediction Accuracy & Research")

st.info(
    "Player statistics are retrieved from nflverse when available. "
    "Always verify current statistics, injuries and lineups."
)

# ==================================================
# SESSION STORAGE
# ==================================================

if "prediction_log" not in st.session_state:
    st.session_state.prediction_log = []

if "prop_log" not in st.session_state:
    st.session_state.prop_log = []

# ==================================================
# LIVE NFL PLAYER DATA
# ==================================================

@st.cache_data(ttl=3600)
def load_nfl_player_stats():

    season = datetime.now().year

    url = (
        "https://github.com/nflverse/nflverse-data/"
        "releases/download/stats_player/"
        f"stats_player_week_{season}.csv"
    )

    try:
        data = pd.read_csv(url)

        required_columns = [
            "player_display_name",
            "position",
            "team",
            "season",
            "week",
            "season_type"
        ]

        for column in required_columns:
            if column not in data.columns:
                raise ValueError(
                    f"Missing required column: {column}"
                )

        data = data[
            (data["season"] == season) &
            (data["season_type"] == "REG") &
            (data["week"] > 0)
        ].copy()

        data = data.dropna(
            subset=["player_display_name"]
        )

        data["week"] = pd.to_numeric(
            data["week"], errors="coerce"
        )

        data = data.dropna(subset=["week"])

        return data

    except Exception as error:
        st.warning(
            f"Live player data is temporarily unavailable: {error}"
        )
        return pd.DataFrame()


# Load player data
with st.spinner("Connecting to NFL player statistics..."):
    nfl_data = load_nfl_player_stats()

if not nfl_data.empty:
    st.success(
        f"Live player statistics connected: "
        f"{nfl_data['player_display_name'].nunique()} players found."
    )
else:
    st.warning(
        "Manual research mode is available while the live data "
        "connection is unavailable."
    )

# ==================================================
# PLAYER PROP STAT MAPPING
# ==================================================

STAT_COLUMNS = {
    "Passing Yards": "passing_yards",
    "Passing Touchdowns": "passing_tds",
    "Pass Completions": "completions",
    "Interceptions": "passing_interceptions",
    "Rushing Yards": "rushing_yards",
    "Rushing Attempts": "carries",
    "Receiving Yards": "receiving_yards",
    "Receptions": "receptions",
    "Receiving Touchdowns": "receiving_tds",
    "Rushing Touchdowns": "rushing_tds",
    "Sacks": "sacks",
    "Tackles": "def_tackles"
}


def get_player_averages(player_rows, stat_column):

    if stat_column not in player_rows.columns:
        return None, None, None

    games = player_rows.sort_values("week").copy()

    games[stat_column] = pd.to_numeric(
        games[stat_column], errors="coerce"
    ).fillna(0)

    values = games[stat_column]

    if len(values) == 0:
        return None, None, None

    last5 = float(values.tail(5).mean())
    last10 = float(values.tail(10).mean())
    season_average = float(values.mean())

    return last5, last10, season_average


# ==================================================
# NAVIGATION
# ==================================================

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

# ==================================================
# MATCHUPS
# ==================================================

with tabs[0]:

    st.header("📊 Game Analysis")

    home = st.text_input(
        "Home Team", "Houston Texans"
    )

    away = st.text_input(
        "Away Team", "Indianapolis Colts"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Home Team")

        home_off = st.number_input(
            "Home points scored per game",
            0.0, 60.0, 25.0
        )

        home_def = st.number_input(
            "Home points allowed per game",
            0.0, 60.0, 20.0
        )

        home_recent = st.number_input(
            "Home last 5 game average",
            0.0, 60.0, 25.0
        )

    with col2:
        st.subheader("Away Team")

        away_off = st.number_input(
            "Away points scored per game",
            0.0, 60.0, 23.0
        )

        away_def = st.number_input(
            "Away points allowed per game",
            0.0, 60.0, 22.0
        )

        away_recent = st.number_input(
            "Away last 5 game average",
            0.0, 60.0, 23.0
        )

    st.subheader("Game Research")

    weather = st.selectbox(
        "Weather conditions",
        [
            "Not entered",
            "Clear",
            "Rain",
            "Snow",
            "High wind",
            "Indoor"
        ]
    )

    matchup_notes = st.text_area("Matchup notes")


# ==================================================
# INJURIES
# ==================================================

with tabs[1]:

    st.header("🏥 Injury Center")

    st.warning(
        "Verify injury information against official NFL reports."
    )

    home_injuries = st.text_area(
        "Home team injury report"
    )

    away_injuries = st.text_area(
        "Away team injury report"
    )

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

    st.text_area(
        "Important player absences and replacements"
    )


# ==================================================
# PREDICTIONS
# ==================================================

with tabs[2]:

    st.header("🎯 Prediction Center")

    home_est = (home_off + away_def) / 2
    away_est = (away_off + home_def) / 2

    home_projection = (
        home_est * 0.6 + home_recent * 0.4
    )

    away_projection = (
        away_est * 0.6 + away_recent * 0.4
    )

    total_projection = (
        home_projection + away_projection
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Home projected points",
        round(home_projection, 1)
    )

    c2.metric(
        "Away projected points",
        round(away_projection, 1)
    )

    c3.metric(
        "Projected game total",
        round(total_projection, 1)
    )

    if home_projection > away_projection:
        st.success(f"Model favors {home}")

    elif away_projection > home_projection:
        st.success(f"Model favors {away}")

    else:
        st.info("Model sees an even matchup.")

    total_line = st.number_input(
        "Game total betting line",
        20.0, 80.0, 45.5
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


# ==================================================
# GAME SIMULATIONS
# ==================================================

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

        home_wins = np.sum(
            home_scores > away_scores
        )

        away_wins = np.sum(
            away_scores > home_scores
        )

        ties = (
            sim_count - home_wins - away_wins
        )

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
            "Simplified simulation, not a calibrated NFL model."
        )


# ==================================================
# PLAYER PROPS CENTER - VERSION 3.1
# ==================================================

with tabs[4]:

    st.header("👤 NFL Player Props Research Center")

    st.success(
        "50,000 simulations available per player prop."
    )

    st.write(
        "Search NFL players and retrieve available weekly statistics."
    )

    player_rows = pd.DataFrame()

    live_player_selected = False

    if not nfl_data.empty:

        player_names = sorted(
            nfl_data["player_display_name"]
            .dropna()
            .unique()
            .tolist()
        )

        player_options = ["Enter manually"] + player_names

        selected_player = st.selectbox(
            "Search NFL player",
            player_options
        )

        if selected_player != "Enter manually":

            player_rows = nfl_data[
                nfl_data["player_display_name"] == selected_player
            ].copy()

            player_rows = player_rows.sort_values("week")

            player = selected_player

            live_player_selected = True

            latest_team = player_rows.iloc[-1]["team"]
            latest_position = player_rows.iloc[-1]["position"]

            st.success(
                f"Player found: {player} | "
                f"Team: {latest_team} | "
                f"Position: {latest_position}"
            )

        else:
            player = st.text_input(
                "Enter player name",
                "Jonathan Taylor"
            )

    else:

        player = st.text_input(
            "Player name",
            "Jonathan Taylor"
        )

    if live_player_selected:

        team = str(latest_team)

        position = str(latest_position)

        st.text_input(
            "Player's team",
            value=team,
            disabled=True
        )

        st.text_input(
            "Player position",
            value=position,
            disabled=True
        )

    else:

        team = st.text_input(
            "Player's team",
            ""
        )

        position = st.selectbox(
            "Player position",
            ["QB", "RB", "WR", "TE", "Defense"]
        )

    prop_type = st.selectbox(
        "Player prop market",
        list(STAT_COLUMNS.keys())
    )

    stat_column = STAT_COLUMNS[prop_type]

    auto_last5 = 0.0
    auto_last10 = 0.0
    auto_season = 0.0

    stats_available = False

    if live_player_selected:

        auto_last5, auto_last10, auto_season = (
            get_player_averages(
                player_rows,
                stat_column
            )
        )

        if auto_last5 is not None:

            stats_available = True

            st.success(
                "Live statistics loaded for this player and market."
            )

            st.write(
                f"Latest games available: {len(player_rows)}"
            )

        else:

            st.warning(
                f"The live data does not contain the "
                f"'{stat_column}' statistic for this market. "
                "Enter verified values manually."
            )

    st.subheader("Player Statistics")

    if stats_available:

        default_last5 = auto_last5
        default_last10 = auto_last10
        default_season = auto_season

    else:

        default_last5 = 0.0
        default_last10 = 0.0
        default_season = 0.0

    c1, c2 = st.columns(2)

    with c1:

        last5 = st.number_input(
            "Last 5 games average",
            min_value=0.0,
            max_value=1000.0,
            value=float(default_last5),
            key="prop_last5"
        )

        last10 = st.number_input(
            "Last 10 games average",
            min_value=0.0,
            max_value=1000.0,
            value=float(default_last10),
            key="prop_last10"
        )

    with c2:

        season_avg = st.number_input(
            "Season average",
            min_value=0.0,
            max_value=1000.0,
            value=float(default_season),
            key="prop_season"
        )

        projection = st.number_input(
            "Your projected player statistic",
            min_value=0.0,
            max_value=1000.0,
            value=float(default_last5 if stats_available else 0.0),
            key="prop_projection"
        )

    prop_line = st.number_input(
        "Prop betting line",
        min_value=0.0,
        max_value=1000.0,
        value=float(default_last5 if stats_available else 0.0),
        key="prop_line"
    )

    variation = st.number_input(
        "Expected game-to-game variation",
        min_value=0.1,
        max_value=300.0,
        value=20.0
    )

    st.subheader("Opportunity Research")

    snap_share = st.slider(
        "Snap share (%)",
        0,
        100,
        75
    )

    opportunity = st.text_area(
        "Targets, carries, workload and matchup notes"
    )

    if stats_available:

        st.caption(
            "Historical averages were retrieved from nflverse. "
            "Verify the data and enter your own projection."
        )

    else:

        st.caption(
            "Manual entry mode. Verify all statistics before analysis."
        )

    if st.button("Run 50,000 Player Prop Simulations"):

        if not player.strip():

            st.error("Enter a player name first.")

        else:

            rng = np.random.default_rng()

            samples = rng.normal(
                projection,
                variation,
                50000
            )

            # Prevent impossible negative statistics
            samples = np.maximum(samples, 0)

            over = np.sum(samples > prop_line)
            under = np.sum(samples < prop_line)
            push = 50000 - over - under

            over_pct = over / 50000 * 100
            under_pct = under / 50000 * 100

            st.subheader("Player Prop Results")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "OVER probability",
                f"{over_pct:.2f}%"
            )

            c2.metric(
                "UNDER probability",
                f"{under_pct:.2f}%"
            )

            c3.metric(
                "Push frequency",
                f"{push / 50000 * 100:.2f}%"
            )

            st.metric(
                "Average simulated statistic",
                round(np.mean(samples), 2)
            )

            st.metric(
                "Last 5 game average",
                round(last5, 2)
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
                "Season Average": season_avg,
                "Data Source": (
                    "nflverse" if stats_available else "Manual"
                )
            })

            st.success(
                "Player prop research saved for this session."
            )

            st.caption(
                "Simulation estimates depend on your projection "
                "and variation. They are not verified betting odds."
            )


# ==================================================
# PARLAY BUILDER
# ==================================================

with tabs[5]:

    st.header("🎟️ AI Parlay Builder")

    st.write(
        "Build a research shortlist from saved player prop analyses."
    )

    if st.session_state.prop_log:

        props = st.session_state.prop_log

        st.dataframe(
            props,
            use_container_width=True
        )

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
                        max(
                            props[i]["Over %"],
                            props[i]["Under %"]
                        ) / 100
                    )

                st.metric(
                    "Illustrative combined probability",
                    f"{probability * 100:.2f}%"
                )

                st.warning(
                    "Illustrative only. This uses each leg's stronger "
                    "side and assumes independence. It does not account "
                    "for direction selection or correlated outcomes."
                )

            else:

                st.warning("Select at least one leg.")

    else:

        st.info(
            "Run player prop research to populate this section."
        )


# ==================================================
# RESEARCH CENTER
# ==================================================

with tabs[6]:

    st.header("🔬 Advanced Research Center")

    st.subheader("Player Matchup Analyzer")

    st.text_area(
        "Opponent defensive matchup notes"
    )

    st.subheader("Player Usage Tracker")

    st.write(
        "Track targets, carries, receptions, snap share, "
        "red-zone touches and workload."
    )

    st.subheader("Weather Impact Analyzer")

    st.selectbox(
        "Game environment",
        [
            "Not entered",
            "Indoor",
            "Clear",
            "Rain",
            "Snow",
            "High wind"
        ]
    )

    st.subheader("Historical Matchup Research")

    st.text_area(
        "Previous meetings and historical performance"
    )

    st.subheader("First Half / Second Half Research")

    st.text_area(
        "First-half and second-half projections"
    )

    st.subheader("AI Research Assistant")

   


    research_question = st.text_area(
        "What NFL matchup or player would you like to research?"
    )

    if st.button("Analyze Research Question"):

        if research_question.strip():

            st.info(
                "Research question saved. Verify current NFL "
                "statistics, injuries, starting lineups and "
                "betting lines before making a decision."
            )

            st.write("Your research question:")
            st.write(research_question)

        else:

            st.warning("Enter a research question first.")


# ==================================================
# ACCURACY TRACKER
# ==================================================



with tabs[7]:

    st.header("📋 Prediction Accuracy Tracker")

    if "accuracy_log" not in st.session_state:
        st.session_state.accuracy_log = []

    # SAVED GAME PREDICTIONS

    st.subheader("Saved Game Predictions")

    if st.session_state.prediction_log:

        st.dataframe(
            st.session_state.prediction_log,
            use_container_width=True
        )

    else:

        st.info("No game predictions have been saved yet.")

    st.divider()

    # SAVED PLAYER PROP RESEARCH

    st.subheader("Saved Player Prop Research")

    if st.session_state.prop_log:

        st.dataframe(
            st.session_state.prop_log,
            use_container_width=True
        )

    else:

        st.info("No player prop research has been saved yet.")

    st.divider()

    # RECORD PREDICTION RESULTS

    st.subheader("📝 Record Prediction Result")

    prediction_name = st.text_input(
        "Game or Player Name",
        key="accuracy_prediction_name"
    )

    prediction_type = st.selectbox(
        "Prediction Category",
        ["Game Prediction", "Player Prop"],
        key="accuracy_prediction_type"
    )

    prediction_result = st.selectbox(
        "Prediction Result",
        ["Correct", "Incorrect"],
        key="accuracy_prediction_result"
    )

    if st.button("Save Prediction Result"):

        if prediction_name.strip():

            st.session_state.accuracy_log.append({
                "prediction": prediction_name.strip(),
                "type": prediction_type,
                "result": prediction_result,
                "date": datetime.now().strftime("%Y-%m-%d")
            })

            st.success("Prediction result saved!")

        else:

            st.warning("Please enter a game or player name.")

    st.divider()

    # ACCURACY STATISTICS

    st.subheader("📊 Prediction Accuracy Statistics")

    if st.session_state.accuracy_log:

        accuracy_df = pd.DataFrame(
            st.session_state.accuracy_log
        )

        # SUPPORT OLDER RECORDS

        if "type" not in accuracy_df.columns:
            accuracy_df["type"] = "Game Prediction"

        if "result" not in accuracy_df.columns:
            accuracy_df["result"] = ""

        accuracy_df["type"] = (
            accuracy_df["type"].fillna("Game Prediction")
        )

        accuracy_df["result"] = (
            accuracy_df["result"].fillna("").astype(str)
        )

        # KEEP VALID RESULTS

        accuracy_df = accuracy_df[
            accuracy_df["result"].str.lower().isin(
                ["correct", "incorrect"]
            )
        ]

        # OVERALL PERFORMANCE

        total_predictions = len(accuracy_df)

        correct_predictions = (
            accuracy_df["result"].str.lower() == "correct"
        ).sum()

        incorrect_predictions = (
            accuracy_df["result"].str.lower() == "incorrect"
        ).sum()

        overall_accuracy = (
            correct_predictions / total_predictions * 100
            if total_predictions > 0 else 0
        )

        st.subheader("🏆 Overall Performance")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Predictions",
            total_predictions
        )

        col2.metric(
            "Correct",
            int(correct_predictions)
        )

        col3.metric(
            "Incorrect",
            int(incorrect_predictions)
        )

        col4.metric(
            "Overall Accuracy",
            f"{overall_accuracy:.1f}%"
        )

        st.divider()

        # GAME PREDICTION PERFORMANCE

        st.subheader("🏈 Game Prediction Performance")

        game_df = accuracy_df[
            accuracy_df["type"] == "Game Prediction"
        ]

        if not game_df.empty:

            game_total = len(game_df)

            game_correct = (
                game_df["result"].str.lower() == "correct"
            ).sum()

            game_incorrect = game_total - game_correct

            game_accuracy = (
                game_correct / game_total * 100
            )

            col1, col2, col3 = st.columns(3)

            col1.metric("Game Predictions", game_total)
            col2.metric("Correct", int(game_correct))
            col3.metric("Accuracy", f"{game_accuracy:.1f}%")

        else:

            st.info("No game prediction results recorded yet.")

        st.divider()

        # PLAYER PROP PERFORMANCE

        st.subheader("👤 Player Prop Performance")

        prop_df = accuracy_df[
            accuracy_df["type"] == "Player Prop"
        ]

        if not prop_df.empty:

            prop_total = len(prop_df)

            prop_correct = (
                prop_df["result"].str.lower() == "correct"
            ).sum()

            prop_incorrect = prop_total - prop_correct

            prop_accuracy = (
                prop_correct / prop_total * 100
            )

            col1, col2, col3 = st.columns(3)

            col1.metric("Player Props", prop_total)
            col2.metric("Correct", int(prop_correct))
            col3.metric("Accuracy", f"{prop_accuracy:.1f}%")

        else:

            st.info("No player prop results recorded yet.")

        st.divider()

        # RESULTS CHART

        st.subheader("📈 Prediction Results Chart")

        chart_df = pd.DataFrame({
            "Results": ["Correct", "Incorrect"],
            "Predictions": [
                int(correct_predictions),
                int(incorrect_predictions)
            ]
        })

        st.bar_chart(
            chart_df.set_index("Results")
        )

        st.divider()

        # COMPLETE HISTORY

        st.subheader("📚 Complete Prediction History")

        if not accuracy_df.empty:

            st.dataframe(
                accuracy_df,
                use_container_width=True
            )

        else:

            st.info(
                "No valid prediction results recorded yet."
            )

    else:

        st.info(
            "Record game predictions and player props "
            "to begin tracking accuracy."
        )

    st.caption(
        "Prediction accuracy is currently session-based. "
        "Permanent storage will be added in a future upgrade."
    )
