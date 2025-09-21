# app.py — Advanced Hello for Streamlit
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time
from datetime import datetime

# ---- Page setup ----
st.set_page_config(
    page_title="Hello • Streamlit Advanced",
    page_icon="✨",
    layout="wide"
)

# ---- Sidebar controls ----
st.sidebar.title("⚙️ Controls")
name = st.sidebar.text_input("Your name", value="Arindam Jaiman")
points = st.sidebar.slider("Data points (days)", 30, 365, 120, step=15)
noise = st.sidebar.slider("Noise level", 0.0, 1.0, 0.25, 0.05)
chart_type = st.sidebar.selectbox("Chart type", ["Line", "Area", "Bar"])
show_table = st.sidebar.checkbox("Show data table", value=True)

# Simple session counter
if "clicks" not in st.session_state:
    st.session_state.clicks = 0
if st.sidebar.button("Increment counter"):
    st.session_state.clicks += 1
st.sidebar.caption(f"Clicks this session: **{st.session_state.clicks}**")

# ---- Cached data generator ----
@st.cache_data(ttl=600, show_spinner=False)
def make_timeseries(periods: int, noise: float, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=periods)
    base = np.linspace(0, 3 * np.pi, periods)
    values = np.sin(base) + np.linspace(0, 0.5, periods) + rng.normal(0, noise, periods)
    return pd.DataFrame({"date": dates, "value": values.round(4)})

df = make_timeseries(points, noise)

# ---- Header ----
left, right = st.columns([3, 2], vertical_alignment="center")
with left:
    st.title(f"Hello, {name}! 👋")
    st.caption(
        "An advanced hello page: reactive controls, caching, charts, file upload, "
        "download, progress demo, and session state."
    )
with right:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    st.metric("UTC Time", now)
    if len(df) >= 2:
        delta = df["value"].iloc[-1] - df["value"].iloc[-2]
        st.metric("Latest Δ", f"{delta:+.3f}")

# ---- KPIs ----
k1, k2, k3, k4 = st.columns(4)
k1.metric("Points", f"{len(df):,}")
k2.metric("Mean", f"{df['value'].mean():.3f}")
k3.metric("Std Dev", f"{df['value'].std():.3f}")
k4.metric("Last Value", f"{df['value'].iloc[-1]:.3f}")

# ---- Tabs ----
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🧮 Interact", "📂 Data", "ℹ️ About"])

with tab1:
    # Altair chart with hover
    base = alt.Chart(df).encode(x="date:T", y="value:Q", tooltip=["date:T", "value:Q"])
    if chart_type == "Line":
        chart = base.mark_line(point=True)
    elif chart_type == "Area":
        chart = base.mark_area(opacity=0.5)
    else:
        chart = base.mark_bar()
    st.altair_chart(chart.interactive(), use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download sample CSV", csv, file_name="hello_timeseries.csv", mime="text/csv")

with tab2:
    st.subheader("Simulate a short task")
    if st.button("Run task"):
        status = st.empty()
        bar = st.progress(0)
        for i in range(25):
            time.sleep(0.04)
            bar.progress(int((i + 1) * 4))
            status.info(f"Working… step {i + 1}/25")
        status.success("Done!")
    st.write("Session clicks counter:", st.session_state.clicks)

with tab3:
    up = st.file_uploader("Upload a CSV to preview", type=["csv"])
    if up is not None:
        user_df = pd.read_csv(up)
        st.success(f"Loaded {len(user_df):,} rows × {len(user_df.columns)} cols")
        st.dataframe(user_df.head(20), use_container_width=True)
        if "date" in user_df.columns:
            st.caption("Found a 'date' column—showing quick daily count.")
            quick = user_df["date"].astype("datetime64[ns]", errors="ignore")
            counts = pd.Series(1, index=quick).resample("D").count().rename("rows").reset_index()
            st.line_chart(counts, x="date", y="rows", use_container_width=True)
    else:
        st.info("No file uploaded. Showing the generated dataset below.")
        if show_table:
            st.dataframe(df, use_container_width=True)

with tab4:
    st.write(
        """
        **What you’re seeing**
        - `st.cache_data` to avoid recomputation
        - Session state (`st.session_state`) for a counter
        - Sidebar controls driving the UI
        - Altair charts with hover & zoom
        - File upload preview + quick chart
        - Download button for CSV
        """
    )
    st.code(
        "Tip: redeploy by editing and pushing this file. On Streamlit Cloud, builds pick up "
        "changes from `main` automatically when configured.",
        language="text",
    )
