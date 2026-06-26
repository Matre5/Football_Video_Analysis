import streamlit as st
import pandas as pd
import json
from collections import defaultdict
import matplotlib.pyplot as plt

st.set_page_config(page_title="Match Performance Dashboard", layout="wide")

MAX_HUMAN_SPEED = 12.4  # same noise cap used in sprint_detection.py

@st.cache_data
def load_data():
    with open("1st_Half/tracks_speed.json") as f: speed_data = json.load(f)
    with open("1st_Half/active_time.json") as f: active_data = json.load(f)
    with open("1st_Half/heatmaps_pitch.json") as f: heatmap_data = json.load(f)
    with open("1st_Half/sprints.json") as f: sprint_data = json.load(f)
    with open("1st_Half/fatigue_results.json") as f: fatigue_data = json.load(f)
    return speed_data, active_data, heatmap_data, sprint_data, fatigue_data

speed_data, active_data, heatmap_data, sprint_data, fatigue_data = load_data()

by_id = defaultdict(list)
for d in speed_data:
    by_id[d["id"]].append(d)

def clean_speeds(records):
    return [r["speed_mps"] for r in records if r["speed_mps"] <= MAX_HUMAN_SPEED]

sprint_counts = defaultdict(int)
for s in sprint_data:
    sprint_counts[s["id"]] += 1

fatigue_by_id = {f["id"]: f for f in fatigue_data}
active_by_id = {a["id"]: a for a in active_data}

summary_rows = []
for pid, records in by_id.items():
    total_distance = sum(r["distance_m"] for r in records)
    speeds = clean_speeds(records)
    avg_speed = sum(speeds) / len(speeds) if speeds else 0
    max_speed = max(speeds) if speeds else 0
    active = active_by_id.get(pid, {})
    fatigue = fatigue_by_id.get(pid, {})

    summary_rows.append({
        "Player ID": pid,
        "Active %": active.get("pct_active", 0),
        "Distance (m)": round(total_distance, 1),
        "Avg Speed (m/s)": round(avg_speed, 2),
        "Max Speed (m/s)": round(max_speed, 2),
        "Sprints": sprint_counts.get(pid, 0),
        "Intensity Drop %": fatigue.get("speed_decline_percent"),
        "Risk Flag": "🔴 Elevated" if fatigue.get("observed_intensity_drop") else
                     ("🟢 Normal" if pid in fatigue_by_id else "⚪ Not enough data"),
        "Confidence": fatigue.get("confidence", "n/a"),
    })

summary_df = pd.DataFrame(summary_rows).sort_values("Distance (m)", ascending=False)

st.title("⚽ Match Performance Dashboard")
st.caption("Crystal Palace 1 – 2 Arsenal · First Half · eSteps / Mitus.AI Technical Assessment")

tab1, tab2 = st.tabs(["Team Overview", "Player Detail"])

with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Players Tracked", len(summary_df))
    col2.metric("Evaluated for Fatigue", len(fatigue_data))
    col3.metric("Elevated Risk Flags", sum(1 for f in fatigue_data if f["observed_intensity_drop"]))

    st.subheader("All Tracked Players")
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.subheader("Top 10 by Observed Distance Covered")
    st.bar_chart(summary_df.head(10).set_index("Player ID")["Distance (m)"])

with tab2:
    player_ids = sorted(by_id.keys())
    selected = st.selectbox("Tracked Player ID", player_ids)

    records = sorted(by_id[selected], key=lambda r: r["frame"])
    speeds = clean_speeds(records)
    active = active_by_id.get(selected, {})
    fatigue = fatigue_by_id.get(selected)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Observed Distance Covered", f"{sum(r['distance_m'] for r in records):.1f} m")
    c2.metric("Avg Speed", f"{(sum(speeds)/len(speeds) if speeds else 0):.2f} m/s")
    c3.metric("Active Time", f"{active.get('pct_active', 0):.1f}%")
    c4.metric("Sprints", sprint_counts.get(selected, 0))

    st.subheader("Fatigue Indicator")
    if fatigue:
        f1, f2, f3 = st.columns(3)
        f1.metric("Early Avg Speed", f"{fatigue['early_avg_speed_mps']} m/s")
        f2.metric("Late Avg Speed", f"{fatigue['late_avg_speed_mps']} m/s")
        f3.metric("Intensity Drop", f"{fatigue['speed_decline_percent']}%")
        if fatigue["observed_intensity_drop"]:
            st.warning(f"⚠️ Elevated intensity drop (confidence: {fatigue['confidence']})")
        else:
            st.success(f"No significant drop (confidence: {fatigue['confidence']})")
    else:
        st.info("Not enough tracked data for this player to evaluate fatigue.")

    st.subheader("Speed Over Time")
    chart_df = pd.DataFrame({
        "Minute": [r["frame"] / 25 / 60 for r in records],
        "Speed (m/s)": [min(r["speed_mps"], MAX_HUMAN_SPEED) for r in records],
    })
    st.line_chart(chart_df.set_index("Minute"))

    st.subheader("Pitch Heatmap")
    grid = heatmap_data.get(str(selected))
    if grid:
        fig, ax = plt.subplots(figsize=(10,6))
        ax.imshow(grid, cmap="hot", interpolation="nearest")
        ax.set_xticks([]); ax.set_yticks([])
        st.pyplot(fig)
    else:
        st.info("No heatmap data for this player.")