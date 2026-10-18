from pathlib import Path
import unicodedata

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard ERA5 – Europa", page_icon="🌦️", layout="wide")

st.markdown("""
<style>
    .main .block-container {padding-top: 1.8rem; padding-bottom: 2rem;}
    .dashboard-title {font-size: 2.3rem; font-weight: 800; margin-bottom: 0.2rem;}
    .dashboard-subtitle {color: #6c757d; font-size: 1rem; margin-bottom: 1.2rem;}
    .metric-card {border: 1px solid rgba(120,120,120,0.25); border-radius: 18px; padding: 18px 20px; background: rgba(255,255,255,0.04); box-shadow: 0 8px 24px rgba(0,0,0,0.08); min-height: 110px;}
    .metric-label {font-size: 0.82rem; color: #808891; margin-bottom: 0.4rem;}
    .metric-value {font-size: 1.65rem; font-weight: 800;}
    .chart-card {border: 1px solid rgba(120,120,120,0.25); border-radius: 18px; padding: 14px 14px 6px 14px; background: rgba(255,255,255,0.03); box-shadow: 0 8px 24px rgba(0,0,0,0.08); margin-bottom: 1.1rem;}
    div[data-testid="stDataFrame"] {border: 1px solid rgba(120,120,120,0.25); border-radius: 14px; padding: 8px; box-shadow: 0 8px 24px rgba(0,0,0,0.08);}
    .sidebar-help {
        border: 1px solid rgba(255, 75, 75, 0.65);
        border-radius: 14px;
        padding: 14px 14px;
        background: rgba(255, 75, 75, 0.06);
        margin-top: 1rem;
        font-size: 0.82rem;
        line-height: 1.45;
    }
    .sidebar-help-title {
        font-weight: 800;
        margin-bottom: 0.45rem;
        color: #ff6b6b;
    }
    .sidebar-help ul {
        padding-left: 1.1rem;
        margin-bottom: 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="dashboard-title">🌦️ Dashboard klimatyczny ERA5</div>', unsafe_allow_html=True)
st.markdown('<div class="dashboard-subtitle">Interaktywna analiza temperatury, opadów, wilgotności i ekstremów klimatycznych dla wybranych lokalizacji.</div>', unsafe_allow_html=True)

DATA_DIR = Path(__file__).parent
DAILY_FILE = DATA_DIR / "era5europa_daily.parquet"
MONTHLY_FILE = DATA_DIR / "era5europa_monthly.parquet"
YEARLY_FILE = DATA_DIR / "era5europa_yearly.parquet"
RAW_FILE = DATA_DIR / "era5_europa_raw_1940_2026.parquet"
METRICS_FILE = DATA_DIR / "catboost_results_metrics.csv"
TEST_PRED_FILE = DATA_DIR / "catboost_test_predictions.csv"
FUTURE_FORECAST_FILE = DATA_DIR / "catboost_future_7day_forecast.csv"

CITY_COORDS = {
    "polska_krakow": {"latitude": 50.06, "longitude": 19.94},
    "polska_warszawa": {"latitude": 52.23, "longitude": 21.01},
    "polska_gdansk": {"latitude": 54.35, "longitude": 18.65},
    "polska_poznan": {"latitude": 52.41, "longitude": 16.93},
    "hiszpania_madrid": {"latitude": 40.42, "longitude": -3.70},
    "hiszpania_barcelona": {"latitude": 41.39, "longitude": 2.17},
    "hiszpania_valencia": {"latitude": 39.47, "longitude": -0.38},
    "hiszpania_granada": {"latitude": 37.18, "longitude": -3.60},
    "norwegia_oslo": {"latitude": 59.91, "longitude": 10.75},
    "norwegia_bergen": {"latitude": 60.39, "longitude": 5.32},
    "norwegia_trondheim": {"latitude": 63.43, "longitude": 10.39},
    "norwegia_tromso": {"latitude": 69.65, "longitude": 18.96},
    "grecja_athens": {"latitude": 37.98, "longitude": 23.72},
    "grecja_thessaloniki": {"latitude": 40.64, "longitude": 22.94},
    "grecja_patras": {"latitude": 38.25, "longitude": 21.73},
    "grecja_heraklion": {"latitude": 35.34, "longitude": 25.13},
    "wegry_budapest": {"latitude": 47.50, "longitude": 19.04},
    "wegry_szeged": {"latitude": 46.25, "longitude": 20.15},
    "wegry_pecs": {"latitude": 46.07, "longitude": 18.23},
    "wegry_debrecen": {"latitude": 47.53, "longitude": 21.63},
    "turcja_istanbul": {"latitude": 41.01, "longitude": 28.97},
    "turcja_ankara": {"latitude": 39.93, "longitude": 32.85},
    "turcja_izmir": {"latitude": 38.42, "longitude": 27.14},
    "turcja_antalya": {"latitude": 36.90, "longitude": 30.70},
    "wlochy_rome": {"latitude": 41.90, "longitude": 12.50},
    "wlochy_milan": {"latitude": 45.46, "longitude": 9.19},
    "wlochy_bologna": {"latitude": 44.50, "longitude": 11.34},
    "wlochy_naples": {"latitude": 40.85, "longitude": 14.27},
    "rumunia_bucharest": {"latitude": 44.43, "longitude": 26.10},
    "rumunia_cluj": {"latitude": 46.77, "longitude": 23.59},
    "rumunia_iasi": {"latitude": 47.16, "longitude": 27.58},
    "rumunia_timisoara": {"latitude": 45.75, "longitude": 21.23},
    "francja_paris": {"latitude": 48.86, "longitude": 2.35},
    "francja_lyon": {"latitude": 45.76, "longitude": 4.84},
    "francja_toulouse": {"latitude": 43.60, "longitude": 1.44},
    "francja_nice": {"latitude": 43.70, "longitude": 7.26},
}

POLISH_COLS = {
    "kraj": "Kraj", "miasto": "Miasto", "year": "Rok", "month": "Miesiąc", "day": "Dzień", "date": "Data", "lokalizacja": "Lokalizacja",
    "tempC_mean": "Średnia temperatura [°C]", "tempC_min": "Temperatura minimalna [°C]", "tempC_max": "Temperatura maksymalna [°C]",
    "dewpointC_mean": "Średni punkt rosy [°C]", "humidity_mean": "Średnia wilgotność [%]", "tempdewdiff_mean": "Różnica temp.–punkt rosy [°C]",
    "windspeed_mean": "Średnia prędkość wiatru [m/s]", "windspeed_max": "Maks. prędkość wiatru [m/s]",
    "tpmm_sum": "Suma opadów [mm]", "tpmm_annual": "Roczna suma opadów [mm]", "tpmm_extreme": "Opady ekstremalne [mm]",
    "tpmm_extreme_sum": "Suma opadów ekstremalnych [mm]", "tpmm_extreme_annual": "Roczna suma opadów ekstremalnych [mm]",
    "extreme_hours": "Godziny z opadem ekstremalnym", "extreme_hours_sum": "Suma godzin z opadem ekstremalnym", "extreme_hours_annual": "Roczna liczba godzin z opadem ekstremalnym",
    "heat_hours": "Godziny upalne", "heat_hours_sum": "Suma godzin upalnych", "heat_hours_annual": "Roczna liczba godzin upalnych",
    "frost_hours": "Godziny mroźne", "frost_hours_sum": "Suma godzin mroźnych", "frost_hours_annual": "Roczna liczba godzin mroźnych",
    "rainy_days": "Dni z opadem", "rainy_days_annual": "Roczna liczba dni z opadem", "heavy_rain_days": "Dni z ulewą", "heavy_rain_days_annual": "Roczna liczba dni z ulewą",
    "heat_days": "Dni z godzinami upalnymi", "frost_days": "Dni z godzinami mroźnymi", "hot_days": "Dni upalne", "hot_days_annual": "Roczna liczba dni upalnych",
    "cold_days": "Dni silnego mrozu", "cold_days_annual": "Roczna liczba dni silnego mrozu",
}

df_metrics = load_parquet(METRICS_FILE) if METRICS_FILE.suffix == ".parquet" else pd.read_csv(METRICS_FILE)
df_test_pred = pd.read_csv(TEST_PRED_FILE)
df_future = pd.read_csv(FUTURE_FORECAST_FILE)

df_test_pred["date"] = pd.to_datetime(df_test_pred["date"])
df_test_pred["forecast_date"] = pd.to_datetime(df_test_pred["forecast_date"])
df_future["date"] = pd.to_datetime(df_future["date"])
df_future["forecast_date"] = pd.to_datetime(df_future["forecast_date"])

df_test_pred["lokalizacja"] = df_test_pred["kraj"].astype(str) + " – " + df_test_pred["miasto"].astype(str)
df_future["lokalizacja"] = df_future["kraj"].astype(str) + " – " + df_future["miasto"].astype(str)

def normalize_text(value: str) -> str:
    value = str(value).strip().lower()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.replace("ł", "l").replace("Ł", "l")
    return value.replace(" ", "_").replace("-", "_")

def pl_label(col: str) -> str:
    return POLISH_COLS.get(col, col)

def add_location(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["lokalizacja"] = df["kraj"].astype(str) + " – " + df["miasto"].astype(str)
    return df

def translate_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={c: pl_label(c) for c in df.columns})

def apply_fig_style(fig, height=500):
    fig.update_layout(
        height=height,
        margin=dict(l=30, r=30, t=70, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(245,245,245,0.08)",
        legend_title_text="",
        hovermode="x unified",
        font=dict(size=13),
        title=dict(x=0.02, xanchor="left", font=dict(size=19)),
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(150,150,150,0.25)", zeroline=False, showline=True, linewidth=1, linecolor="rgba(150,150,150,0.45)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(150,150,150,0.25)", zeroline=False, showline=True, linewidth=1, linecolor="rgba(150,150,150,0.45)")
    return fig

def show_chart(fig, height=500):
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(apply_fig_style(fig, height), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

@st.cache_data(show_spinner=True)
def load_parquet(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path)

@st.cache_data(show_spinner=True)
def aggregate_from_raw(raw_path: Path):
    df = pd.read_parquet(raw_path)
    required = {"kraj", "miasto", "year", "month", "day", "temp_C", "dewpoint_C", "humidity", "temp_dew_diff", "wind_speed", "tp_mm"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Brakuje kolumn w pliku raw: {missing}")

    def aggregate_extreme_precip(group):
        rain = group["tp_mm"]
        temp = group["temp_C"]
        return pd.Series({
            "tpmm_sum": float(rain.sum()),
            "tpmm_extreme": float(rain[rain >= 10.1].sum()),
            "extreme_hours": int((rain >= 10.1).sum()),
            "heat_hours": int((temp > 30).sum()),
            "frost_hours": int((temp <= -15).sum()),
        })

    daily_parts = []
    for (kraj, miasto), chunk in df.groupby(["kraj", "miasto"]):
        grp = chunk.groupby(["year", "month", "day"])
        meteo = grp.agg(
            tempC_mean=("temp_C", "mean"), tempC_min=("temp_C", "min"), tempC_max=("temp_C", "max"),
            dewpointC_mean=("dewpoint_C", "mean"), humidity_mean=("humidity", "mean"),
            tempdewdiff_mean=("temp_dew_diff", "mean"), windspeed_mean=("wind_speed", "mean"), windspeed_max=("wind_speed", "max"),
        ).reset_index()
        precip = grp.apply(aggregate_extreme_precip).reset_index()
        daily = meteo.merge(precip, on=["year", "month", "day"])
        daily["kraj"] = kraj
        daily["miasto"] = miasto
        daily["date"] = pd.to_datetime(daily[["year", "month", "day"]])
        daily_parts.append(daily)
    df_daily = pd.concat(daily_parts, ignore_index=True)

    monthly_parts = []
    for (kraj, miasto), chunk in df_daily.groupby(["kraj", "miasto"]):
        monthly = chunk.groupby(["year", "month"]).agg(
            tempC_mean=("tempC_mean", "mean"), tempC_min=("tempC_min", "min"), tempC_max=("tempC_max", "max"),
            dewpointC_mean=("dewpointC_mean", "mean"), humidity_mean=("humidity_mean", "mean"),
            tempdewdiff_mean=("tempdewdiff_mean", "mean"), windspeed_mean=("windspeed_mean", "mean"), windspeed_max=("windspeed_max", "max"),
            tpmm_sum=("tpmm_sum", "sum"), tpmm_extreme_sum=("tpmm_extreme", "sum"), extreme_hours_sum=("extreme_hours", "sum"),
            heat_hours_sum=("heat_hours", "sum"), frost_hours_sum=("frost_hours", "sum"),
            rainy_days=("tpmm_sum", lambda x: (x > 0.1).sum()), heavy_rain_days=("tpmm_extreme", lambda x: (x > 0).sum()),
            heat_days=("heat_hours", lambda x: (x > 0).sum()), frost_days=("frost_hours", lambda x: (x > 0).sum()),
            hot_days=("tempC_max", lambda x: (x > 30).sum()), cold_days=("tempC_min", lambda x: (x <= -15).sum()),
        ).reset_index()
        monthly["kraj"] = kraj
        monthly["miasto"] = miasto
        monthly_parts.append(monthly)
    df_monthly = pd.concat(monthly_parts, ignore_index=True)

    yearly_parts = []
    for (kraj, miasto), chunk in df_monthly.groupby(["kraj", "miasto"]):
        yearly = chunk.groupby("year").agg(
            tempC_mean=("tempC_mean", "mean"), tempC_min=("tempC_min", "min"), tempC_max=("tempC_max", "max"),
            dewpointC_mean=("dewpointC_mean", "mean"), humidity_mean=("humidity_mean", "mean"),
            tempdewdiff_mean=("tempdewdiff_mean", "mean"), windspeed_mean=("windspeed_mean", "mean"), windspeed_max=("windspeed_max", "max"),
            tpmm_annual=("tpmm_sum", "sum"), tpmm_extreme_annual=("tpmm_extreme_sum", "sum"), extreme_hours_annual=("extreme_hours_sum", "sum"),
            rainy_days_annual=("rainy_days", "sum"), heavy_rain_days_annual=("heavy_rain_days", "sum"),
            heat_hours_annual=("heat_hours_sum", "sum"), frost_hours_annual=("frost_hours_sum", "sum"),
            hot_days_annual=("hot_days", "sum"), cold_days_annual=("cold_days", "sum"),
        ).reset_index()
        yearly["kraj"] = kraj
        yearly["miasto"] = miasto
        yearly_parts.append(yearly)
    df_yearly = pd.concat(yearly_parts, ignore_index=True)
    return df_daily, df_monthly, df_yearly

try:
    if DAILY_FILE.exists() and MONTHLY_FILE.exists() and YEARLY_FILE.exists():
        df_daily = load_parquet(DAILY_FILE)
        df_monthly = load_parquet(MONTHLY_FILE)
        df_yearly = load_parquet(YEARLY_FILE)
    elif RAW_FILE.exists():
        df_daily, df_monthly, df_yearly = aggregate_from_raw(RAW_FILE)
    else:
        st.error("Nie znaleziono plików danych. Umieść obok aplikacji pliki daily/monthly/yearly albo raw parquet.")
        st.stop()
except Exception as e:
    st.error(f"Błąd podczas wczytywania danych: {e}")
    st.stop()

for df in [df_daily, df_monthly, df_yearly]:
    df["kraj"] = df["kraj"].astype(str)
    df["miasto"] = df["miasto"].astype(str)
    df["kraj_norm"] = df["kraj"].map(normalize_text)
    df["miasto_norm"] = df["miasto"].map(normalize_text)
    df["coord_key"] = df["kraj_norm"] + "_" + df["miasto_norm"]

if "date" in df_daily.columns:
    df_daily["date"] = pd.to_datetime(df_daily["date"])
else:
    df_daily["date"] = pd.to_datetime(df_daily[["year", "month", "day"]])

df_monthly["date"] = pd.to_datetime(dict(year=df_monthly["year"], month=df_monthly["month"], day=1))


with st.sidebar:
    st.markdown("### 🌍 ERA5 Dashboard")
    st.caption(
        "Analiza trendów klimatycznych, ekstremów pogodowych "
        "oraz prognoz temperatury dla miast Europy."
    )

    st.divider()

    kraje = sorted(df_yearly["kraj"].dropna().unique())

    kraje = sorted(df_yearly["kraj"].dropna().unique())

    selected_countries = st.multiselect(
        "Kraj",
        kraje,
        default=kraje
    )

    miasta_available = sorted(
        df_yearly[
            df_yearly["kraj"].isin(selected_countries)
        ]["miasto"].dropna().unique()
    )

    selected_cities = st.multiselect(
        "Miasto",
        miasta_available,
        default=miasta_available[: min(12, len(miasta_available))]
    )

    min_year = int(df_yearly["year"].min())
    max_year = int(df_yearly["year"].max())

    year_range = st.slider(
        "Zakres lat",
        min_year,
        max_year,
        (min_year, max_year)
    )
    metric_options = {
        "Średnia temperatura [°C]": "tempC_mean", "Maksymalna temperatura [°C]": "tempC_max", "Minimalna temperatura [°C]": "tempC_min",
        "Roczna suma opadów [mm]": "tpmm_annual", "Dni upalne [liczba dni]": "hot_days_annual", "Dni silnego mrozu [liczba dni]": "cold_days_annual",
        "Dni z ulewą [liczba dni]": "heavy_rain_days_annual", "Średnia wilgotność [%]": "humidity_mean", "Średnia prędkość wiatru [m/s]": "windspeed_mean",
    }
    selected_metric_label = st.selectbox("Główna metryka", list(metric_options.keys()))
    selected_metric = metric_options[selected_metric_label]
    st.markdown(
        """
        <div class="sidebar-help">
            <div class="sidebar-help-title">Jak korzystać z filtrów?</div>
            <ul>
                <li>Najpierw wybierz kraje i miasta do analizy.</li>
                <li>Ustaw zakres lat, dla którego mają być liczone wykresy i rankingi.</li>
                <li>Główna metryka steruje wykresami trendów rocznych.</li>
                <li>W zakładce mapy i rankingów możesz osobno wybrać metrykę oraz TOP/BOTTOM N.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

base_filter = df_yearly["kraj"].isin(selected_countries) & df_yearly["miasto"].isin(selected_cities) & df_yearly["year"].between(year_range[0], year_range[1])
yearly = add_location(df_yearly[base_filter])
monthly = add_location(df_monthly[df_monthly["kraj"].isin(selected_countries) & df_monthly["miasto"].isin(selected_cities) & df_monthly["year"].between(year_range[0], year_range[1])])
daily = add_location(df_daily[df_daily["kraj"].isin(selected_countries) & df_daily["miasto"].isin(selected_cities) & df_daily["year"].between(year_range[0], year_range[1])])

if yearly.empty:
    st.warning("Brak danych dla wybranych filtrów.")
    st.stop()

st.subheader("Podsumowanie")
col1, col2, col3, col4, col5 = st.columns(5)
metrics = [
    (col1, "Liczba krajów", yearly["kraj"].nunique()),
    (col2, "Liczba miast", yearly["miasto"].nunique()),
    (col3, "Zakres lat", f"{yearly['year'].min()}–{yearly['year'].max()}"),
    (col4, "Średnia temp.", f"{yearly['tempC_mean'].mean():.2f} °C"),
    (col5, "Roczny opad", f"{yearly['tpmm_annual'].mean():.1f} mm" if "tpmm_annual" in yearly.columns else "—"),
]
for col, label, value in metrics:
    with col:
        st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)

