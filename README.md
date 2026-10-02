# Care Transition Efficiency & Placement Outcome Analytics

A process efficiency and bottleneck analytics dashboard built on operational data from the U.S. Department of Health and Human Services' Unaccompanied Alien Children (UAC) Program.

The UAC Program manages a multi-stage care and reunification pipeline:  
**Apprehension & CBP Custody → Transfer to HHS Care → Sheltering & Case Management → Discharge & Reunification with a Vetted Sponsor.**

This project reframes public operational records from simple aggregate counts into an **interactive decision-support and workflow analytics platform** — tracking stage transition velocity, pipeline capacity strain, and reunification stability.

---

## 🌐 Live Application

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://care-transition-analytics-app.streamlit.app/)

The interactive dashboard is deployed on Streamlit Community Cloud:  
👉 **[care-transition-analytics-app.streamlit.app](https://care-transition-analytics-app.streamlit.app/)**

---

## 📂 Repository Structure

```text
Care-Transition-Analytics-WebApp/
├── app/
│   └── uac_app/
│       ├── .streamlit/
│       │   └── config.toml                          # Streamlit UI theme and server configuration
│       ├── data/
│       │   └── HHS_Unaccompanied_Alien_Children_Program.csv # Longitudinal operational dataset (2023–2025)
│       └── app.py                                   # Streamlit dashboard application & analytics engine
├── UAC_Care_Transition_Analysis.ipynb               # Exploratory data analysis & prototyping notebook
├── requirements.txt                                 # Production dependencies
├── .gitignore                                       # Git ignore rules (venv, bytecode, runtime cache)
└── README.md                                        # Project documentation & operational KPI dictionary
```

---

## 📊 Core Operational KPIs

| KPI | Formula | Analytical Focus |
|---|---|---|
| **Transfer Efficiency Ratio (TER)** | Transferred out of CBP ÷ CBP custody | Inter-agency handover velocity from CBP to HHS facilities. |
| **Discharge Effectiveness Index (DEI)** | Discharged ÷ HHS care population | Daily operational throughput toward vetted sponsor placement. |
| **Pipeline Throughput Rate** | Total discharged ÷ Total apprehended (period) | Net intake-to-reunification capacity balance across the care pipeline. |
| **Stage Backlog Accumulation** | Day-over-day change in total pipeline population (CBP custody + HHS care); tracked per-stage | Dynamic load monitoring and structural custody bottleneck identification. |
| **Outcome Stability Score** | 1 − (30-day rolling std ÷ mean of daily discharges) | Placement predictability, cadence stability, and volatility reduction. |

---

## 🛠️ Dashboard Architecture & Modules

1. **Executive Pipeline Summary & Flow Visualization:** Longitudinal intake volumes, bed occupancy levels, current custody loads, and stage transition funnels.
2. **Transfer & Discharge Efficiency Panels:** Rolling 7-day and 30-day efficiency metrics (TER and DEI), monthly throughput distributions, and weekday vs. weekend handover performance.
3. **Bottleneck Detection Engine:** Stage-level capacity imbalances, monthly backlog delta charts, and sustained bottleneck alerts (periods where backlog accumulation $\ge$ threshold days).
4. **Outcome Trend & Stability Analysis:** 30-day rolling stability metrics, sudden-drop event logs, and inter-stage correlation heatmaps.

*User controls include dynamic date-range filtering, metric visibility toggles, and configurable alert threshold parameters with responsive alert banners.*

---

## 💻 Local Setup & Execution

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Prsharma2112006/Care-Transition-Analytics-WebApp.git](https://github.com/Prsharma2112006/Care-Transition-Analytics-WebApp.git)
   cd Care-Transition-Analytics-WebApp
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the dashboard:**
   ```bash
   streamlit run app/uac_app/app.py
   ```

---

## 🚀 Deployment (Streamlit Community Cloud)

This application is deployed via [Streamlit Community Cloud](https://share.streamlit.io/):

- **Repository:** `Prsharma2112006/Care-Transition-Analytics-WebApp`
- **Branch:** `main`
- **Main file path:** `app/uac_app/app.py`
- **Live URL:** [care-transition-analytics-app.streamlit.app](https://care-transition-analytics-app.streamlit.app/)

---

## 📈 Data Governance & Source

- **Source:** U.S. Department of Health and Human Services (HHS) Unaccompanied Alien Children Program operational releases.
- **Coverage:** January 2023 – December 2025.
- **Metrics Tracked:** Apprehensions, CBP custody counts, transfers to HHS care, active HHS bed capacity, and sponsor reunification discharges.

---

## 📋 Project Deliverables

- [x] Streamlit analytics dashboard (`app/uac_app/app.py`)
- [x] Streamlit Community Cloud production deployment
- [x] Exploratory Data Analysis & statistical reporting (`UAC_Care_Transition_Analysis.ipynb`)
- [ ] Policy insights and recommendations executive briefing