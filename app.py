import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    day = pd.read_csv("day.csv")
    hour = pd.read_csv("hour.csv")
    day["dteday"] = pd.to_datetime(day["dteday"])
    hour["dteday"] = pd.to_datetime(hour["dteday"])
    hour["datetime"] = hour["dteday"] + pd.to_timedelta(hour["hr"], unit="h")


    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    weather_map = {
        1: "Clear/Few Clouds",
        2: "Mist/Cloudy",
        3: "Light Snow/Rain",
        4: "Heavy Rain/Snow"
    }
    weekday_map = {
        0: "Sunday",
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday"
    }

    for df in [day, hour]:
        df["year"] = df["yr"].map({0: 2011, 1: 2012})
        df["season_label"] = df["season"].map(season_map)
        df["weather_label"] = df["weathersit"].map(weather_map)
        df["weekday_label"] = df["weekday"].map(weekday_map)
        df["quarter"] = df["dteday"].dt.quarter
        df["temp_c"] = df["temp"] * 41
        df["humidity_pct"] = df["hum"] * 100
        df["casual_ratio"] = df["casual"] / df["cnt"]

    day["usage_category"] = pd.qcut(
        day["cnt"],
        q=3,
        labels=["Low Usage", "Medium Usage", "High Usage"]
    )

    return day, hour


day, hour = load_data()

# =========================
# HEADER
# =========================
st.title("🚲 Bike Sharing Interactive Dashboard")
st.write("Dashboard Interaktif Berdasarkan Project Analisis Bike Sharing Dataset.")

with st.expander("📌 Pertanyaan Bisnis Project"):
    st.markdown("""
    1. Faktor apa saja yang memengaruhi rendahnya penyewaan sepeda pada hari kerja selama musim panas tahun 2012?
    2. Pada kondisi apa proporsi pengguna casual melebihi 40% selama Q2 tahun 2012?
    3. Bagaimana perbedaan pola penyewaan casual dan registered berdasarkan jam penggunaan pada hari kerja tahun 2012?
    """)

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("🎛️ Filter Interaktif")

selected_year = st.sidebar.selectbox("Pilih Tahun", [2011, 2012], index=1)

selected_season = st.sidebar.multiselect(
    "Pilih Season",
    day["season_label"].unique(),
    default=day["season_label"].unique()
)

selected_weather = st.sidebar.multiselect(
    "Pilih Weather",
    day["weather_label"].unique(),
    default=day["weather_label"].unique()
)

filtered_day = day[
    (day["year"] == selected_year) &
    (day["season_label"].isin(selected_season)) &
    (day["weather_label"].isin(selected_weather))
]

filtered_hour = hour[
    (hour["year"] == selected_year) &
    (hour["season_label"].isin(selected_season)) &
    (hour["weather_label"].isin(selected_weather))
]

# =========================
# KPI
# =========================
st.subheader("📊 Key Performance Indicator")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Rental", f"{filtered_day['cnt'].sum():,}")
col2.metric("Rata-rata Harian", f"{filtered_day['cnt'].mean():.0f}")
col3.metric("Casual User", f"{filtered_day['casual'].sum():,}")
col4.metric("Registered User", f"{filtered_day['registered'].sum():,}")

st.divider()

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Q1 Demand Rendah",
    "Q2 Casual > 40%",
    "Q3 Casual vs Registered",
    "Usage Category"
])

# =========================
# OVERVIEW
# =========================
with tab1:
    st.subheader("📈 Trend Penyewaan Sepeda")

    agg = st.radio(
        "Pilih agregasi waktu",
        ["Daily", "Monthly"],
        horizontal=True
    )

    if agg == "Daily":
        trend = filtered_day.copy()
        trend["period"] = trend["dteday"]
    else:
        trend = filtered_day.copy()
        trend["period"] = trend["dteday"].dt.to_period("M").astype(str)

    trend_group = trend.groupby("period")[["cnt", "casual", "registered"]].sum().reset_index()

    fig = px.line(
        trend_group,
        x="period",
        y=["cnt", "casual", "registered"],
        markers=True,
        title="Trend Total Rental, Casual, dan Registered"
    )
    st.plotly_chart(fig, use_container_width=True)

    peak_hour = filtered_hour.groupby("hr")["cnt"].mean().idxmax()
    best_weather = filtered_day.groupby("weather_label")["cnt"].mean().idxmax()
    best_season = filtered_day.groupby("season_label")["cnt"].mean().idxmax()

    st.info(
        f"Key insight: peak hour terjadi sekitar jam {peak_hour}:00. "
        f"Season dengan rata-rata rental tertinggi adalah {best_season}, "
        f"dan cuaca terbaik adalah {best_weather}."
    )