st.divider()

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Trendy roczne",
    "Ekstrema klimatyczne",
    "Sezonowość miesięczna",
    "Mapa lokalizacji",
    "Rankingi",
    "Dane",
    "Prognoza temperatury"
])

with tab1:
    st.subheader("Trend roczny wybranej metryki")
    fig = px.line(yearly, x="year", y=selected_metric, color="lokalizacja", markers=True, title=f"{selected_metric_label} w czasie", labels={"year": "Rok", selected_metric: selected_metric_label, "lokalizacja": "Lokalizacja"})
    show_chart(fig, 560)
    trend_country = yearly.groupby(["kraj", "year"], as_index=False)[selected_metric].mean()
    fig2 = px.line(trend_country, x="year", y=selected_metric, color="kraj", markers=True, title="Średni trend według kraju", labels={"year": "Rok", selected_metric: selected_metric_label, "kraj": "Kraj"})
    show_chart(fig2, 500)

with tab2:
    st.subheader("Ekstrema: upały, mróz i ulewy")

    poziom_ekstremow = st.radio(
        "Poziom prezentacji danych",
        ["Według krajów", "Według miast", "Kraje i miasta"],
        horizontal=True
    )

    charts = [
        ("hot_days_annual", "Dni upalne, temp. max > 30°C", "Roczna liczba dni upalnych"),
        ("cold_days_annual", "Dni silnego mrozu, temp. min ≤ -15°C", "Roczna liczba dni silnego mrozu"),
        ("heavy_rain_days_annual", "Dni z ulewą", "Roczna liczba dni z ulewą"),
    ]

    if poziom_ekstremow in ["Według krajów", "Kraje i miasta"]:
        st.markdown("### Ekstrema klimatyczne według krajów")

        cols = st.columns(3)

        for c, (col, title, y_label) in zip(cols, charts):
            data_country = yearly.groupby(["year", "kraj"], as_index=False)[col].sum()

            fig = px.line(
                data_country,
                x="year",
                y=col,
                color="kraj",
                markers=True,
                title=title,
                labels={
                    "year": "Rok",
                    col: y_label,
                    "kraj": "Kraj"
                }
            )

            fig.update_layout(
                height=420,
                plot_bgcolor="rgba(245,245,245,0.08)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=40, r=30, t=60, b=40),
                legend_title_text="Kraj"
            )

            fig.update_xaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor="rgba(180,180,180,0.25)",
                zeroline=False
            )

            fig.update_yaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor="rgba(180,180,180,0.25)",
                zeroline=False
            )

            c.plotly_chart(fig, use_container_width=True)

    if poziom_ekstremow in ["Według miast", "Kraje i miasta"]:
        st.markdown("### Ekstrema klimatyczne według wybranych miast")

        cols = st.columns(3)

        for c, (col, title, y_label) in zip(cols, charts):
            data_city = yearly.groupby(["year", "lokalizacja"], as_index=False)[col].sum()

            fig = px.line(
                data_city,
                x="year",
                y=col,
                color="lokalizacja",
                markers=True,
                title=title + " – miasta",
                labels={
                    "year": "Rok",
                    col: y_label,
                    "lokalizacja": "Miasto"
                }
            )

            fig.update_layout(
                height=420,
                plot_bgcolor="rgba(245,245,245,0.08)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=40, r=30, t=60, b=40),
                legend_title_text="Miasto"
            )

            fig.update_xaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor="rgba(180,180,180,0.25)",
                zeroline=False
            )

            fig.update_yaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor="rgba(180,180,180,0.25)",
                zeroline=False
            )

            c.plotly_chart(fig, use_container_width=True)

    st.subheader("Porównanie ekstremów dla lokalizacji")

    extremes = yearly.groupby("lokalizacja", as_index=False)[
        ["hot_days_annual", "cold_days_annual", "heavy_rain_days_annual"]
    ].mean()

    extremes_long = extremes.melt(
        id_vars="lokalizacja",
        var_name="metryka",
        value_name="średnia roczna liczba dni"
    )

    labels = {
        "hot_days_annual": "Dni upalne",
        "cold_days_annual": "Dni mroźne",
        "heavy_rain_days_annual": "Dni z ulewą",
    }

    extremes_long["metryka"] = extremes_long["metryka"].map(labels)

    max_y = extremes_long["średnia roczna liczba dni"].max()

    fig = px.bar(
        extremes_long,
        x="lokalizacja",
        y="średnia roczna liczba dni",
        color="metryka",
        barmode="group",
        text="średnia roczna liczba dni",
        title="Średnia roczna liczba dni ekstremalnych w wybranych miastach",
        labels={
            "lokalizacja": "Lokalizacja",
            "średnia roczna liczba dni": "Średnia roczna liczba dni",
            "metryka": "Rodzaj ekstremum"
        }
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside",
        cliponaxis=False
    )

    fig.update_layout(
        height=680,
        plot_bgcolor="rgba(245,245,245,0.08)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=30, t=90, b=160),
        xaxis_tickangle=-45,
        legend_title_text="Rodzaj ekstremum",
        uniformtext_minsize=8,
        uniformtext_mode="show"
    )

    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(180,180,180,0.25)"
    )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(180,180,180,0.25)",
        range=[0, max_y * 1.25 if max_y > 0 else 1]
    )

    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Sezonowość miesięczna")
    monthly_metric_map = {
        "tempC_mean": "tempC_mean",
        "tempC_max": "tempC_max",
        "tempC_min": "tempC_min",
        "tpmm_annual": "tpmm_sum",
        "hot_days_annual": "hot_days",
        "cold_days_annual": "cold_days",
        "heavy_rain_days_annual": "heavy_rain_days",
        "humidity_mean": "humidity_mean",
        "windspeed_mean": "windspeed_mean",
    }

    m_col = monthly_metric_map[selected_metric]
    m_label = selected_metric_label
    monthly_avg = monthly.groupby(["month", "lokalizacja"], as_index=False)[m_col].mean()
    fig = px.line(monthly_avg, x="month", y=m_col, color="lokalizacja", markers=True, title=f"Średni przebieg miesięczny dla miast: {m_label}", labels={"month": "Miesiąc", m_col: m_label, "lokalizacja": "Lokalizacja"})
    fig.update_xaxes(dtick=1)
    show_chart(fig, 520)
    heatmap_data = monthly.groupby(["lokalizacja", "month"], as_index=False)[m_col].mean()
    fig2 = px.density_heatmap(heatmap_data, x="month", y="lokalizacja", z=m_col, histfunc="avg", title=f"Mapa ciepła miesięcy dla wybranych miast: {m_label}", labels={"month": "Miesiąc", "lokalizacja": "Lokalizacja", m_col: m_label})
    fig2.update_xaxes(dtick=1)
    show_chart(fig2, 520)

