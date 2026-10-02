"""
Care Transition Efficiency & Placement Outcome Analytics
HHS Unaccompanied Alien Children (UAC) Program — Enterprise Analytics Platform
"""

import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="UAC Care Transition Analytics",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "HHS_Unaccompanied_Alien_Children_Program.csv")

# =========================================================
# COLORS
# =========================================================
NAVY, BLUE, TEAL, AMBER = "#0F3460", "#2E5EAA", "#1B9C85", "#E1A731"
RED, GREEN, PURPLE = "#C0392B", "#1E8449", "#6C5CE7"
BG, CARD, TEXT, MUTED, GRID = "#F5F7FB", "#FFFFFF", "#1B2A4A", "#65708A", "#E7EBF3"

STAGE_COLORS = {
    "apprehended": BLUE,
    "cbp_custody": TEAL,
    "transferred_out_cbp": AMBER,
    "hhs_care": RED,
    "discharged": PURPLE,
}
DISPLAY_NAMES = {
    "apprehended": "Apprehended",
    "cbp_custody": "CBP Custody",
    "transferred_out_cbp": "Transferred",
    "hhs_care": "HHS Care",
    "discharged": "Discharged",
}

# =========================================================
# GLOBAL CSS
# =========================================================
st.html(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{ font-family: "Inter", sans-serif; }}

/* Dev UI Cleanup */
header[data-testid="stHeader"] {{
    background: transparent !important;
    height: 3.5rem !important;
    z-index: 100 !important;
}}
div[data-testid="stToolbar"] {{ display: none !important; }}
div[data-testid="stDecoration"] {{ display: none !important; }}
#MainMenu {{ visibility: hidden !important; }}
footer {{ visibility: hidden !important; }}

/* =========================================================
   PERMANENTLY OPEN SIDEBAR & HIDE ALL TOGGLES
   ========================================================= */