# =========================
# Q1
# =========================
with tab2:
    st.subheader("❓ Q1: Faktor Demand Rendah pada Hari Kerja Summer 2012")

    q1 = day[
        (day["year"] == 2012) &
        (day["season_label"] == "Summer") &
        (day["workingday"] == 1)
    ].copy()

    threshold_type = st.selectbox(
        "Pilih threshold demand rendah",
        ["Rata-rata", "Median", "Custom"]
    )

    if threshold_type == "Rata-rata":
        threshold = q1["cnt"].mean()
    elif threshold_type == "Median":
        threshold = q1["cnt"].median()
    else:
        threshold = st.slider(
            "Atur threshold manual",
            int(q1["cnt"].min()),
            int(q1["cnt"].max()),
            int(q1["cnt"].mean())
        )

    q1["demand_status"] = q1["cnt"].apply(
        lambda x: "Low Demand" if x < threshold else "Normal/High Demand"
    )

    low_demand = q1[q1["demand_status"] == "Low Demand"]

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Hari Kerja Summer 2012", len(q1))
    c2.metric("Low Demand Days", len(low_demand))
    c3.metric("Threshold", f"{threshold:.0f}")

    col_a, col_b = st.columns(2)

    with col_a:
        fig1 = px.box(
            q1,
            x="weather_label",
            y="cnt",
            color="demand_status",
            points="all",
            title="Demand Berdasarkan Cuaca"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        fig2 = px.scatter(
            q1,
            x="temp_c",
            y="cnt",
            color="demand_status",
            size="humidity_pct",
            hover_data=["dteday", "weather_label"],
            title="Demand vs Suhu"
        )
        fig2.add_hline(y=threshold, line_dash="dash")
        st.plotly_chart(fig2, use_container_width=True)

    dominant_weather = low_demand["weather_label"].mode()[0]

    st.warning(
        f"Key insight: pada hari kerja Summer 2012, low demand paling sering terjadi "
        f"pada kondisi cuaca {dominant_weather}. Faktor cuaca dan suhu terlihat memengaruhi rendahnya jumlah rental."
    )

# =========================
# Q2
# =========================
with tab3:
    st.subheader("❓ Q2: Kondisi Casual User Melebihi 40% pada Q2 2012")

    threshold_ratio = st.slider(
        "Atur threshold casual ratio",
        0.1,
        0.8,
        0.4,
        0.05
    )

    q2 = hour[
        (hour["year"] == 2012) &
        (hour["quarter"] == 2)
    ].copy()

    q2["casual_status"] = q2["casual_ratio"].apply(
        lambda x: "Casual > Threshold" if x > threshold_ratio else "Normal"
    )

    high_casual = q2[q2["casual_ratio"] > threshold_ratio]

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Data Jam", len(q2))
    c2.metric("Casual > Threshold", len(high_casual))
    c3.metric("Persentase", f"{len(high_casual) / len(q2) * 100:.1f}%")

    col_a, col_b = st.columns(2)

    with col_a:
        ratio_hour = q2.groupby("hr")["casual_ratio"].mean().reset_index()

        fig3 = px.line(
            ratio_hour,
            x="hr",
            y="casual_ratio",
            markers=True,
            title="Rata-rata Casual Ratio per Jam"
        )
        fig3.add_hline(y=threshold_ratio, line_dash="dash")
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        ratio_day = q2.groupby("weekday_label")["casual_ratio"].mean().reset_index()

        fig4 = px.bar(
            ratio_day,
            x="weekday_label",
            y="casual_ratio",
            title="Casual Ratio Berdasarkan Hari"
        )
        fig4.add_hline(y=threshold_ratio, line_dash="dash")
        st.plotly_chart(fig4, use_container_width=True)

    heatmap = q2.groupby(["weekday_label", "hr"])["casual_ratio"].mean().reset_index()
    heatmap_pivot = heatmap.pivot(
        index="weekday_label",
        columns="hr",
        values="casual_ratio"
    )

    fig5 = px.imshow(
        heatmap_pivot,
        aspect="auto",
        title="Heatmap Casual Ratio berdasarkan Hari dan Jam"
    )
    st.plotly_chart(fig5, use_container_width=True)

    top_hour = high_casual["hr"].mode()[0]
    top_day = high_casual["weekday_label"].mode()[0]
    top_weather = high_casual["weather_label"].mode()[0]

    st.info(
        f"Key insight: casual ratio di atas {threshold_ratio:.0%} paling sering terjadi "
        f"pada jam {top_hour}:00, hari {top_day}, dengan cuaca {top_weather}."
    )

# =========================
# Q3
# =========================
with tab4:
    st.subheader("❓ Q3: Perbedaan Pola Casual dan Registered pada Hari Kerja 2012")

    day_type = st.radio(
        "Pilih tipe hari",
        ["Working Day", "Non-working Day", "All"],
        horizontal=True
    )

    q3 = hour[hour["year"] == 2012].copy()

    if day_type == "Working Day":
        q3 = q3[q3["workingday"] == 1]
    elif day_type == "Non-working Day":
        q3 = q3[q3["workingday"] == 0]

    hourly_pattern = q3.groupby("hr")[["casual", "registered"]].mean().reset_index()

    fig6 = px.line(
        hourly_pattern,
        x="hr",
        y=["casual", "registered"],
        markers=True,
        title="Pola Casual vs Registered per Jam"
    )
    st.plotly_chart(fig6, use_container_width=True)

    casual_peak = hourly_pattern.loc[hourly_pattern["casual"].idxmax(), "hr"]
    registered_peak = hourly_pattern.loc[hourly_pattern["registered"].idxmax(), "hr"]

    st.success(
        f"Key insight: casual user mencapai puncak pada jam {casual_peak}:00, "
        f"sedangkan registered user mencapai puncak pada jam {registered_peak}:00. "
        f"Ini menunjukkan registered user cenderung punya pola penggunaan rutin."
    )

    st.dataframe(hourly_pattern, use_container_width=True)

# =========================
# USAGE CATEGORY
# =========================
with tab5:
    st.subheader("🧩 Analisis Lanjutan: Usage Category")

    st.write(
        "Kategori ini dibuat dari jumlah rental harian menjadi Low Usage, Medium Usage, dan High Usage."
    )

    col_a, col_b = st.columns(2)

    with col_a:
        usage_count = filtered_day["usage_category"].value_counts().reset_index()
        usage_count.columns = ["usage_category", "count"]

        fig7 = px.pie(
            usage_count,
            names="usage_category",
            values="count",
            title="Distribusi Usage Category"
        )
        st.plotly_chart(fig7, use_container_width=True)

    with col_b:
        usage_season = pd.crosstab(
            filtered_day["season_label"],
            filtered_day["usage_category"]
        ).reset_index()

        usage_melt = usage_season.melt(
            id_vars="season_label",
            var_name="usage_category",
            value_name="count"
        )

        fig8 = px.bar(
            usage_melt,
            x="season_label",
            y="count",
            color="usage_category",
            barmode="group",
            title="Usage Category berdasarkan Season"
        )
        st.plotly_chart(fig8, use_container_width=True)

    selected_usage = st.selectbox(
        "Pilih kategori untuk drill-down",
        ["Low Usage", "Medium Usage", "High Usage"]
    )

    detail = filtered_day[
        filtered_day["usage_category"].astype(str) == selected_usage
    ]

    st.write(f"Data detail untuk kategori: {selected_usage}")

st.dataframe(
    detail[
        [
            "dteday",
            "season_label",
            "weather_label",
            "weekday_label",
            "temp_c",
            "humidity_pct",
            "casual",
            "registered",
            "cnt"
        ]
    ],
    use_container_width=True
)

st.subheader("Data Hourly (Per Jam)")

st.dataframe(
    filtered_hour[
        [
            "datetime",
            "hr",
            "season_label",
            "weather_label",
            "weekday_label",
            "temp_c",
            "humidity_pct",
            "casual",
            "registered",
            "cnt"
        ]
    ],
    use_container_width=True
)