with tab4:
    st.subheader("Mapa lokalizacji")

    ranking_metric = selected_metric
    ranking_metric_label = selected_metric_label

    ranking = yearly.groupby(["kraj", "miasto", "coord_key"], as_index=False)[ranking_metric].mean()
    ranking["lokalizacja"] = ranking["kraj"] + " – " + ranking["miasto"]
    ranking["lat"] = ranking["coord_key"].map(lambda key: CITY_COORDS.get(key, {}).get("latitude"))
    ranking["lon"] = ranking["coord_key"].map(lambda key: CITY_COORDS.get(key, {}).get("longitude"))

    missing_coords = ranking[
        ranking["lat"].isna() | ranking["lon"].isna()
    ][["kraj", "miasto", "coord_key"]].drop_duplicates()

    mapa = ranking.dropna(subset=["lat", "lon"]).copy().sort_values(ranking_metric, ascending=False)

    if not missing_coords.empty:
        st.warning(
            "Brak współrzędnych dla: "
            + ", ".join(
                (
                    missing_coords["kraj"]
                    + " – "
                    + missing_coords["miasto"]
                    + " ["
                    + missing_coords["coord_key"]
                    + "]"
                ).tolist()
            )
        )

    if mapa.empty:
        st.warning("Brak współrzędnych dla wybranych miast.")
    else:
        top_row = mapa.sort_values(ranking_metric, ascending=False).iloc[0]
        bottom_row = mapa.sort_values(ranking_metric, ascending=True).iloc[0]
        avg_value = mapa[ranking_metric].mean()
        median_value = mapa[ranking_metric].median()

        k1, k2, k3, k4 = st.columns(4)

        cards = [
            (k1, "Najwyższa wartość", top_row[ranking_metric], top_row["lokalizacja"]),
            (k2, "Najniższa wartość", bottom_row[ranking_metric], bottom_row["lokalizacja"]),
            (k3, "Średnia dla lokalizacji", avg_value, ranking_metric_label),
            (k4, "Mediana", median_value, f"{mapa['lokalizacja'].nunique()} lokalizacji")
        ]

        for k, label, value, desc in cards:
            with k:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{value:.2f}</div>
                        <div style="font-size:0.85rem;color:#808891;">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("### Lokalizacje na mapie Europy")

        fig_map = px.scatter_mapbox(
            mapa,
            lat="lat",
            lon="lon",
            color=ranking_metric,
            size=ranking_metric,
            hover_name="lokalizacja",
            hover_data={
                "kraj": True,
                "miasto": True,
                ranking_metric: ":.2f",
                "lat": False,
                "lon": False
            },
            zoom=3.0,
            height=650,
            title=f"Lokalizacje pomiarowe w Europie – {ranking_metric_label}",
            color_continuous_scale="Turbo",
            size_max=30,
            labels={
                ranking_metric: ranking_metric_label,
                "kraj": "Kraj",
                "miasto": "Miasto"
            }
        )

        fig_map.update_layout(
            mapbox_style="carto-positron",
            mapbox=dict(
                center=dict(lat=51.0, lon=14.0),
                zoom=3.0
            ),
            margin=dict(l=10, r=10, t=60, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_colorbar=dict(
                title=ranking_metric_label,
                thickness=18,
                len=0.75
            )
        )

        fig_map.update_traces(
            marker=dict(
                opacity=0.9,
                sizemin=10
            )
        )

        st.plotly_chart(fig_map, use_container_width=True)

        st.markdown("### Ranking lokalizacji na mapie")

        tryb_map_rankingu = st.radio(
            "Zakres rankingu na mapie",
            ["TOP N", "BOTTOM N", "TOP N i BOTTOM N", "Wszystkie"],
            horizontal=True,
            key="map_ranking_mode"
        )

        if tryb_map_rankingu != "Wszystkie":
            n_map = st.slider(
                "Ile lokalizacji pokazać?",
                min_value=1,
                max_value=max(1, min(30, mapa["lokalizacja"].nunique())),
                value=min(5, mapa["lokalizacja"].nunique()),
                key="map_ranking_n"
            )

        mapa_desc = mapa.sort_values(ranking_metric, ascending=False)
        mapa_asc = mapa.sort_values(ranking_metric, ascending=True)

        if tryb_map_rankingu == "TOP N":
            ranking_map_plot = mapa_desc.head(n_map).copy()
            ranking_map_plot["typ_rankingu"] = "TOP"
            title = f"TOP {n_map} lokalizacji według metryki: {ranking_metric_label}"

        elif tryb_map_rankingu == "BOTTOM N":
            ranking_map_plot = mapa_asc.head(n_map).copy()
            ranking_map_plot["typ_rankingu"] = "BOTTOM"
            title = f"BOTTOM {n_map} lokalizacji według metryki: {ranking_metric_label}"

        elif tryb_map_rankingu == "TOP N i BOTTOM N":
            top_part = mapa_desc.head(n_map).copy()
            bottom_part = mapa_asc.head(n_map).copy()

            top_part["typ_rankingu"] = "TOP"
            bottom_part["typ_rankingu"] = "BOTTOM"

            ranking_map_plot = pd.concat([top_part, bottom_part])
            ranking_map_plot = ranking_map_plot.drop_duplicates(subset=["lokalizacja"], keep="first")
            title = f"TOP {n_map} i BOTTOM {n_map} lokalizacji według metryki: {ranking_metric_label}"

        else:
            ranking_map_plot = mapa_desc.copy()
            ranking_map_plot["typ_rankingu"] = "Wszystkie"
            title = f"Wszystkie lokalizacje według metryki: {ranking_metric_label}"

        if tryb_map_rankingu == "TOP N i BOTTOM N":
            color_col = "typ_rankingu"
            color_map = {
                "TOP": "#ef4444",
                "BOTTOM": "#3b82f6"
            }
            legend_title = "Typ rankingu"
        else:
            color_col = ranking_metric
            color_map = None
            legend_title = ""

        fig_top5 = px.bar(
            ranking_map_plot,
            x=ranking_metric,
            y="lokalizacja",
            orientation="h",
            color=color_col,
            color_discrete_map=color_map,
            color_continuous_scale="Turbo" if color_col == ranking_metric else None,
            text=ranking_metric,
            title=title,
            labels={
                ranking_metric: ranking_metric_label,
                "lokalizacja": "Lokalizacja",
                "typ_rankingu": "Typ rankingu"
            }
        )

        fig_top5.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
            cliponaxis=False
        )

        fig_top5.update_layout(
            height=max(420, 35 * len(ranking_map_plot) + 160),
            yaxis={"categoryorder": "total ascending"},
            plot_bgcolor="rgba(245,245,245,0.08)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=40, r=80, t=70, b=40),
            coloraxis_showscale=False,
            uniformtext_minsize=8,
            uniformtext_mode="show",
            legend_title_text=legend_title
        )

        fig_top5.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(150,150,150,0.25)",
            zeroline=False
        )

        fig_top5.update_yaxes(showgrid=False)

        st.plotly_chart(fig_top5, use_container_width=True)

        st.markdown("### Automatyczna interpretacja")

        st.info(
            f"Najwyższą wartość metryki **{ranking_metric_label}** odnotowano dla lokalizacji "
            f"**{top_row['lokalizacja']}** ({top_row[ranking_metric]:.2f}), natomiast najniższą dla "
            f"**{bottom_row['lokalizacja']}** ({bottom_row[ranking_metric]:.2f}). "
            f"Średnia wartość dla aktualnie wybranych lokalizacji wynosi **{avg_value:.2f}**, "
            f"a mediana **{median_value:.2f}**."
        )

        st.markdown("### Tabela lokalizacji")

        tabela = mapa[["kraj", "miasto", "lokalizacja", ranking_metric, "lat", "lon"]].copy()
        tabela = tabela.rename(
            columns={
                "kraj": "Kraj",
                "miasto": "Miasto",
                "lokalizacja": "Lokalizacja",
                ranking_metric: ranking_metric_label,
                "lat": "Szerokość geograficzna",
                "lon": "Długość geograficzna"
            }
        )

        st.dataframe(
            tabela.style.format(
                {
                    ranking_metric_label: "{:.2f}",
                    "Szerokość geograficzna": "{:.2f}",
                    "Długość geograficzna": "{:.2f}"
                }
            ),
            use_container_width=True,
            hide_index=True
        )

