# 📊 Decoding a Decade: RTI Filing Pattern Analysis at HPCL (2014–2024)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)
![SQL](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Seaborn-11557c?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-27AE60?style=for-the-badge)

**An end-to-end data analytics project built during an internship at the RTI Department, Hindustan Petroleum Corporation Limited (HPCL)**

</div>

---

## 📌 Project Overview

During my internship in the **RTI (Right to Information) Department at HPCL**, I was tasked with analysing a decade of RTI filing data to help the department improve **transparency, compliance, and responsiveness**.

This project delivers a full analytical pipeline — from raw data to actionable business recommendations — covering:

- 📁 **6,080 RTI records** spanning 11 years (2014–2024)
- 🏭 **13 HPCL departments** including Mumbai Refinery, LPG Division (Indane), Retail Marketing, Vigilance, Projects & Pipelines, and more
- 🔍 **15 SQL analytical queries** on an SQLite database
- 📈 **14 production-quality visualisations** in HPCL brand colours
- 📊 **6-page Power BI dashboard** with 28 DAX measures
- 📄 **3 structured Jupyter notebooks** (data generation → EDA → SQL analysis)

---

## 🔑 Key Findings

| # | Finding | Metric |
|---|---------|--------|
| 1 | RTI filings grew steadily over the decade | **+66%** — 430 (2014) → 714 (2024) |
| 2 | COVID-19 caused a severe compliance breakdown | Dropped from **83.4% → 56.3%** in 2020 |
| 3 | Vigilance is the worst-performing department | **44.5% breach rate** on 30-day deadline |
| 4 | Projects & Pipelines also critical | **34.3% breach rate** |
| 5 | January, March & October are peak filing months | Together = **31%** of annual filings |
| 6 | Online filing adoption nearly doubled | **25.3% (2014) → 52.1% (2024)** |
| 7 | Section 8(1)(j) is the most cited rejection reason | **32.3%** of all rejections |
| 8 | 15.8% of RTIs escalate to First Appeals | Of those, **50%** are rejected again at appeal stage |
| 9 | Proactive disclosure can eliminate 20.7% of RTI load | 5 recurring categories → **~1,261 RTIs** reducible |
| 10 | Maharashtra accounts for 22% of all filers | Driven by HPCL HQ + Mumbai Refinery proximity |

---

## 🏗️ Project Structure

```
hpcl-rti-analytics/
│
├── 📁 data/
│   ├── raw/
│   │   └── hpcl_rti_2014_2024.csv          # Synthetic dataset — 6,080 records, 23 columns
│   └── processed/
│       ├── hpcl_rti_cleaned.csv             # Cleaned dataset — 29 columns with engineered features
│       └── hpcl_rti.db                      # SQLite database for analytical queries
│
├── 📓 notebooks/
│   ├── 01_data_generation.ipynb             # Dataset schema design & synthetic data generation
│   ├── 02_data_cleaning_eda.ipynb           # Full EDA — cleaning, feature engineering, 14 charts
│   └── 03_sql_analysis.ipynb               # 15 SQL queries with explanations & outputs
│
├── 🗄️ sql/
│   └── rti_analysis_queries.sql            # All 15 analytical queries (runs on SQLite/PostgreSQL)
│
├── 📊 visuals/
│   ├── 01_yearly_trend.png                 # RTI filing volume & YoY growth (2014–2024)
│   ├── 02_monthly_heatmap.png              # Month × Year filing intensity heatmap
│   ├── 03_monthly_pattern.png              # Peak month analysis
│   ├── 04_department_volume.png            # Department-wise RTI volume
│   ├── 05_department_compliance.png        # Compliance rate by department
│   ├── 06_compliance_trend.png             # Year-wise compliance & response time trend
│   ├── 07_disposal_breakdown.png           # Disposal type donut chart
│   ├── 08_rejection_reasons.png            # Section-wise rejection analysis
│   ├── 09_appeal_funnel.png                # RTI → First Appeal → CIC funnel
│   ├── 10_digital_adoption.png             # Online vs offline filing trend
│   ├── 11_covid_impact.png                 # COVID-19 impact — 2019 vs 2020 vs 2021
│   ├── 12_proactive_disclosure.png         # Section 4 proactive disclosure opportunity
│   ├── 13_pio_workload.png                 # PIO workload & performance scatter
│   ├── 14_state_distribution.png           # Geographic distribution of filers
│   └── PBI_P1–P6_*.png                     # Power BI dashboard page mockups (6 pages)
│
├── 📊 dashboard/
│   ├── hpcl_rti_dashboard.pbix             # Power BI dashboard file
│   ├── dax_measures.txt                    # All 28 DAX measures (ready to paste)
│   └── powerbi_build_guide.md              # Step-by-step Power BI build instructions
│
├── 🔧 scripts/
│   ├── generate_dataset.py                 # Synthetic data generation logic
│   ├── 02_cleaning_preprocessing.py        # Standalone cleaning script
│   ├── 03_sql_analysis.py                  # Standalone SQL runner
│   ├── 04_visualisations_p1.py             # Charts 1–5 generation
│   ├── 04_visualisations_p2.py             # Charts 6–14 generation
│   ├── 05_powerbi_mockups.py               # Dashboard mockup generation
│   └── generate_notebooks.py              # Notebook generator (nbformat)
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔄 Analysis Pipeline

```
Raw Dataset (6,080 records)
        │
        ▼