/* Keep sidebar visible, docked, and impossible to collapse */
section[data-testid="stSidebar"],
div[data-testid="stSidebar"] {{
    display: block !important;
    visibility: visible !important;
    transform: none !important;
    position: relative !important;
    left: 0 !important;
    width: 310px !important;
    min-width: 310px !important;
    max-width: 310px !important;
    opacity: 1 !important;
    background: linear-gradient(180deg, #0B2447 0%, #102F59 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
    z-index: 100 !important;
}}

/* Permanently hide all collapse buttons (<<) */
button[data-testid="stSidebarCollapseButton"],
button[aria-label="Close sidebar"],
section[data-testid="stSidebar"] button[kind="header"],
div[data-testid="stSidebarHeader"] button {{
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
}}

/* Permanently hide all reopen/expand buttons (>) */
div[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
button[aria-label="Open sidebar"],
button[data-testid="stSidebarCollapsedControl"] {{
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
}}

/* Ensure responsive breakpoints cannot force-collapse the sidebar */
@media (max-width: 9999px) {{
    section[data-testid="stSidebar"],
    div[data-testid="stSidebar"] {{
        display: block !important;
        visibility: visible !important;
        transform: none !important;
        width: 310px !important;
        min-width: 310px !important;
        max-width: 310px !important;
    }}
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {{
        display: none !important;
    }}
}}

/* =========================================================
   SIDEBAR BRAND CARD & WIDGET REFINEMENTS
   ========================================================= */

/* Sidebar Header Branding Card */
.sidebar-brand {{
    padding: 14px 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
}}
.sidebar-brand-icon {{
    font-size: 26px;
    line-height: 1;
}}
.sidebar-brand-title {{
    font-size: 15px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.2px;
    line-height: 1.2;
    margin: 0;
}}
.sidebar-brand-sub {{
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #9FB6E0;
    margin-top: 3px;
}}

/* Metric Checkbox Toggles & Spacing */
section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label {{
    font-size: 13.5px !important;
    font-weight: 500 !important;
    color: #E2E8F0 !important;
    padding: 2px 0 !important;
}}
section[data-testid="stSidebar"] div[data-testid="stCheckbox"] p {{
    font-size: 13.5px !important;
    font-weight: 500 !important;
}}
section[data-testid="stSidebar"] div[data-testid="stCheckbox"] {{
    margin-bottom: 6px !important;
}}

/* Date Slider Labels */
section[data-testid="stSidebar"] div[data-testid="stSlider"] div[data-testid="stTickBarMin"],
section[data-testid="stSidebar"] div[data-testid="stSlider"] div[data-testid="stTickBarMax"],
section[data-testid="stSidebar"] div[data-testid="stSlider"] [data-testid="stThumbValue"] {{
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #CBD5E1 !important;
}}

/* =========================================================
   BASE LAYOUT & TYPOGRAPHY
   ========================================================= */

.stApp {{
    background: radial-gradient(circle at top right, rgba(46,94,170,0.07), transparent 28%),
                linear-gradient(180deg, #F8FAFD 0%, #F5F7FB 100%);
}}
div.block-container {{ padding-top: 1.4rem; padding-bottom: 2rem; max-width: 1360px; }}

section[data-testid="stSidebar"] p, 
section[data-testid="stSidebar"] span, 
section[data-testid="stSidebar"] label {{
    color: #F4F7FB;
}}
section[data-testid="stSidebar"] label {{ font-weight: 600; }}
section[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,0.14); }}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{ font-size: 13px; font-weight: 600; color: #E2E8F0; }}

.sidebar-card-title {{
    font-size: 11.5px; font-weight: 800; letter-spacing: 0.06em; text-transform: uppercase;
    color: #9FB6E0; margin-bottom: 8px; margin-top: 14px;
}}

/* Hero Banner */
.hero {{
    position: relative; overflow: hidden;
    background: linear-gradient(135deg, #0B2447 0%, #123F73 52%, #176C76 100%);
    border-radius: 20px; padding: 30px 36px; margin-bottom: 20px; color: white;
    box-shadow: 0 18px 45px rgba(15,52,96,0.15);
}}
.hero::before {{ content:""; position:absolute; width:280px; height:280px; border-radius:50%;
    background: rgba(255,255,255,0.06); right:-80px; top:-110px; }}
.hero::after {{ content:""; position:absolute; width:180px; height:180px; border-radius:50%;
    background: rgba(255,255,255,0.045); right:120px; bottom:-100px; }}
.hero-content {{ position: relative; z-index: 2; }}
.hero-eyebrow {{ font-size:12px; font-weight:800; letter-spacing:1.6px; text-transform:uppercase; opacity:0.82; margin-bottom:8px; color:#A5F3FC; }}
.hero-title {{ font-size: clamp(25px, 2.5vw, 36px); line-height:1.2; font-weight:800; margin:0; letter-spacing:-0.5px; }}
.hero-subtitle {{ margin-top:10px; max-width:920px; font-size:14.5px; line-height:1.6; color:rgba(255,255,255,0.88); }}
.hero-pipeline {{ display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-top:18px; }}
.hero-pill {{ padding:6px 14px; border-radius:999px; background:rgba(255,255,255,0.12);
    border:1px solid rgba(255,255,255,0.18); font-size:12px; font-weight:700; color:rgba(255,255,255,0.95); }}
.hero-arrow {{ color:rgba(255,255,255,0.45); font-weight:700; }}

/* KPI Cards */
.kpi-card {{
    position:relative; background:rgba(255,255,255,0.98); border:1px solid rgba(15,52,96,0.08);
    border-radius: 16px; padding: 18px 20px 16px; min-height: 120px;
    box-shadow: 0 8px 20px rgba(15,52,96,0.05); overflow:hidden;
    transition: transform 0.15s ease, box-shadow 0.15s ease; cursor: help;
}}
.kpi-card:hover {{ transform: translateY(-3px); box-shadow: 0 14px 28px rgba(15,52,96,0.10); }}
.kpi-card::after {{ content:""; position:absolute; width:80px; height:80px; border-radius:50%;
    right:-30px; bottom:-35px; background:var(--kpi-accent); opacity:0.07; }}
.kpi-accent {{ position:absolute; left:0; top:0; bottom:0; width:4.5px; background:var(--kpi-accent); border-radius:16px 0 0 16px; }}
.kpi-top {{ display:flex; align-items:center; justify-content:space-between; gap:8px; }}
.kpi-icon {{ width:32px; height:32px; display:flex; align-items:center; justify-content:center;
    border-radius:8px; background:rgba(0,0,0,0.04); color:var(--kpi-accent); font-size:16px; }}
.kpi-label {{ color:var(--muted); font-size:11.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.04em; }}
.kpi-value {{ margin-top:10px; color:var(--text); font-size:27px; font-weight:800; letter-spacing:-0.4px; line-height:1.1; }}
.kpi-sub {{ margin-top:4px; font-size:10.8px; color:var(--muted); font-weight:500; }}
:root {{ --text:{TEXT}; --muted:{MUTED}; }}

/* Alerts */
.alert-card {{ border-radius:12px; padding:13px 18px; margin:10px 0; display:flex; align-items:center; gap:12px; border:1px solid; }}
.alert-danger {{ background:#FFF5F5; border-color:#FED7D7; color:#9B1C1C; }}
.alert-success {{ background:#F0FDF4; border-color:#BBF7D0; color:#166534; }}
.alert-icon {{ font-size:18px; }}
.alert-text {{ font-size:13.5px; line-height:1.45; font-weight: 500; }}

/* Section Titles */
.section-title {{ font-size:19px; font-weight:800; color:{TEXT}; margin:6px 0 2px; letter-spacing:-0.2px; }}
.section-subtitle {{ color:{MUTED}; font-size:13px; line-height:1.55; margin-bottom:14px; }}
.chart-title {{ font-size:14.5px; font-weight:700; color:{TEXT}; margin:16px 0 4px; }}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{ gap:4px; border-bottom:1px solid {GRID}; }}
.stTabs [data-baseweb="tab"] {{ height:44px; background:transparent; border-radius:8px 8px 0 0;
    padding:0 18px; color:{MUTED}; font-weight:700; font-size:14px; }}
.stTabs [aria-selected="true"] {{ background:{CARD}; color:{NAVY} !important; border-bottom:3px solid {BLUE}; }}

/* Plotly Wrapper */
div[data-testid="stPlotlyChart"] {{
    background: rgba(255,255,255,0.9); border:1px solid rgba(15,52,96,0.06); border-radius:16px;
    padding:8px; box-shadow:0 4px 16px rgba(15,52,96,0.03);
}}
div[data-testid="stDataFrame"] {{ border-radius:12px; overflow:hidden; border:1px solid rgba(15,52,96,0.08); }}

.app-footer {{ margin-top:36px; padding:18px 4px 6px; border-top:1px solid {GRID}; color:{MUTED}; font-size:12px; text-align:center; }}

/* Pull the sidebar content to start right at the top */
section[data-testid="stSidebar"] div.block-container {{
    padding-top: 1rem !important;
}}

/* Top Brand Section - Pulled higher with prominent typography */
.sidebar-brand {{
    padding: 12px 14px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    margin-top: 0 !important;
    margin-bottom: 22px;
    display: flex;
    align-items: center;
    gap: 12px;
}}
.sidebar-brand-icon {{
    font-size: 28px;
    line-height: 1;
}}
.sidebar-brand-title {{
    font-size: 16.5px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.3px;
    line-height: 1.2;
    margin: 0;
}}
.sidebar-brand-sub {{
    font-size: 10.5px;
    font-weight: 800;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #9FB6E0;
    margin-top: 4px;
}}

/* Section Titles (DATE RANGE, METRIC TOGGLES, ALERT THRESHOLDS) */
.sidebar-card-title {{
    font-size: 13.5px !important;
    font-weight: 800 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #A5F3FC !important;
    margin-top: 22px !important;
    margin-bottom: 10px !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}}

/* Widget Main Labels */
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
    font-size: 14.5px !important;
    font-weight: 700 !important;
    color: #F1F5F9 !important;
}}

/* Remove top padding and hide empty header container in sidebar */
section[data-testid="stSidebar"] div.block-container {{
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
}}

section[data-testid="stSidebarHeader"],
div[data-testid="stSidebarHeader"] {{
    display: none !important;
    height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}}

/* Tighten the brand title element spacing */
.sidebar-brand {{
    margin-top: 0 !important;
    margin-bottom: 10px !important;
    padding-top: 0 !important;
}}

/* Strip any lingering background boxes inside the sidebar header and content */
section[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"],
div[data-testid="stSidebarHeader"],
header[data-testid="stSidebarHeader"],
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:first-child {{
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}

.sidebar-brand {{
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}}

/* =========================================================
   SIDEBAR TYPOGRAPHY & FONT HIERARCHY ENHANCEMENT
   ========================================================= */

/* Top Brand Section - Larger & More Prominent */
.sidebar-brand-icon {{
    font-size: 32px !important;
    line-height: 1 !important;
}}

.sidebar-brand-title {{
    font-size: 19px !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    letter-spacing: -0.3px !important;
    line-height: 1.15 !important;
    margin: 0 !important;
}}

.sidebar-brand-sub {{
    font-size: 11px !important;
    font-weight: 800 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #9FB6E0 !important;
    margin-top: 4px !important;
}}

/* Section Titles (DATE RANGE, METRIC TOGGLES, ALERT THRESHOLDS) */
.sidebar-card-title {{
    font-size: 14.5px !important;
    font-weight: 800 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #38BDF8 !important;
    margin-top: 18px !important;
    margin-bottom: 8px !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}}

/* Checkbox Labels (Metric Toggles) - Increased Readability */
section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label {{
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #F1F5F9 !important;
    padding: 2px 0 !important;
}}

section[data-testid="stSidebar"] div[data-testid="stCheckbox"] p {{
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #F1F5F9 !important;
}}

/* Helper / Caption text under toggles */
section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {{
    font-size: 12.5px !important;
    line-height: 1.4 !important;
    color: #94A3B8 !important;
}}

/* Slider Main Widget Labels (e.g., Low Transfer Efficiency alert) */
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
    font-size: 14.5px !important;
    font-weight: 700 !important;
    color: #E2E8F0 !important;
}}

/* Slider Dynamic Values (Min, Max, Current Thumb Value) */
section[data-testid="stSidebar"] div[data-testid="stSlider"] div[data-testid="stTickBarMin"],
section[data-testid="stSidebar"] div[data-testid="stSlider"] div[data-testid="stTickBarMax"],
section[data-testid="stSidebar"] div[data-testid="stSlider"] [data-testid="stThumbValue"] {{
    font-size: 13px !important;
    font-weight: 700 !important;
    color: #CBD5E1 !important;
}}

/* =========================================================
   SIDEBAR CONTENT TYPOGRAPHY SCALING
   ========================================================= */

/* 1. DATE RANGE & ALERT SLIDER VALUES (Jan 2023, Dec 2025, 0.40, 0.00, etc.) */
section[data-testid="stSidebar"] div[data-testid="stSlider"] div[data-testid="stTickBarMin"],
section[data-testid="stSidebar"] div[data-testid="stSlider"] div[data-testid="stTickBarMax"],
section[data-testid="stSidebar"] div[data-testid="stSlider"] [data-testid="stThumbValue"] {{
    font-size: 14px !important;
    font-weight: 700 !important;
    color: #F8FAFC !important;
}}

/* Date input display boxes if using st.date_input */
section[data-testid="stSidebar"] div[data-testid="stDateInput"] input {{
    font-size: 14.5px !important;
    font-weight: 600 !important;
    color: #FFFFFF !important;
}}

/* 2. METRIC TOGGLE CHECKBOX LABELS */
section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label {{
    font-size: 15.5px !important;
    font-weight: 600 !important;
    color: #F1F5F9 !important;
    padding: 3px 0 !important;
}}

section[data-testid="stSidebar"] div[data-testid="stCheckbox"] p {{
    font-size: 15.5px !important;
    font-weight: 600 !important;
    color: #F1F5F9 !important;
}}

/* Make the checkbox square slightly larger to balance the text */
section[data-testid="stSidebar"] div[data-testid="stCheckbox"] input[type="checkbox"] {{
    transform: scale(1.15) !important;
    margin-right: 4px !important;
}}

/* Helper/Caption text under metric toggles */
section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {{
    font-size: 13px !important;
    line-height: 1.45 !important;
    color: #94A3B8 !important;
}}

/* 3. ALERT THRESHOLD LABELS ("Low Transfer Efficiency alert (<)", etc.) */
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
    font-size: 14.5px !important;
    font-weight: 600 !important;
    color: #E2E8F0 !important;
    margin-bottom: 2px !important;
}}

/* Number inputs / slider container text */
section[data-testid="stSidebar"] input[type="number"],
section[data-testid="stSidebar"] div[data-testid="stNumberInput"] input {{
    font-size: 15px !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
}}

</style>
""")

# =========================================================
# PLOTLY & UI HELPERS
# =========================================================
PLOTLY_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
}



# =========================================================
# PLOTLY & UI HELPERS
# =========================================================
PLOTLY_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
}

def style_fig(fig, height=380, show_legend=None):
    current_title = fig.layout.title.text
    fig.update_layout(title=dict(text=current_title if current_title else ""))
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Inter, sans-serif", color=TEXT, size=12.5),
        title_font=dict(size=14.5, color=NAVY, family="Inter, sans-serif"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=15, r=15, t=20, b=45),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)"),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter"),
    )
    if show_legend is not None:
        fig.update_layout(showlegend=show_legend)
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=GRID, tickfont=dict(color=MUTED))
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=MUTED))
    return fig

def kpi_card(label, value, icon, accent, sub="", tooltip=""):
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return f"""
    <div class="kpi-card" style="--kpi-accent:{accent};" title="{tooltip}">
        <div class="kpi-accent"></div>
        <div class="kpi-top">
            <div class="kpi-label">{label}</div>
            <div class="kpi-icon">{icon}</div>
        </div>
        <div class="kpi-value">{value}</div>
        {sub_html}
    </div>
    """

def zebra_style(dframe: pd.DataFrame):
    def _stripe(row):
        bg = BG if row.name % 2 else "#FFFFFF"
        return [f"background-color:{bg}"] * len(row)
    styler = dframe.style.apply(_stripe, axis=1)
    float_cols = dframe.select_dtypes(include=["float64", "float32"]).columns
    if len(float_cols):
        styler = styler.format({c: "{:,.0f}" for c in float_cols})
    try:
        styler = styler.hide(axis="index")
    except Exception:
        pass
    return styler

# =========================================================
# DATA LOADING & COMPUTATION
# =========================================================
@st.cache_data
def load_and_process(path: str) -> pd.DataFrame:
    raw = pd.read_csv(path)
    df = raw.dropna(how="all").copy()
    df.columns = [c.strip() for c in df.columns]

    df = df.rename(columns={
        "Children apprehended and placed in CBP custody*": "apprehended",
        "Children in CBP custody": "cbp_custody",
        "Children transferred out of CBP custody": "transferred_out_cbp",
        "Children in HHS Care": "hhs_care",
        "Children discharged from HHS Care": "discharged",
    })

    df["hhs_care"] = df["hhs_care"].astype(str).str.replace(",", "").astype(float)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    df["transfer_efficiency_ratio"] = df["transferred_out_cbp"] / df["cbp_custody"].replace(0, np.nan)
    df["discharge_effectiveness"] = df["discharged"] / df["hhs_care"].replace(0, np.nan)

    df["cbp_stage_imbalance"] = df["apprehended"] - df["transferred_out_cbp"]
    df["hhs_stage_imbalance"] = df["transferred_out_cbp"] - df["discharged"]

    df["total_pipeline"] = df["cbp_custody"] + df["hhs_care"]
    df["backlog_change"] = df["total_pipeline"].diff()

    df["weekday"] = df["Date"].dt.day_name()
    df["is_weekend"] = df["Date"].dt.dayofweek >= 5
    df["month"] = df["Date"].dt.to_period("M").astype(str)

    roll_mean = df["discharged"].rolling(30).mean()
    roll_std = df["discharged"].rolling(30).std()
    df["outcome_stability_score"] = 1 - (roll_std / roll_mean)

    df["discharge_pct_change"] = df["discharged"].pct_change()
    df["sudden_drop"] = (df["discharge_pct_change"] <= -0.5) & (df["discharged"].shift() > 20)

    df["hhs_backlog_day"] = df["hhs_stage_imbalance"] > 0
    df["backlog_streak_id"] = (df["hhs_backlog_day"] != df["hhs_backlog_day"].shift()).cumsum()

    return df

def get_sustained_streaks(df: pd.DataFrame, min_days: int = 5) -> pd.DataFrame:
    streaks = (
        df[df["hhs_backlog_day"]]
        .groupby("backlog_streak_id")
        .agg(start=("Date", "min"), end=("Date", "max"), days=("Date", "count"),
             total_imbalance=("hhs_stage_imbalance", "sum"))
    )
    return streaks[streaks["days"] >= min_days].sort_values("days", ascending=False)

df_full = load_and_process(DATA_PATH)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.html("""
    <div style="margin:-1rem -1rem 18px -1rem; padding:24px 20px 16px 20px;
                background:rgba(255,255,255,0.05); border-bottom:1px solid rgba(255,255,255,0.1);">
        <div style="font-size:28px; line-height:1;">🧭</div>
        <div style="font-size:18px; font-weight:800; margin-top:8px; color:#FFFFFF;">UAC Care Analytics</div>
        <div style="font-size:11px; font-weight:700; color:#93C5FD; margin-top:4px; letter-spacing:0.06em; text-transform:uppercase;">
            PROCESS EFFICIENCY DASHBOARD
        </div>
    </div>
    """)

    st.html('<div class="sidebar-card-title">📅 Date Range</div>')
    min_date, max_date = df_full["Date"].min().date(), df_full["Date"].max().date()
    all_dates = pd.date_range(min_date, max_date, freq="D").date
    
    date_range = st.select_slider(
        "Select Date Range",
        options=all_dates,
        value=(min_date, max_date),
        format_func=lambda d: d.strftime("%b %Y"),
        label_visibility="collapsed"
    )

    st.html('<div class="sidebar-card-title">🎛️ Metric Toggles</div>')
    show_ter = st.checkbox("Transfer Efficiency Ratio", value=True)
    show_dei = st.checkbox("Discharge Effectiveness Index", value=True)
    show_throughput = st.checkbox("Pipeline Throughput", value=True)
    show_stability = st.checkbox("Outcome Stability Score", value=True)
    st.caption("Toggle metrics to customize KPI cards and their analytical charts.")

    st.html('<div class="sidebar-card-title">🚨 Alert Thresholds</div>')
    ter_alert_threshold = st.slider("Low Transfer Efficiency alert (<)", 0.0, 1.5, 0.4, 0.05)
    dei_alert_threshold = st.slider("Low Discharge Effectiveness alert (<)", 0.0, 0.05, 0.015, 0.001)
    backlog_streak_alert = st.slider("Sustained bottleneck alert (days ≥)", 3, 30, 5, 1)

    st.html("""
    <div style="height:18px;"></div>
    <hr>
    <div style="font-size:11px; opacity:0.65; line-height:1.5;">
        Source: U.S. HHS Program Data<br>Real-Time Transition Monitoring
    </div>
    """)

# =========================================================
# DATE FILTER
# =========================================================
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

df = df_full[(df_full["Date"].dt.date >= start_date) & (df_full["Date"].dt.date <= end_date)].copy()

if df.empty:
    st.warning("No data found for the selected date range. Please widen the selection.")
    st.stop()

# =========================================================
# HERO BANNER
# =========================================================
st.html("""
<div class="hero">
    <div class="hero-content">
        <div class="hero-eyebrow">U.S. Department of Health &amp; Human Services — Analytics Division</div>
        <div class="hero-title">Care Transition Efficiency &amp; Placement Outcome Analytics</div>
        <div class="hero-subtitle">
            HHS Unaccompanied Alien Children (UAC) Program — tracking longitudinal throughput,
            identifying structural custody bottlenecks, and monitoring placement effectiveness.
        </div>
        <div class="hero-pipeline">
            <span class="hero-pill">Apprehended</span><span class="hero-arrow">→</span>
            <span class="hero-pill">CBP Custody</span><span class="hero-arrow">→</span>
            <span class="hero-pill">HHS Care</span><span class="hero-arrow">→</span>
            <span class="hero-pill">Sponsor Placement</span>
        </div>
    </div>
</div>
""")

# =========================================================
# ALERT BANNERS
# =========================================================
recent = df.tail(14)
alerts = []
if recent["transfer_efficiency_ratio"].mean() < ter_alert_threshold:
    alerts.append(f"Transfer Efficiency Ratio averaged {recent['transfer_efficiency_ratio'].mean():.2f} "
                  f"over the past 14 days — below the configured threshold of {ter_alert_threshold:.2f}.")
if recent["discharge_effectiveness"].mean() < dei_alert_threshold:
    alerts.append(f"Discharge Effectiveness Index averaged {recent['discharge_effectiveness'].mean():.4f} "
                  f"over the past 14 days — below the configured threshold of {dei_alert_threshold:.4f}.")

streaks_all = get_sustained_streaks(df, min_days=backlog_streak_alert)
if not streaks_all.empty and streaks_all.iloc[0]["end"] >= df["Date"].max() - pd.Timedelta(days=7):
    top = streaks_all.iloc[0]
    alerts.append(f"Active sustained bottleneck detected: {int(top['days'])} days "
                  f"({top['start'].date()} → {top['end'].date()}) with net imbalance of {int(top['total_imbalance']):,} children.")

if alerts:
    for a in alerts:
        st.html(f"""<div class="alert-card alert-danger"><div class="alert-icon">⚠️</div>
                 <div class="alert-text">{a}</div></div>""")
else:
    st.html("""<div class="alert-card alert-success"><div class="alert-icon">✅</div>
             <div class="alert-text">All pipeline efficiency metrics are currently operating within nominal parameters.</div></div>""")

# =========================================================
# KPI CARDS
# =========================================================
throughput_overall = df["discharged"].sum() / df["apprehended"].sum() if df["apprehended"].sum() > 0 else np.nan

all_cards = [
    (show_ter, "Avg Transfer Efficiency", f"{df['transfer_efficiency_ratio'].mean():.3f}", "🔀", BLUE,
     "Transferred ÷ CBP custody", "Measures transfer velocity from CBP into HHS care."),
    (show_dei, "Avg Discharge Effectiveness", f"{df['discharge_effectiveness'].mean():.4f}", "🏠", RED,
     "Discharged ÷ HHS care", "Daily proportion of children in HHS care successfully placed with sponsors."),
    (show_throughput, "Pipeline Throughput", f"{throughput_overall:.2f}", "📈", TEAL,
     "Total discharged ÷ total apprehended", "Ratio > 1.0 indicates net system backlog reduction."),
    (show_stability, "Avg Outcome Stability", f"{df['outcome_stability_score'].mean():.3f}", "🎯", PURPLE,
     "1 − CV of daily discharges", "Measures day-to-day placement consistency (1.0 = absolute stability)."),
    (True, "Sustained Bottlenecks", f"{len(streaks_all)}", "🚧", AMBER,
     f"Periods ≥ {backlog_streak_alert} days", "Count of extended multi-day periods where inflows exceeded outflows."),
]
visible_cards = [c for c in all_cards if c[0]]
if visible_cards:
    cols = st.columns(len(visible_cards))
    for c, (_, label, value, icon, accent, sub, tip) in zip(cols, visible_cards):
        with c:
            st.html(kpi_card(label, value, icon, accent, sub, tip))
else:
    st.info("All metric toggles are deactivated in the sidebar.")

st.html('<div style="height:8px;"></div>')

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🔀 Care Pipeline Flow",
    "📈 Transfer & Discharge Efficiency",
    "🚧 Bottleneck Detection",
    "📊 Outcome Trend Analysis",
])

# ---- Tab 1: Care Pipeline Flow ----
with tab1:
    st.html('<div class="section-title">Care Pipeline Flow</div>'
            '<div class="section-subtitle">Longitudinal movement through apprehension, transfer, and discharge stages.</div>')

    fig = go.Figure()
    for col in ["apprehended", "transferred_out_cbp", "discharged"]:
        fig.add_trace(go.Scatter(x=df["Date"], y=df[col], name=DISPLAY_NAMES[col],
                                 line=dict(color=STAGE_COLORS[col], width=1.6)))
    style_fig(fig, height=400)
    st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG)

    col_a, col_b = st.columns(2)
    with col_a:
        st.html('<div class="chart-title">CBP Custody Load (Active Inventory)</div>')
        fig2 = px.line(df, x="Date", y="cbp_custody", color_discrete_sequence=[STAGE_COLORS["cbp_custody"]])
        fig2.update_yaxes(title="Children in custody")
        style_fig(fig2, height=320, show_legend=False)
        st.plotly_chart(fig2, width="stretch", config=PLOTLY_CONFIG)
    with col_b:
        st.html('<div class="chart-title">HHS Care Load (Active Inventory)</div>')
        fig3 = px.area(df, x="Date", y="hhs_care", color_discrete_sequence=[STAGE_COLORS["hhs_care"]])
        fig3.update_traces(fillcolor="rgba(192,57,43,0.12)")
        fig3.update_yaxes(title="Children in HHS care")
        style_fig(fig3, height=320, show_legend=False)
        st.plotly_chart(fig3, width="stretch", config=PLOTLY_CONFIG)

    st.html('<div class="section-title" style="margin-top:14px;">Pipeline Flow Snapshot (Period Totals)</div>')
    snap = pd.DataFrame({
        "Stage": ["Apprehended (→ CBP)", "Transferred (→ HHS)", "Discharged (→ Sponsor)"],
        "Total children": [df["apprehended"].sum(), df["transferred_out_cbp"].sum(), df["discharged"].sum()],
    })
    fig_snap = px.bar(snap, x="Stage", y="Total children", text="Total children", color="Stage",
                      color_discrete_sequence=[BLUE, AMBER, PURPLE])
    fig_snap.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    style_fig(fig_snap, height=330, show_legend=False)
    st.plotly_chart(fig_snap, width="stretch", config=PLOTLY_CONFIG)
    st.caption(
        "Note: Transferred and Discharged totals exceed Apprehended totals because the system was resolving a large "
        f"pre-existing backlog (HHS held ~{int(df_full['hhs_care'].iloc[0]):,} children at period onset)."
    )

# ---- Tab 2: Transfer & Discharge Efficiency ----
with tab2:
    st.html('<div class="section-title">Transfer &amp; Discharge Efficiency</div>'
            '<div class="section-subtitle">Evaluating custody handoff velocity and placement cadence.</div>')

    if show_ter:
        st.html('<div class="chart-title">Transfer Efficiency Ratio (CBP → HHS Velocity)</div>')
        fig_ter = go.Figure()
        fig_ter.add_trace(go.Scatter(x=df["Date"], y=df["transfer_efficiency_ratio"], name="Daily TER",
                                     line=dict(color=BLUE, width=1), opacity=0.35))
        fig_ter.add_trace(go.Scatter(x=df["Date"], y=df["transfer_efficiency_ratio"].rolling(30).mean(),
                                     name="30-day avg", line=dict(color=BLUE, width=2.5)))
        fig_ter.add_hline(y=1.0, line_dash="dash", line_color=MUTED)
        fig_ter.add_hline(y=ter_alert_threshold, line_dash="dot", line_color=RED,
                          annotation_text="Alert threshold", annotation_font_color=RED)
        style_fig(fig_ter, height=350)
        st.plotly_chart(fig_ter, width="stretch", config=PLOTLY_CONFIG)

    if show_dei:
        st.html('<div class="chart-title">Discharge Effectiveness Index (Sponsor Placement Rate)</div>')
        fig_dei = go.Figure()
        fig_dei.add_trace(go.Scatter(x=df["Date"], y=df["discharge_effectiveness"], name="Daily DEI",
                                     line=dict(color=RED, width=1), opacity=0.35))
        fig_dei.add_trace(go.Scatter(x=df["Date"], y=df["discharge_effectiveness"].rolling(30).mean(),
                                     name="30-day avg", line=dict(color=RED, width=2.5)))
        fig_dei.add_hline(y=dei_alert_threshold, line_dash="dot", line_color=RED,
                          annotation_text="Alert threshold", annotation_font_color=RED)
        style_fig(fig_dei, height=350)
        st.plotly_chart(fig_dei, width="stretch", config=PLOTLY_CONFIG)

    if show_throughput:
        st.html('<div class="chart-title">Monthly Pipeline Throughput Rate (Discharges ÷ Apprehensions)</div>')
        monthly = df.groupby("month").agg(entries=("apprehended", "sum"), exits=("discharged", "sum")).reset_index()
        monthly["throughput"] = monthly["exits"] / monthly["entries"].replace(0, np.nan)
        fig_thr = px.bar(monthly, x="month", y="throughput",
                         color=(monthly["throughput"] >= 1).map({True: "≥ 1.0 (Resolving backlog)", False: "< 1.0 (Backlog accumulating)"}),
                         color_discrete_map={"≥ 1.0 (Resolving backlog)": TEAL, "< 1.0 (Backlog accumulating)": RED})
        fig_thr.add_hline(y=1.0, line_dash="dash", line_color=MUTED)
        fig_thr.update_layout(legend_title="", xaxis_title="", yaxis_title="Throughput ratio")
        style_fig(fig_thr, height=350)
        st.plotly_chart(fig_thr, width="stretch", config=PLOTLY_CONFIG)

    st.html('<div class="section-title" style="margin-top:14px;">Weekday Performance Distribution</div>')
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_counts = df["weekday"].value_counts()
    valid_days = [d for d in weekday_order if weekday_counts.get(d, 0) >= 10]
    excluded_days = [d for d in weekday_order if d not in valid_days]
    weekday_stats = (
        df[df["weekday"].isin(valid_days)]
        .groupby("weekday")[["transfer_efficiency_ratio", "discharge_effectiveness"]]
        .mean().reindex(valid_days).reset_index()
    )
    col_a, col_b = st.columns(2)
    with col_a:
        st.html('<div class="chart-title">Avg Transfer Efficiency by Weekday</div>')
        fig_wd1 = px.bar(weekday_stats, x="weekday", y="transfer_efficiency_ratio", color_discrete_sequence=[BLUE])
        fig_wd1.update_layout(xaxis_title="", yaxis_title="")
        style_fig(fig_wd1, height=290, show_legend=False)
        st.plotly_chart(fig_wd1, width="stretch", config=PLOTLY_CONFIG)
    with col_b:
        st.html('<div class="chart-title">Avg Discharge Effectiveness by Weekday</div>')
        fig_wd2 = px.bar(weekday_stats, x="weekday", y="discharge_effectiveness", color_discrete_sequence=[RED])
        fig_wd2.update_layout(xaxis_title="", yaxis_title="")
        style_fig(fig_wd2, height=290, show_legend=False)
        st.plotly_chart(fig_wd2, width="stretch", config=PLOTLY_CONFIG)

    if excluded_days:
        st.caption(
            f"**{' and '.join(excluded_days)}** excluded — weekly agency reporting bundles weekend movements into "
            "Monday filings, leaving insufficient weekend records for isolated analysis."
        )

# ---- Tab 3: Bottleneck Detection ----
with tab3:
    st.html('<div class="section-title">Bottleneck Detection</div>'
            '<div class="section-subtitle">Surfacing localized flow disparities and extended accumulation phases.</div>')

    st.html('<div class="chart-title">CBP-Stage Imbalance (Apprehended − Transferred) · Red = Backlog Formation</div>')
    fig_cbp = go.Figure()
    fig_cbp.add_trace(go.Bar(x=df["Date"], y=df["cbp_stage_imbalance"],
                             marker_color=np.where(df["cbp_stage_imbalance"] > 0, RED, TEAL)))
    style_fig(fig_cbp, height=290, show_legend=False)
    st.plotly_chart(fig_cbp, width="stretch", config=PLOTLY_CONFIG)

    st.html('<div class="chart-title">HHS-Stage Imbalance (Transferred In − Discharged) · Red = Backlog Formation</div>')
    fig_hhs = go.Figure()
    fig_hhs.add_trace(go.Bar(x=df["Date"], y=df["hhs_stage_imbalance"],
                             marker_color=np.where(df["hhs_stage_imbalance"] > 0, RED, TEAL)))
    style_fig(fig_hhs, height=290, show_legend=False)
    st.plotly_chart(fig_hhs, width="stretch", config=PLOTLY_CONFIG)

    st.html('<div class="section-title" style="margin-top:14px;">Monthly Net Backlog Shift</div>'
            '<div class="section-subtitle">Total change in children held in system custody (CBP + HHS) by month.</div>')
    monthly_backlog = df.groupby("month")["backlog_change"].sum().reset_index()
    fig_backlog = px.bar(monthly_backlog, x="month", y="backlog_change",
                         color=(monthly_backlog["backlog_change"] >= 0).map({True: "Backlog growing", False: "Backlog shrinking"}),
                         color_discrete_map={"Backlog growing": RED, "Backlog shrinking": TEAL})
    fig_backlog.update_layout(legend_title="", xaxis_title="", yaxis_title="Net change (children)")
    style_fig(fig_backlog, height=350)
    st.plotly_chart(fig_backlog, width="stretch", config=PLOTLY_CONFIG)

    st.html(f'<div class="section-title" style="margin-top:14px;">Sustained Bottleneck Periods (≥ {backlog_streak_alert} consecutive days)</div>')
    if streaks_all.empty:
        st.info("No sustained bottleneck events exceed the current threshold in this date range.")
    else:
        display_streaks = streaks_all.copy()
        display_streaks["start"] = display_streaks["start"].dt.date
        display_streaks["end"] = display_streaks["end"].dt.date
        display_streaks.columns = ["Start Date", "End Date", "Duration (Days)", "Total Inflow Imbalance"]
        display_streaks = display_streaks.reset_index(drop=True)
        st.dataframe(zebra_style(display_streaks), hide_index=True, width="stretch")
        st.caption("Click any column header to sort table.")

# ---- Tab 4: Outcome Trend Analysis ----
with tab4:
    st.html('<div class="section-title">Outcome Trend Analysis</div>'
            '<div class="section-subtitle">Longitudinal stability and cross-stage system correlations.</div>')

    if show_stability:
        st.html('<div class="chart-title">Outcome Stability Score (30-Day Rolling Window)</div>')
        fig_stab = go.Figure()
        fig_stab.add_trace(go.Scatter(x=df["Date"], y=df["outcome_stability_score"],
                                      line=dict(color=PURPLE, width=1.8), name="Stability score"))
        fig_stab.add_hline(y=df["outcome_stability_score"].mean(), line_dash="dash", line_color=MUTED,
                           annotation_text="Period mean")
        fig_stab.update_yaxes(title="Stability score (higher = consistent)")
        style_fig(fig_stab, height=350, show_legend=False)
        st.plotly_chart(fig_stab, width="stretch", config=PLOTLY_CONFIG)

    st.html('<div class="section-title" style="margin-top:14px;">Significant Reunification Drops</div>')
    drops = df[df["sudden_drop"]][["Date", "discharged", "discharge_pct_change"]].copy()
    if drops.empty:
        st.info("No anomalous single-day drops (≥ 50% decrease) detected in the selected timeframe.")
    else:
        drops["Date"] = drops["Date"].dt.date
        drops["discharge_pct_change"] = (drops["discharge_pct_change"] * 100).round(1).astype(str) + "%"
        drops.columns = ["Event Date", "Discharges", "Day-over-Day Variance"]
        drops = drops.reset_index(drop=True)
        st.dataframe(zebra_style(drops), hide_index=True, width="stretch")
        st.caption("Click any column header to sort table.")

    st.html('<div class="section-title" style="margin-top:14px;">Pipeline Stage Correlation Matrix</div>')
    corr_cols = ["apprehended", "cbp_custody", "transferred_out_cbp", "hhs_care", "discharged"]
    corr = df[corr_cols].corr()
    corr.index = [DISPLAY_NAMES[c] for c in corr_cols]
    corr.columns = [DISPLAY_NAMES[c] for c in corr_cols]
    fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1, aspect="auto")
    fig_corr.update_xaxes(side="bottom", tickangle=0, automargin=True)
    fig_corr.update_yaxes(automargin=True)
    style_fig(fig_corr, height=420, show_legend=False)
    fig_corr.update_layout(margin=dict(t=20, l=15, r=15, b=70))
    st.plotly_chart(fig_corr, width="stretch", config=PLOTLY_CONFIG)

# =========================================================
# FOOTER
# =========================================================
st.html("""
<div class="app-footer">
    Data Source: U.S. Department of Health &amp; Human Services Program Reporting &nbsp;·&nbsp;
    Care Transition Efficiency &amp; Placement Outcome Analytics
</div>
""")