with tab5:
    st.subheader("Rankingi lokalizacji")

    ranking_metric = selected_metric

    ranking = yearly.groupby(["kraj", "miasto"], as_index=False)[ranking_metric].mean()
    ranking["lokalizacja"] = ranking["kraj"] + " – " + ranking["miasto"]

    tryb_rankingu = st.radio(
        "Zakres rankingu",
        ["TOP N", "BOTTOM N", "TOP N i BOTTOM N", "Wszystkie"],
        horizontal=True
    )

    if tryb_rankingu != "Wszystkie":
        n = st.slider(
            "Ile lokalizacji pokazać?",
            min_value=1,
            max_value=max(1, min(30, ranking["lokalizacja"].nunique())),
            value=min(5, ranking["lokalizacja"].nunique())
        )

    ranking_desc = ranking.sort_values(ranking_metric, ascending=False)
    ranking_asc = ranking.sort_values(ranking_metric, ascending=True)

    if tryb_rankingu == "TOP N":
        ranking_plot = ranking_desc.head(n)
        title = f"TOP {n} lokalizacji według: {pl_label(ranking_metric)}"
    elif tryb_rankingu == "BOTTOM N":
        ranking_plot = ranking_asc.head(n)
        title = f"BOTTOM {n} lokalizacji według: {pl_label(ranking_metric)}"
    elif tryb_rankingu == "TOP N i BOTTOM N":
        ranking_plot = pd.concat([ranking_desc.head(n), ranking_asc.head(n)]).drop_duplicates(subset=["lokalizacja"])
        title = f"TOP {n} i BOTTOM {n} lokalizacji według: {pl_label(ranking_metric)}"
    else:
        ranking_plot = ranking_desc
        title = f"Wszystkie lokalizacje według: {pl_label(ranking_metric)}"

    fig = px.bar(
        ranking_plot,
        x=ranking_metric,
        y="lokalizacja",
        orientation="h",
        title=title,
        labels={
            ranking_metric: pl_label(ranking_metric),
            "lokalizacja": "Lokalizacja"
        },
        text=ranking_metric
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        cliponaxis=False
    )

    fig.update_layout(
        height=max(560, 35 * len(ranking_plot) + 160),
        yaxis={"categoryorder": "total ascending"},
        plot_bgcolor="rgba(245,245,245,0.08)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=80, t=80, b=50),
        uniformtext_minsize=8,
        uniformtext_mode="show"
    )

    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(150,150,150,0.25)",
        zeroline=False
    )

    fig.update_yaxes(showgrid=False)

    st.plotly_chart(fig, use_container_width=True)

    ranking_show = ranking_plot[["kraj", "miasto", ranking_metric, "lokalizacja"]].copy()
    ranking_show[ranking_metric] = ranking_show[ranking_metric].round(3)

    st.dataframe(
        translate_df(ranking_show),
        use_container_width=True,
        hide_index=True
    )