┌─────────────────────┐
│  Data Generation    │  → 23 columns, HPCL-specific distributions,
│  (Notebook 01)      │    seasonal patterns, COVID-year effects
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Cleaning & EDA     │  → 29 columns, compliance flags, breach days,
│  (Notebook 02)      │    14 charts, 10 analytical themes
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  SQL Analysis       │  → 15 queries on SQLite, covering volume,
│  (Notebook 03)      │    compliance, appeals, geography, COVID
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Power BI Dashboard │  → 6 pages, 28 DAX measures, cross-filtering,
│  (6 pages)          │    HPCL brand theme, executive-ready
└────────┬────────────┘
         │
         ▼
  Recommendations & Report
```

---

## 🗃️ Dataset Schema

The dataset models real RTI filing behaviour at HPCL with HPCL-specific departments, categories, and distributions.

| Column | Type | Description |
|--------|------|-------------|
| `RTI_ID` | String | Unique ID — format `HPCL-RTI-XXXXX` |
| `Filing_Date` | Date | Date the RTI was filed |
| `Year / Month / Quarter` | Int/String | Temporal breakdown fields |
| `Department` | String | HPCL department receiving the RTI |
| `Category` | String | Type of information sought |
| `Applicant_Type` | String | Individual / Journalist / NGO / Lawyer / Business |
| `State` | String | State from which RTI was filed |
| `Mode_of_Filing` | String | Online (RTI Portal) / Offline / By Post |
| `PIO_Assigned` | String | Public Information Officer handling the RTI |
| `Response_Time_Days` | Int | Days taken to respond |
| `Response_Status` | String | On-Time / Delayed / Pending |
| `Disposal_Type` | String | Info Provided / Partially Provided / Rejected / Transferred |
| `Rejection_Reason` | String | RTI Act Section cited (if rejected) |
| `First_Appeal_Filed` | String | Yes / No |
| `First_Appeal_Outcome` | String | Upheld / Partially Upheld / Rejected |
| `Second_Appeal_CIC` | String | Escalated to Central Information Commission |
| `Compliant_Response` | String | **Engineered** — Yes / No / Pending (30-day rule) |
| `Breach_Days` | Int | **Engineered** — Days past the 30-day deadline |
| `Financial_Year` | String | **Engineered** — Indian FY (e.g. FY 2023-24) |
| `Proactive_Disclosure_Candidate` | String | **Engineered** — Flagged for Section 4 disclosure |

**Engineered features** are added in Notebook 02 during the cleaning phase.

---

## 📈 Dashboard Preview

> Built in Power BI with HPCL brand colours — Navy Blue `#003087` · Gold `#F7B500`

| Page | Description |
|------|-------------|
| **P1 — Executive Overview** | 5 KPI cards + yearly trend + disposal donut. Senior management view. |
| **P2 — Filing Trends** | Month×Year heatmap + peak month bars + digital adoption stacked chart. |
| **P3 — Department Intelligence** | Volume + compliance bars + state geographic distribution. |
| **P4 — Compliance & Response** | Gauge + on-time vs breached by year + scatter plot + dept avg days. |
| **P5 — Appeal Analysis** | Funnel (RTI→Appeal→CIC) + first appeal outcomes + dept breakdown. |
| **P6 — Insights & Recommendations** | Proactive disclosure opportunity + 6 prioritised recommendations. |

*Dashboard mockup screenshots are in `visuals/PBI_P*.png`*

---

## 💡 Recommendations Delivered

