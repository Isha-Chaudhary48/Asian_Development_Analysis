# Asian Development Intelligence System — CSV version
# Run: streamlit run asian_dev_is.py
# Install: pip install streamlit plotly pandas

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="ADIS", page_icon="🌏", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.block-container{padding-top:1rem!important;padding-bottom:2rem!important}
[data-testid="metric-container"]{display:none!important}
.kpi-card{border-radius:12px;padding:14px 16px 12px;border-left:4px solid transparent;height:100%}
.kpi-label{font-size:11px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;margin-bottom:5px}
.kpi-value{font-size:26px;font-weight:700;line-height:1.1;margin-bottom:5px}
.kpi-delta{font-size:11px;font-weight:500;margin-bottom:7px}
.kpi-badge{font-size:10px;font-weight:600;padding:2px 8px;border-radius:20px;display:inline-block}
.kpi-source{font-size:9px;opacity:.55;margin-top:4px;font-family:monospace;display:block}
.kpi-blue{background:#E6F1FB;border-left-color:#185FA5}
.kpi-teal{background:#E1F5EE;border-left-color:#0F6E56}
.kpi-purple{background:#EEEDFE;border-left-color:#534AB7}
.kpi-amber{background:#FAEEDA;border-left-color:#854F0B}
.kpi-red{background:#FCEBEB;border-left-color:#A32D2D}
.lbl-blue{color:#185FA5}.lbl-teal{color:#0F6E56}.lbl-purple{color:#534AB7}.lbl-amber{color:#854F0B}.lbl-red{color:#A32D2D}
.val-blue{color:#0C447C}.val-teal{color:#085041}.val-purple{color:#3C3489}.val-amber{color:#633806}.val-red{color:#791F1F}
.bdg-blue{background:#B5D4F4;color:#0C447C}.bdg-teal{background:#9FE1CB;color:#085041}
.bdg-purple{background:#CECBF6;color:#3C3489}.bdg-amber{background:#FAC775;color:#633806}.bdg-red{background:#F7C1C1;color:#791F1F}
.positive-delta{color:#0F6E56}.negative-delta{color:#A32D2D}.neutral-delta{color:#888780}
.section-divider{font-size:10px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;color:#888780;margin:16px 0 10px;padding-bottom:5px;border-bottom:1px solid #e8e8e8}
.adis-score-card{display:flex;align-items:center;gap:20px;background:#E6F1FB;border-radius:12px;padding:16px 20px;border-left:4px solid #185FA5;margin-bottom:14px}
.adis-score-number{font-size:36px;font-weight:700;color:#0C447C;line-height:1}
.adis-score-title{font-size:9px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;color:#185FA5;margin-bottom:3px}
.adis-grade-label{font-size:13px;font-weight:600;margin-top:3px}
.adis-rank-note{font-size:10px;color:#185FA5;margin-top:3px;line-height:1.5}
.pillar-row{display:flex;align-items:center;gap:10px;margin-bottom:6px}
.pillar-label{font-size:10px;font-weight:600;width:72px;flex-shrink:0}
.pillar-track{flex:1;height:6px;background:#e8e8e8;border-radius:3px;overflow:hidden}
.pillar-bar{height:100%;border-radius:3px;background:#9E9E9E!important}
.pillar-score{font-size:10px;font-weight:700;width:24px;text-align:right;flex-shrink:0}
.insight-box{border-radius:8px;padding:9px 12px;margin-bottom:7px;border-left:3px solid transparent}
.insight-title{font-size:10px;font-weight:700;letter-spacing:.3px;margin-bottom:2px}
.insight-body{font-size:10px;line-height:1.5}
.sidebar-section-label{font-size:9px;font-weight:700;letter-spacing:.7px;text-transform:uppercase;color:#888780;margin:9px 0 3px;padding-bottom:2px;border-bottom:.5px solid #e0e0e0}
.indicator-row{display:flex;align-items:center;gap:5px;padding:2px 3px;margin-bottom:1px}
.category-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.indicator-name{font-size:10px;color:#CCCCCC;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.indicator-value{font-size:10px;font-weight:600;color:#FFFFFF;white-space:nowrap}
.trend-arrow{font-size:9px;flex-shrink:0}
</style>
""", unsafe_allow_html=True)

# ── Column names that must match your CSV ──
CSV_COLUMN_TO_LABEL = {
    "gdp_per_capita":"GDP per capita","gdp_growth":"GDP growth",
    "fdi_inflows":"FDI inflows","unemployment":"Unemployment",
    "life_expectancy":"Life expectancy","infant_mortality":"Infant mortality",
    "hospital_beds":"Hospital beds","population":"Population",
    "school_enrolment_primary":"Primary enrolment",
    "school_enrolment_secondary":"Secondary enrolment","education_expenditure":"Education spend",
    "electricity_access":"Electricity access",
    "renewable_energy":"Renewable energy","forest_area":"Forest area",
    "clean_water_access":"Clean water","female_labour":"Female labour",
    "women_parliament":"Women in parliament",
    "maternal_mortality":"Maternal mortality","gender_parity":"Gender parity",
    "internet_users":"Internet users",
}
ALL_INDICATOR_COLUMNS = list(CSV_COLUMN_TO_LABEL.keys())

# ── How to display each indicator ──
INDICATOR_DISPLAY_CONFIG = {
    "gdp_per_capita":             {"pfx":"$","sfx":"",    "fmt":",.0f","higher_is_better":True, "dot_color":"#378ADD"},
    "gdp_growth":                 {"pfx":"", "sfx":"%",   "fmt":".1f", "higher_is_better":True, "dot_color":"#378ADD"},
    "fdi_inflows":                {"pfx":"", "sfx":"% GDP","fmt":".1f","higher_is_better":True, "dot_color":"#378ADD"},
    "unemployment":               {"pfx":"", "sfx":"%",   "fmt":".1f", "higher_is_better":False,"dot_color":"#378ADD"},
    "life_expectancy":            {"pfx":"", "sfx":" yrs","fmt":".1f", "higher_is_better":True, "dot_color":"#1D9E75"},
    "infant_mortality":           {"pfx":"", "sfx":"",    "fmt":".1f", "higher_is_better":False,"dot_color":"#E24B4A"},
    "hospital_beds":              {"pfx":"", "sfx":"/1k", "fmt":".1f", "higher_is_better":True, "dot_color":"#1D9E75"},
    "population":                 {"pfx":"", "sfx":"",    "fmt":",.0f","higher_is_better":True, "dot_color":"#1D9E75"},
    "school_enrolment_primary":   {"pfx":"", "sfx":"%",   "fmt":".1f", "higher_is_better":True, "dot_color":"#7F77DD"},
    "school_enrolment_secondary": {"pfx":"", "sfx":"%",   "fmt":".1f", "higher_is_better":True, "dot_color":"#7F77DD"},
    "education_expenditure":      {"pfx":"", "sfx":"% GDP","fmt":".1f","higher_is_better":True, "dot_color":"#7F77DD"},
    "electricity_access":         {"pfx":"", "sfx":"%",   "fmt":".1f", "higher_is_better":True, "dot_color":"#639922"},
    "renewable_energy":           {"pfx":"", "sfx":"%",   "fmt":".1f", "higher_is_better":True, "dot_color":"#639922"},
    "forest_area":                {"pfx":"", "sfx":"%",   "fmt":".1f", "higher_is_better":True, "dot_color":"#639922"},
    "clean_water_access":         {"pfx":"", "sfx":"%",   "fmt":".1f", "higher_is_better":True, "dot_color":"#1D9E75"},
    "female_labour":              {"pfx":"", "sfx":"%",   "fmt":".1f", "higher_is_better":True, "dot_color":"#D4537E"},
    "women_parliament":           {"pfx":"", "sfx":"%",   "fmt":".1f", "higher_is_better":True, "dot_color":"#D4537E"},
    "maternal_mortality":         {"pfx":"", "sfx":"",    "fmt":".0f", "higher_is_better":False,"dot_color":"#E24B4A"},
    "gender_parity":              {"pfx":"", "sfx":"",    "fmt":".2f", "higher_is_better":True, "dot_color":"#D4537E"},
    "internet_users":             {"pfx":"", "sfx":"%",   "fmt":".1f", "higher_is_better":True, "dot_color":"#EF9F27"},
}

ADIS_PILLARS = {
    "Economy":     {"pillar_color":"#378ADD","pillar_weight":0.25,"indicators":[("gdp_growth",0.30,True),("gdp_per_capita",0.25,True),("fdi_inflows",0.20,True),("unemployment",0.15,False)]},
    "Health":      {"pillar_color":"#1D9E75","pillar_weight":0.20,"indicators":[("life_expectancy",0.45,True),("infant_mortality",0.35,False),("hospital_beds",0.20,True)]},
    "Education":   {"pillar_color":"#7F77DD","pillar_weight":0.20,"indicators":[("school_enrolment_primary",0.25,True),("school_enrolment_secondary",0.25,True),("education_expenditure",0.15,True)]},
    "Environment": {"pillar_color":"#639922","pillar_weight":0.15,"indicators":[("electricity_access",0.25,True),("renewable_energy",0.25,True),("clean_water_access",0.25,True),("forest_area",0.15,True)]},
    "Gender":      {"pillar_color":"#D4537E","pillar_weight":0.10,"indicators":[("female_labour",0.25,True),("women_parliament",0.20,True),("maternal_mortality",0.20,False),("gender_parity",0.10,True)]},
    "Digital":     {"pillar_color":"#EF9F27","pillar_weight":0.10,"indicators":[("internet_users",1.00,True)]},
}

SCORE_NORMALIZATION_RANGES = {
    "gdp_growth":(-5,12),"gdp_per_capita":(200,50000),"fdi_inflows":(-2,10),
    "unemployment":(0,30),
    "life_expectancy":(45,85),"infant_mortality":(2,100),"hospital_beds":(0,15),
    "school_enrolment_primary":(30,130),
    "school_enrolment_secondary":(10,130),"education_expenditure":(0,10),
    "electricity_access":(0,100),"renewable_energy":(0,100),
    "forest_area":(0,90),"clean_water_access":(0,100),"female_labour":(10,85),
    "women_parliament":(0,60),"maternal_mortality":(2,2000),
    "gender_parity":(0.5,1.5),"internet_users":(0,100),
}

CATEGORY_CHART_COLORS = {
    "blue":  ["#378ADD","#85B7EB","#185FA5","#B5D4F4","#0C447C"],
    "teal":  ["#1D9E75","#5DCAA5","#0F6E56","#9FE1CB","#085041"],
    "purple":["#7F77DD","#AFA9EC","#534AB7","#CECBF6","#3C3489"],
    "amber": ["#EF9F27","#FAC775","#854F0B","#FAEEDA","#633806"],
    "red":   ["#E24B4A","#F09595","#A32D2D","#F7C1C1","#791F1F"],
    "green": ["#639922","#97C459","#3B6D11","#C0DD97","#27500A"],
    "pink":  ["#D4537E","#ED93B1","#993556","#F4C0D1","#72243E"],
}

CHART_BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="sans-serif",size=11,color="#444441"),
    margin=dict(l=8,r=8,t=36,b=8),
    legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,font=dict(size=10)),
    xaxis=dict(showgrid=False,zeroline=False),
    yaxis=dict(showgrid=True,gridcolor="#efefef",zeroline=False),
)

# ── Load CSV ──
@st.cache_data(ttl=0, show_spinner=False)
def load_csv_data() -> pd.DataFrame:
    """Reads world_bank_cleaned.csv. Expects columns: country_code, country_name, year, + indicator columns."""
    raw_df = pd.read_csv("Data/world_bank_cleaned.csv")
    raw_df = raw_df.rename(columns={"economy": "country_code", "country": "country_name"})
    raw_df["year"] = pd.to_numeric(raw_df["year"], errors="coerce")
    for col in ALL_INDICATOR_COLUMNS:
        if col in raw_df.columns:
            raw_df[col] = pd.to_numeric(raw_df[col], errors="coerce")
    return raw_df

def filter_by_countries_and_years(full_df, country_codes, start_year, end_year):
    """Returns only rows matching selected countries and year range."""
    return full_df[
        full_df["country_code"].isin(country_codes) &
        full_df["year"].between(start_year, end_year)
    ].copy()

# ── Value extractors ──
def get_latest_value(filtered_df, country_code, indicator_col):
    """Most recent non-null value for one country + indicator. Returns (value, year)."""
    rows = filtered_df[(filtered_df["country_code"]==country_code) & (filtered_df[indicator_col].notna())]
    if rows.empty: return None, None
    row = rows.sort_values("year", ascending=False).iloc[0]
    return row[indicator_col], int(row["year"])

def get_previous_year_value(filtered_df, country_code, indicator_col, latest_year):
    """Value exactly one year before latest_year. Used for delta arrows."""
    rows = filtered_df[(filtered_df["country_code"]==country_code) & (filtered_df["year"]==latest_year-1) & (filtered_df[indicator_col].notna())]
    return rows.iloc[0][indicator_col] if not rows.empty else None

def get_latest_for_all_countries(filtered_df, indicator_col):
    """One row per country with its most recent value for indicator_col."""
    if indicator_col not in filtered_df.columns: return pd.DataFrame()
    rows = filtered_df[filtered_df[indicator_col].notna()]
    return rows.sort_values("year", ascending=False).groupby("country_code").first().reset_index()

# ── Formatting ──
def format_indicator_value(raw_value, indicator_col):
    """Turns a float into a display string like '$2,390' or '6.4%'."""
    if raw_value is None or pd.isna(raw_value): return "N/A"
    cfg = INDICATOR_DISPLAY_CONFIG[indicator_col]
    p, s, f = cfg["pfx"], cfg["sfx"], cfg["fmt"]
    if "," in f and abs(raw_value)>=1e9: return f"{p}{raw_value/1e9:.1f}B{s}"
    if "," in f and abs(raw_value)>=1e6: return f"{p}{raw_value/1e6:.1f}M{s}"
    return f"{p}{raw_value:{f}}{s}"

def build_delta_html(current_value, previous_value, higher_is_better):
    """HTML string for the delta line e.g. '▲ 5.2% vs prev yr' in green."""
    if current_value is None or previous_value is None:
        return '<span class="neutral-delta">— no prior data</span>'
    change = current_value - previous_value
    pct    = abs(change/previous_value*100) if previous_value else 0
    is_good = (change>0)==higher_is_better 
    cls  = "positive-delta" if is_good else "negative-delta"
    sym  = "▲" if change>0 else "▼"
    return f'<span class="{cls}">{sym} {pct:.1f}% vs prev yr</span>'

# ── KPI card ──
def build_kpi_card_html(indicator_col, card_theme, badge_label, filtered_df, focus_country_code):
    """Returns HTML for one colored KPI card."""
    cfg   = INDICATOR_DISPLAY_CONFIG[indicator_col]
    label = CSV_COLUMN_TO_LABEL[indicator_col]
    current_val, current_year = get_latest_value(filtered_df, focus_country_code, indicator_col)
    prev_val = get_previous_year_value(filtered_df, focus_country_code, indicator_col, current_year) if current_year else None
    if current_val is None:
        return f'<div class="kpi-card kpi-{card_theme}"><div class="kpi-label lbl-{card_theme}">{label}</div><div class="kpi-value val-{card_theme}">N/A</div><div class="kpi-delta neutral-delta">— unavailable</div><span class="kpi-badge bdg-{card_theme}">{badge_label}</span></div>'
    return f'<div class="kpi-card kpi-{card_theme}"><div class="kpi-label lbl-{card_theme}">{label}</div><div class="kpi-value val-{card_theme}">{format_indicator_value(current_val,indicator_col)}</div><div class="kpi-delta">{build_delta_html(current_val,prev_val,cfg["higher_is_better"])}</div><span class="kpi-badge bdg-{card_theme}">{badge_label}</span><span class="kpi-source">{indicator_col} · {current_year}</span></div>'

# ── ADIS score engine ──
def normalize_to_score(raw_value, indicator_col, higher_is_better):
    """Converts a raw value to 0–100 score. 100 always = best."""
    if raw_value is None or pd.isna(raw_value): return None
    lo, hi = SCORE_NORMALIZATION_RANGES.get(indicator_col,(0,100))
    clamped = max(0.0, min(100.0, (raw_value-lo)/(hi-lo)*100))
    return clamped if higher_is_better else 100.0-clamped

def calculate_adis_score(filtered_df, country_code):
    """Returns (total_score, {pillar: score}) for one country."""
    pillar_results = {}
    for pillar_name, pillar_cfg in ADIS_PILLARS.items():
        w_sum = w_tot = 0.0
        for indicator_col, indicator_weight, higher_is_better in pillar_cfg["indicators"]:
            val, _ = get_latest_value(filtered_df, country_code, indicator_col)
            score  = normalize_to_score(val, indicator_col, higher_is_better)
            if score is None: continue
            w_sum += score*indicator_weight; w_tot += indicator_weight
        pillar_results[pillar_name] = round(w_sum/w_tot,1) if w_tot>0 else None
    valid = {p:s for p,s in pillar_results.items() if s is not None}
    if not valid: return None, pillar_results
    total = round(sum(valid[p]*ADIS_PILLARS[p]["pillar_weight"] for p in valid) / sum(ADIS_PILLARS[p]["pillar_weight"] for p in valid),1)
    return total, pillar_results

def get_development_grade(adis_score):
    """Converts numeric score to (grade_text, hex_color)."""
    if adis_score is None: return "—","#888780"
    if adis_score>=80: return "Advanced","#085041"
    if adis_score>=65: return "Progressive","#0F6E56"
    if adis_score>=50: return "Developing","#854F0B"
    if adis_score>=35: return "Emerging","#A32D2D"
    return "Critical","#791F1F"

# ── Chart helpers ──
def render_trend_line_chart(filtered_df, indicator_col, chart_title, y_axis_label, color_palette, y_axis_suffix=""):
    """Multi-line trend chart — one line per country over years."""
    if indicator_col not in filtered_df.columns: st.info(f"Column '{indicator_col}' not in CSV."); return
    chart_data = filtered_df[filtered_df[indicator_col].notna()]
    if chart_data.empty: st.info(f"No data for {indicator_col}."); return
    fig = px.line(chart_data.sort_values("year"), x="year", y=indicator_col, color="country_name",
                  title=chart_title, labels={indicator_col:y_axis_label,"year":"Year","country_name":"Country"},
                  color_discrete_sequence=CATEGORY_CHART_COLORS[color_palette])
    fig.update_traces(line_width=2, mode="lines+markers", marker_size=4)
    fig.update_layout(**CHART_BASE_LAYOUT)
    if y_axis_suffix: fig.update_yaxes(ticksuffix=y_axis_suffix)
    st.plotly_chart(fig, use_container_width=True)

def render_country_ranking_bar_chart(filtered_df, indicator_col, chart_title, y_axis_label, color_palette, higher_is_better=True, y_axis_suffix=""):
    """Bar chart of latest value per country, sorted best-first."""
    if indicator_col not in filtered_df.columns: st.info(f"Column '{indicator_col}' not in CSV."); return
    latest_per_country = get_latest_for_all_countries(filtered_df, indicator_col)
    if latest_per_country.empty: st.info(f"No data for {indicator_col}."); return
    ranked = latest_per_country.sort_values(indicator_col, ascending=not higher_is_better)
    fig = go.Figure(go.Bar(x=ranked["country_name"], y=ranked[indicator_col],
                           marker_color=CATEGORY_CHART_COLORS[color_palette][0],
                           text=ranked[indicator_col].round(1), textposition="outside"))
    fig.update_layout(title=chart_title, yaxis_title=y_axis_label, **CHART_BASE_LAYOUT)
    if y_axis_suffix: fig.update_yaxes(ticksuffix=y_axis_suffix)
    st.plotly_chart(fig, use_container_width=True)

def render_two_indicator_scatter(filtered_df, x_indicator, y_indicator, chart_title, x_label, y_label, color_palette, bubble_size_indicator=None):
    """Scatter comparing two indicators. Optional bubble sizing by a third indicator."""
    if x_indicator not in filtered_df.columns or y_indicator not in filtered_df.columns:
        st.info("One or both indicators not found in CSV."); return
    lx = get_latest_for_all_countries(filtered_df, x_indicator)[["country_code","country_name",x_indicator]].rename(columns={x_indicator:"x_value"})
    ly = get_latest_for_all_countries(filtered_df, y_indicator)[["country_code",y_indicator]].rename(columns={y_indicator:"y_value"})
    scatter_df = lx.merge(ly, on="country_code", how="inner")
    bubble_col = None
    if bubble_size_indicator and bubble_size_indicator in filtered_df.columns:
        ls = get_latest_for_all_countries(filtered_df, bubble_size_indicator)[["country_code",bubble_size_indicator]].rename(columns={bubble_size_indicator:"bubble_size"})
        scatter_df = scatter_df.merge(ls, on="country_code", how="left")
        scatter_df["bubble_size"] = scatter_df["bubble_size"].fillna(scatter_df["bubble_size"].median())
        bubble_col = "bubble_size"
    fig = px.scatter(scatter_df, x="x_value", y="y_value", text="country_name", size=bubble_col,
                     title=chart_title, labels={"x_value":x_label,"y_value":y_label},
                     color_discrete_sequence=CATEGORY_CHART_COLORS[color_palette])
    fig.update_traces(textposition="top center", marker_opacity=0.75)
    fig.update_layout(**CHART_BASE_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🌏 ADIS")
    st.markdown("---")

    with st.spinner("Loading dataset…"):
        full_world_bank_df = load_csv_data()

    available_country_codes = sorted(full_world_bank_df["country_code"].dropna().unique().tolist())
    available_country_names = {r["country_code"]:r["country_name"] for _,r in full_world_bank_df[["country_code","country_name"]].drop_duplicates().iterrows()}

    st.markdown("**Countries to compare**")
    selected_country_codes = st.multiselect("Countries", options=available_country_codes,
        default=["IND"] + [c for c in available_country_codes[1:8] if c != "IND"], format_func=lambda c:available_country_names.get(c,c),
        label_visibility="collapsed")
    if not selected_country_codes:
        st.warning("Select at least one country."); st.stop()

    st.markdown("**Focus country** *(KPI cards + score)*")
    focus_country_code = st.selectbox("Focus", options=available_country_codes,
        format_func=lambda c:available_country_names.get(c,c), label_visibility="collapsed")
    focus_country_name = available_country_names.get(focus_country_code, focus_country_code)
    
    # Ensure focus country is in comparison list
    if focus_country_code not in selected_country_codes:
        selected_country_codes = [focus_country_code] + selected_country_codes

    st.markdown("**Year range**")
    available_years = sorted(full_world_bank_df["year"].dropna().astype(int).unique())
    min_year, max_year = int(available_years[0]), int(available_years[-1])
    selected_start_year, selected_end_year = st.slider("Years", min_year, max_year,
        (max(min_year, max_year-13), max_year), label_visibility="collapsed")

    st.markdown("**Page**")
    active_page = st.radio("Page",
        ["Overview","Economy","Health","Education","Environment","Gender","Digital","Comparator"],
        label_visibility="collapsed")

    st.markdown("---")

    filtered_display_df = filter_by_countries_and_years(full_world_bank_df, selected_country_codes, selected_start_year, selected_end_year)
    filtered_kpi_df = filter_by_countries_and_years(full_world_bank_df, [focus_country_code], selected_start_year, selected_end_year)

    # Live indicator panel — all 25 indicators for focus country
    st.markdown(f"**All indicators · {focus_country_name}**")
    sidebar_indicator_groups = {
        "Economy":    ["gdp_growth","gdp_per_capita","fdi_inflows","unemployment"],
        "Health":     ["life_expectancy","infant_mortality","hospital_beds","population"],
        "Education":  ["school_enrolment_primary","school_enrolment_secondary","education_expenditure"],
        "Environment":["electricity_access","renewable_energy","forest_area","clean_water_access"],
        "Gender":     ["female_labour","women_parliament","maternal_mortality","gender_parity"],
        "Digital":    ["internet_users"],
    }
    indicator_panel_html = []
    for group_name, group_indicators in sidebar_indicator_groups.items():
        indicator_panel_html.append(f'<div class="sidebar-section-label">{group_name}</div>')
        for indicator_col in group_indicators:
            display_cfg   = INDICATOR_DISPLAY_CONFIG[indicator_col]
            display_label = CSV_COLUMN_TO_LABEL[indicator_col]
            if indicator_col not in filtered_kpi_df.columns:
                indicator_panel_html.append(f'<div class="indicator-row"><div class="category-dot" style="background:#D3D1C7"></div><span class="indicator-name">{display_label}</span><span class="indicator-value">—</span></div>'); continue
            current_val, current_yr = get_latest_value(filtered_kpi_df, focus_country_code, indicator_col)
            prev_val = get_previous_year_value(filtered_kpi_df, focus_country_code, indicator_col, current_yr) if current_yr else None
            formatted_val = format_indicator_value(current_val, indicator_col)
            if current_val is None or prev_val is None:
                arrow_symbol, arrow_color = "—", "#888780"
            else:
                change = current_val - prev_val
                arrow_symbol = "▲" if change>0 else "▼"
                arrow_color  = "#0F6E56" if (change>0)==display_cfg["higher_is_better"] else "#A32D2D"
            indicator_panel_html.append(f'<div class="indicator-row"><div class="category-dot" style="background:{display_cfg["dot_color"]}"></div><span class="indicator-name">{display_label}</span><span class="indicator-value">{formatted_val}</span><span class="trend-arrow" style="color:{arrow_color}">{arrow_symbol}</span></div>')
    st.markdown("".join(indicator_panel_html), unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Source: world_bank_cleaned.csv")
    st.caption(f"Refreshed: {datetime.now().strftime('%H:%M')}")

# ══════════════════════════════════════════════════════════════════
# MAIN PAGE
# ══════════════════════════════════════════════════════════════════
st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
st.markdown(f"### {active_page} — {focus_country_name}")
st.caption(f"{selected_start_year}–{selected_end_year} · {len(selected_country_codes)} countries selected")
st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)

# ── ADIS Score ──
st.markdown('<div class="section-divider">Asian Development Intelligence Score</div>', unsafe_allow_html=True)
focus_adis_score, focus_pillar_scores = calculate_adis_score(filtered_kpi_df, focus_country_code)
grade_text, grade_color = get_development_grade(focus_adis_score)

all_country_scores = {cc: calculate_adis_score(filtered_display_df,cc)[0] for cc in selected_country_codes}
ranked_country_codes = sorted([cc for cc,s in all_country_scores.items() if s is not None], key=lambda cc:all_country_scores[cc], reverse=True)
focus_rank = ranked_country_codes.index(focus_country_code)+1 if focus_country_code in ranked_country_codes else "—"

previous_year_df = filter_by_countries_and_years(full_world_bank_df, [focus_country_code], selected_start_year-1, selected_end_year-1)
prev_adis_score, _ = calculate_adis_score(previous_year_df, focus_country_code)
if focus_adis_score and prev_adis_score:
    score_change = focus_adis_score - prev_adis_score
    score_change_text = f"{'▲' if score_change>0 else '▼'} {abs(score_change):.1f} pts vs last year"
else:
    score_change_text = "— no prior comparison"

ring_circumference = 251.2
ring_filled_length = ring_circumference*((focus_adis_score or 0)/100)
ring_empty_length  = ring_circumference - ring_filled_length
score_ring_svg = f'<svg width="90" height="90" viewBox="0 0 90 90"><circle cx="45" cy="45" r="40" fill="none" stroke="#B5D4F4" stroke-width="8"/><circle cx="45" cy="45" r="40" fill="none" stroke="#185FA5" stroke-width="8" stroke-dasharray="{ring_filled_length:.1f} {ring_empty_length:.1f}" stroke-linecap="round" transform="rotate(-90 45 45)"/><text x="45" y="41" text-anchor="middle" font-size="17" font-weight="700" fill="#0C447C">{int(focus_adis_score or 0)}</text><text x="45" y="56" text-anchor="middle" font-size="9" fill="#185FA5">/100</text></svg>'

pillar_bars_html = "".join([
    f'<div class="pillar-row"><span class="pillar-label" style="color:{p_cfg["pillar_color"]}">{p_name}</span><div class="pillar-track"><div class="pillar-bar" style="width:{int(focus_pillar_scores.get(p_name) or 0)}%;background:{p_cfg["pillar_color"]}"></div></div><span class="pillar-score">{int(focus_pillar_scores.get(p_name) or 0)}</span></div>'
    for p_name, p_cfg in ADIS_PILLARS.items()
])

st.markdown(f'<div class="adis-score-card"><div style="flex-shrink:0">{score_ring_svg}</div><div style="flex:1;min-width:0"><div class="adis-score-title">ADIS Score — {focus_country_name}</div><div class="adis-score-number">{focus_adis_score if focus_adis_score else "N/A"}</div><div class="adis-grade-label" style="color:{grade_color}">{grade_text}</div><div class="adis-rank-note">Ranked {focus_rank} of {len(ranked_country_codes)} countries · {score_change_text}</div></div><div style="min-width:200px">{pillar_bars_html}</div></div>', unsafe_allow_html=True)

valid_pillar_scores = {p:s for p,s in focus_pillar_scores.items() if s is not None}
if valid_pillar_scores:
    strongest_pillar = max(valid_pillar_scores, key=lambda p:valid_pillar_scores[p])
    weakest_pillar   = min(valid_pillar_scores, key=lambda p:valid_pillar_scores[p])
    ins1, ins2 = st.columns(2)
    with ins1: st.markdown(f'<div class="insight-box" style="background:#EAF3DE;border-left-color:#3B6D11"><div class="insight-title" style="color:#3B6D11">Strongest — {strongest_pillar} ({int(valid_pillar_scores[strongest_pillar])}/100)</div><div class="insight-body" style="color:#27500A">{focus_country_name} leads on {strongest_pillar.lower()} among selected countries.</div></div>', unsafe_allow_html=True)
    with ins2: st.markdown(f'<div class="insight-box" style="background:#FAEEDA;border-left-color:#854F0B"><div class="insight-title" style="color:#854F0B">Weakest — {weakest_pillar} ({int(valid_pillar_scores[weakest_pillar])}/100)</div><div class="insight-body" style="color:#633806">Most room to improve on {weakest_pillar.lower()} — lowest pillar score.</div></div>', unsafe_allow_html=True)

# ── 7 KPI Cards ──
st.markdown('<div class="section-divider">Headline KPI indicators</div>', unsafe_allow_html=True)
r1 = st.columns(4, gap="small")
with r1[0]: st.markdown(build_kpi_card_html("gdp_growth",       "blue",  "Economy",   filtered_kpi_df, focus_country_code), unsafe_allow_html=True)
with r1[1]: st.markdown(build_kpi_card_html("gdp_per_capita",   "blue",  "Economy",   filtered_kpi_df, focus_country_code), unsafe_allow_html=True)
with r1[2]: st.markdown(build_kpi_card_html("unemployment",     "blue",  "Economy",   filtered_kpi_df, focus_country_code), unsafe_allow_html=True)
with r1[3]: st.markdown(build_kpi_card_html("infant_mortality", "red",   "Alert",     filtered_kpi_df, focus_country_code), unsafe_allow_html=True)
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
r2 = st.columns(3, gap="small")
with r2[0]: st.markdown(build_kpi_card_html("life_expectancy",  "teal",  "Health",    filtered_kpi_df, focus_country_code), unsafe_allow_html=True)
with r2[1]: st.markdown(build_kpi_card_html("school_enrolment_primary", "purple","Education", filtered_kpi_df, focus_country_code), unsafe_allow_html=True)
with r2[2]: st.markdown(build_kpi_card_html("internet_users",   "amber", "Digital",   filtered_kpi_df, focus_country_code), unsafe_allow_html=True)
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ── Page charts ──
if active_page == "Overview":
    st.markdown('<div class="section-divider">Economy snapshot</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: render_trend_line_chart(filtered_display_df,"gdp_per_capita","GDP per capita over time","USD","blue")
    with c2: render_country_ranking_bar_chart(filtered_display_df,"unemployment","Latest unemployment","% of labour force","blue",higher_is_better=False,y_axis_suffix="%")
    st.markdown('<div class="section-divider">Development snapshot</div>', unsafe_allow_html=True)
    c3,c4 = st.columns(2)
    with c3: render_two_indicator_scatter(filtered_display_df,"gdp_per_capita","life_expectancy","Income vs life expectancy","GDP per capita","Life exp (yrs)","teal","population")
    with c4: render_two_indicator_scatter(filtered_display_df,"gdp_per_capita","school_enrolment_primary","Income vs primary enrolment","GDP per capita","Primary enrolment %","purple","population")
    st.markdown('<div class="section-divider">Alert indicators</div>', unsafe_allow_html=True)
    c5,c6,c7 = st.columns(3)
    with c5: render_country_ranking_bar_chart(filtered_display_df,"maternal_mortality","Maternal mortality","Deaths per 100k births","red",higher_is_better=False)
    with c6: render_country_ranking_bar_chart(filtered_display_df,"infant_mortality","Infant mortality","Deaths/1,000 births","red",higher_is_better=False)
    with c7: render_country_ranking_bar_chart(filtered_display_df,"internet_users","Internet users","% of population","amber",y_axis_suffix="%")

elif active_page == "Economy":
    st.markdown('<div class="section-divider">Growth trends</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: render_trend_line_chart(filtered_display_df,"gdp_growth","GDP growth trend","Annual %","blue","%")
    with c2: render_trend_line_chart(filtered_display_df,"population","Population trend","Total","blue")
    st.markdown('<div class="section-divider">Labour & investment</div>', unsafe_allow_html=True)
    c3,c4 = st.columns(2)
    with c3: render_trend_line_chart(filtered_display_df,"unemployment","Unemployment rate","% of labour force","blue","%")
    with c4: render_trend_line_chart(filtered_display_df,"fdi_inflows","FDI inflows","% of GDP","blue","%")
    st.markdown('<div class="section-divider">Inequality</div>', unsafe_allow_html=True)
    c5,c6 = st.columns(2)
    with c5: render_country_ranking_bar_chart(filtered_display_df,"fdi_inflows","FDI inflows","% of GDP","blue",y_axis_suffix="%")
    with c6: render_two_indicator_scatter(filtered_display_df,"gdp_per_capita","unemployment","Income vs unemployment","GDP per capita","Unemployment %","blue","population")

elif active_page == "Health":
    st.markdown('<div class="section-divider">Health outcomes</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: render_trend_line_chart(filtered_display_df,"life_expectancy","Life expectancy trend","Years","teal")
    with c2: render_trend_line_chart(filtered_display_df,"infant_mortality","Infant mortality trend","Deaths/1,000 births","red")
    st.markdown('<div class="section-divider">System capacity</div>', unsafe_allow_html=True)
    c3,c4 = st.columns(2)
    with c3: render_country_ranking_bar_chart(filtered_display_df,"hospital_beds","Hospital beds — latest","Per 1,000 people","teal")
    with c4: render_two_indicator_scatter(filtered_display_df,"hospital_beds","life_expectancy","Hospital beds vs life expectancy","Hospital beds","Life exp (yrs)","teal","population")

elif active_page == "Education":
    st.markdown('<div class="section-divider">Literacy & enrolment</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: render_trend_line_chart(filtered_display_df,"school_enrolment_primary","Primary enrolment trend","Gross %","purple","%")
    with c2: render_trend_line_chart(filtered_display_df,"school_enrolment_secondary","Secondary enrolment trend","Gross %","purple","%")
    st.markdown('<div class="section-divider">Secondary & spending</div>', unsafe_allow_html=True)
    c3,c4 = st.columns(2)
    with c3: render_trend_line_chart(filtered_display_df,"education_expenditure","Education expenditure trend","% of GDP","purple","%")
    with c4: render_two_indicator_scatter(filtered_display_df,"education_expenditure","school_enrolment_primary","Spend vs primary enrolment","Spend % GDP","Primary enrolment %","purple")

elif active_page == "Environment":
    st.markdown('<div class="section-divider">Energy & emissions</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: render_trend_line_chart(filtered_display_df,"renewable_energy","Renewable energy share","% of final energy","green","%")
    with c2: render_trend_line_chart(filtered_display_df,"forest_area","Forest area trend","% of land area","green","%")
    st.markdown('<div class="section-divider">Access & land</div>', unsafe_allow_html=True)
    c3,c4 = st.columns(2)
    with c3: render_country_ranking_bar_chart(filtered_display_df,"electricity_access","Electricity access","% of population","green",y_axis_suffix="%")
    with c4: render_country_ranking_bar_chart(filtered_display_df,"clean_water_access","Clean water access","% of population","teal",y_axis_suffix="%")
    st.markdown('<div class="section-divider">Forest cover</div>', unsafe_allow_html=True)
    render_country_ranking_bar_chart(filtered_display_df,"forest_area","Forest area — latest","% of land area","green",y_axis_suffix="%")

elif active_page == "Gender":
    st.markdown('<div class="section-divider">Labour & parliament</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: render_trend_line_chart(filtered_display_df,"female_labour","Female labour force","% of female 15+","pink","%")
    with c2: render_trend_line_chart(filtered_display_df,"women_parliament","Women in parliament","% of seats","pink","%")
    st.markdown('<div class="section-divider">Labour & parliament</div>', unsafe_allow_html=True)
    c3,c4 = st.columns(2)
    with c3: render_country_ranking_bar_chart(filtered_display_df,"women_parliament","Women in parliament","% of seats","pink",y_axis_suffix="%")
    with c4: render_trend_line_chart(filtered_display_df,"gender_parity","Gender parity index","Ratio F/M","pink")
    st.markdown('<div class="section-divider">Maternal health — alert</div>', unsafe_allow_html=True)
    render_country_ranking_bar_chart(filtered_display_df,"maternal_mortality","Maternal mortality — latest","Deaths per 100k births","red",higher_is_better=False)

elif active_page == "Digital":
    st.markdown('<div class="section-divider">Internet access</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: render_trend_line_chart(filtered_display_df,"internet_users","Internet users trend","% of population","amber","%")
    with c2: render_country_ranking_bar_chart(filtered_display_df,"internet_users","Internet users — latest","% of population","amber",y_axis_suffix="%")
    st.markdown('<div class="section-divider">Digital vs economic development</div>', unsafe_allow_html=True)
    render_two_indicator_scatter(filtered_display_df,"gdp_per_capita","internet_users","Income vs digital access (bubble=pop)","GDP per capita (USD)","Internet users %","amber","population")

elif active_page == "Comparator":
    st.markdown('<div class="section-divider">ADIS score ranking</div>', unsafe_allow_html=True)
    comparison_rows = []
    for cc in selected_country_codes:
        tot, ps = calculate_adis_score(filtered_display_df, cc)
        row = {"Country":available_country_names.get(cc,cc),"ADIS Score":tot,"Grade":get_development_grade(tot)[0]}
        for pn in ADIS_PILLARS: row[pn] = ps.get(pn)
        comparison_rows.append(row)
    comparison_df = pd.DataFrame(comparison_rows).sort_values("ADIS Score",ascending=False).fillna("N/A")
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    st.markdown('<div class="section-divider">Cross-indicator comparisons</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: render_two_indicator_scatter(filtered_display_df,"life_expectancy","internet_users","Health vs digital","Life exp (yrs)","Internet %","teal")
    with c2: render_two_indicator_scatter(filtered_display_df,"gdp_per_capita","school_enrolment_primary","Income vs education","GDP per capita","Primary enrolment %","purple","population")

st.markdown("---")
st.caption("Data: world_bank_cleaned.csv · ADIS score is a weighted composite — not an official metric")