with tab6:
    st.subheader("Podgląd danych")
    dataset_choice = st.radio("Wybierz poziom agregacji", ["Roczne", "Miesięczne", "Dzienne"], horizontal=True)
    preview = yearly if dataset_choice == "Roczne" else monthly if dataset_choice == "Miesięczne" else daily
    preview_show = translate_df(preview)
    st.dataframe(preview_show, use_container_width=True, hide_index=True)
    csv = preview_show.to_csv(index=False).encode("utf-8-sig")
    st.download_button("Pobierz aktualnie przefiltrowane dane CSV", csv, file_name=f"era5_{dataset_choice.lower()}_filtered.csv", mime="text/csv")


with tab7:
    st.subheader("Prognoza temperatury na kolejne 7 dni")

    st.markdown(
        """
        Ta zakładka pokazuje prognozowaną średnią temperaturę dla lokalizacji wybranych w filtrach po lewej stronie.
        Prognoza obejmuje kolejne 7 dni.
        """
    )

    future_filtered = df_future[
        df_future["kraj"].isin(selected_countries)
        & df_future["miasto"].isin(selected_cities)
    ].copy()

    if future_filtered.empty:
        st.warning("Brak prognoz dla miast wybranych w filtrach po lewej stronie.")
        st.stop()

    future_filtered = future_filtered.sort_values(["lokalizacja", "forecast_date"])

    st.markdown("### Wykres prognozy")

    fig_future = px.line(
        future_filtered,
        x="forecast_date",
        y="prediction",
        color="lokalizacja",
        markers=True,
        title="Prognoza średniej temperatury na kolejne 7 dni",
        labels={
            "forecast_date": "Data prognozy",
            "prediction": "Prognozowana temperatura [°C]",
            "lokalizacja": "Lokalizacja"
        }
    )

    show_chart(fig_future, 560)

    st.markdown("### Mapa prognozy dla wybranego dnia")

    selected_forecast_day = st.slider(
        "Wybierz dzień prognozy",
        min_value=int(future_filtered["horyzont"].min()),
        max_value=int(future_filtered["horyzont"].max()),
        value=1,
        key="forecast_map_day"
    )

    forecast_map = future_filtered[
        future_filtered["horyzont"] == selected_forecast_day
    ].copy()

    forecast_map["kraj_norm"] = forecast_map["kraj"].map(normalize_text)
    forecast_map["miasto_norm"] = forecast_map["miasto"].map(normalize_text)
    forecast_map["coord_key"] = forecast_map["kraj_norm"] + "_" + forecast_map["miasto_norm"]

    forecast_map["lat"] = forecast_map["coord_key"].map(
        lambda key: CITY_COORDS.get(key, {}).get("latitude")
    )
    forecast_map["lon"] = forecast_map["coord_key"].map(
        lambda key: CITY_COORDS.get(key, {}).get("longitude")
    )

    forecast_map = forecast_map.dropna(subset=["lat", "lon"])

    if forecast_map.empty:
        st.warning("Brak współrzędnych dla wybranych lokalizacji.")
    else:
        fig_forecast_map = px.scatter_mapbox(
            forecast_map,
            lat="lat",
            lon="lon",
            color="prediction",
            size="prediction",
            hover_name="lokalizacja",
            hover_data={
                "kraj": True,
                "miasto": True,
                "prediction": ":.2f",
                "lat": False,
                "lon": False
            },
            zoom=3.0,
            height=600,
            title=f"Mapa prognozowanej temperatury – dzień {selected_forecast_day}",
            color_continuous_scale="Turbo",
            size_max=28,
            labels={
                "prediction": "Prognozowana temperatura [°C]",
                "kraj": "Kraj",
                "miasto": "Miasto"
            }
        )

        fig_forecast_map.update_layout(
            mapbox_style="carto-positron",
            mapbox=dict(
                center=dict(lat=51.0, lon=14.0),
                zoom=3.0
            ),
            margin=dict(l=10, r=10, t=60, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_colorbar=dict(
                title="Temperatura [°C]",
                thickness=18,
                len=0.75
            )
        )

        fig_forecast_map.update_traces(
            marker=dict(
                opacity=0.9,
                sizemin=10
            )
        )

        st.plotly_chart(fig_forecast_map, use_container_width=True)

    st.markdown("### Ranking najcieplejszych i najchłodniejszych lokalizacji")

    ranking_forecast = future_filtered.groupby(
        ["kraj", "miasto", "lokalizacja"],
        as_index=False
    ).agg(
        srednia_prognoza=("prediction", "mean")
    )

    n_rank = st.slider(
        "Ile lokalizacji pokazać w rankingu?",
        min_value=1,
        max_value=max(1, min(20, ranking_forecast["lokalizacja"].nunique())),
        value=min(5, ranking_forecast["lokalizacja"].nunique()),
        key="forecast_ranking_n"
    )

    col_top, col_bottom = st.columns(2)

    with col_top:
        st.markdown(f"#### TOP {n_rank} najcieplejszych lokalizacji")

        top_warm = ranking_forecast.sort_values(
            "srednia_prognoza",
            ascending=False
        ).head(n_rank)

        fig_top_warm = px.bar(
            top_warm,
            x="srednia_prognoza",
            y="lokalizacja",
            orientation="h",
            text="srednia_prognoza",
            title="Najcieplejsze lokalizacje według średniej prognozy",
            labels={
                "srednia_prognoza": "Średnia prognoza [°C]",
                "lokalizacja": "Lokalizacja"
            },
            color="srednia_prognoza",
            color_continuous_scale="Turbo"
        )

        fig_top_warm.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
            cliponaxis=False
        )

        fig_top_warm.update_layout(
            height=420,
            yaxis={"categoryorder": "total ascending"},
            coloraxis_showscale=False,
            margin=dict(l=40, r=80, t=70, b=40)
        )

        show_chart(fig_top_warm, 420)

    with col_bottom:
        st.markdown(f"#### TOP {n_rank} najchłodniejszych lokalizacji")

        top_cold = ranking_forecast.sort_values(
            "srednia_prognoza",
            ascending=True
        ).head(n_rank)

        fig_top_cold = px.bar(
            top_cold,
            x="srednia_prognoza",
            y="lokalizacja",
            orientation="h",
            text="srednia_prognoza",
            title="Najchłodniejsze lokalizacje według średniej prognozy",
            labels={
                "srednia_prognoza": "Średnia prognoza [°C]",
                "lokalizacja": "Lokalizacja"
            },
            color="srednia_prognoza",
            color_continuous_scale="Blues"
        )

        fig_top_cold.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
            cliponaxis=False
        )

        fig_top_cold.update_layout(
            height=420,
            yaxis={"categoryorder": "total descending"},
            coloraxis_showscale=False,
            margin=dict(l=40, r=80, t=70, b=40)
        )

        show_chart(fig_top_cold, 420)

    st.markdown("### Podsumowanie prognozy")

    summary_forecast = future_filtered.groupby(
        ["kraj", "miasto", "lokalizacja"],
        as_index=False
    ).agg(
        srednia_prognoza=("prediction", "mean"),
        min_prognoza=("prediction", "min"),
        max_prognoza=("prediction", "max")
    )

    summary_forecast = summary_forecast.rename(
        columns={
            "kraj": "Kraj",
            "miasto": "Miasto",
            "lokalizacja": "Lokalizacja",
            "srednia_prognoza": "Średnia prognoza [°C]",
            "min_prognoza": "Minimalna prognoza [°C]",
            "max_prognoza": "Maksymalna prognoza [°C]"
        }
    )

    st.dataframe(
        summary_forecast.style.format({
            "Średnia prognoza [°C]": "{:.2f}",
            "Minimalna prognoza [°C]": "{:.2f}",
            "Maksymalna prognoza [°C]": "{:.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Szczegółowa tabela prognoz")

    future_show = future_filtered[
        ["kraj", "miasto", "forecast_date", "horyzont", "prediction"]
    ].copy()

    future_show = future_show.rename(
        columns={
            "kraj": "Kraj",
            "miasto": "Miasto",
            "forecast_date": "Data prognozy",
            "horyzont": "Dzień prognozy",
            "prediction": "Prognozowana temperatura [°C]"
        }
    )

    st.dataframe(
        future_show.style.format(
            {"Prognozowana temperatura [°C]": "{:.2f}"}
        ),
        use_container_width=True,
        hide_index=True
    )