| Priority | Recommendation |
|----------|----------------|
| 🔴 **HIGH** | Dedicate additional PIO capacity to Vigilance — set 21-day internal SLA |
| 🔴 **HIGH** | Proactively publish 5 top categories under Section 4 RTI Act — eliminates 20.7% load |
| 🟡 **MEDIUM** | Pre-clear RTI backlog before March & October peak months |
| 🟡 **MEDIUM** | Promote RTI Online Portal; target 70% online filing by 2026 |
| 🟡 **MEDIUM** | Review rejection and disposal quality to cut 50% re-rejection rate at First Appeal |
| 🟢 **LOW** | Build RTI continuity protocol for disruption scenarios (post-COVID learning) |

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/hpcl-rti-analytics.git
cd hpcl-rti-analytics
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the notebooks in order
```bash
jupyter notebook
```
Open and run in this sequence:
1. `notebooks/01_data_generation.ipynb`
2. `notebooks/02_data_cleaning_eda.ipynb`
3. `notebooks/03_sql_analysis.ipynb`

> **Note:** Each notebook saves its outputs (CSV, DB, charts) to the correct directories automatically. Run them in order for full reproducibility.

### 4. Run SQL queries standalone
```bash
# Open the SQL file in DB Browser for SQLite
# or run via Python:
python3 -c "
import sqlite3, pandas as pd
conn = sqlite3.connect('data/hpcl_rti.db')
result = pd.read_sql_query('SELECT Year, COUNT(*) FROM rti_data GROUP BY Year', conn)
print(result)
conn.close()
"
```

### 5. Open the Power BI Dashboard
- Open `dashboard/hpcl_rti_dashboard.pbix` in **Power BI Desktop**
- Refresh the data source if prompted (point to `data/processed/hpcl_rti_cleaned.csv`)

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.10+** | Data generation, cleaning, EDA, visualisations |
| **Pandas & NumPy** | Data manipulation and feature engineering |
| **Matplotlib & Seaborn** | All 14 production-quality charts |
| **SQLite + SQL** | Analytical query layer — 15 queries |
| **Power BI Desktop** | Interactive 6-page dashboard |
| **nbformat** | Programmatic Jupyter notebook generation |
| **Jupyter Notebook** | Analysis documentation and presentation |
| **Git & GitHub** | Version control and portfolio hosting |

---

## 📂 SQL Queries Index

All 15 queries in `sql/rti_analysis_queries.sql` and `notebooks/03_sql_analysis.ipynb`:

| Query | Analysis |
|-------|---------|
| Q1 | Year-wise RTI volume & YoY growth rate |
| Q2 | Monthly filing pattern — peak month identification |
| Q3 | Department-wise volume, share & compliance rate |
| Q4 | Top RTI categories — most frequently filed |
| Q5 | Year-wise compliance rate trend (30-day deadline) |
| Q6 | Disposal type breakdown — overall & year-wise |
| Q7 | Section-wise rejection reason analysis |
| Q8 | RTI appeal funnel — filing → first appeal → CIC |
| Q9 | First appeal outcome distribution |
| Q10 | Departments with highest breach (non-compliance) rate |
| Q11 | PIO workload & individual compliance performance |
| Q12 | State-wise geographic distribution (Top 10) |
| Q13 | Digital adoption — online vs offline trend by year |
| Q14 | COVID-19 impact — 2019 vs 2020 vs 2021 comparison |
| Q15 | Proactive disclosure candidates under Section 4 |

---

## 📋 About This Project

**Context:** This project was completed during a one-month internship at the **RTI Department, Hindustan Petroleum Corporation Limited (HPCL)**. The objective was to analyse historical RTI filing patterns to help the department improve transparency, reduce compliance breaches, and identify opportunities for proactive disclosure under Section 4 of the RTI Act, 2005.

**Dataset Note:** The dataset used in this project is a realistic synthetic dataset modelled on HPCL's organisational structure, RTI filing behaviour observed during the internship, and public RTI data trends for large Indian PSUs. All personally identifiable information is anonymised.

**RTI Act, 2005 Reference:**
- **Section 4** — Obligations of public authorities to proactively disclose information
- **Section 8** — Exemptions from disclosure (cited in rejection analysis)
- **30-day deadline** — Legal mandate for public authorities to respond to RTI applications

---

## 📬 Contact

**Shreyansh**
- 🔗 [LinkedIn](https://linkedin.com/in/yourprofile)
- 💻 [GitHub](https://github.com/yourusername)
- 📧 your.email@example.com

---

<div align="center">

*Built with 💙 during an internship at HPCL | Tools: Python · SQL · Power BI*

⭐ Star this repo if you found it useful!

</div>
