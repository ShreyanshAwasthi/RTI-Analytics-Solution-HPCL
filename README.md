# 📊 Decoding a Decade: RTI Filing Pattern Analysis at HPCL (2014–2024)

An end-to-end **data analytics project** built during an internship at the **RTI Department, Hindustan Petroleum Corporation Limited (HPCL)**.  
This project analyzes a decade of RTI filing data to uncover patterns in **filing volume, compliance, appeals, rejection reasons, digital adoption, department performance, and proactive disclosure opportunities**.

---

## 📌 Project Overview

During my internship in the **RTI (Right to Information) Department at HPCL**, I worked on analyzing historical RTI filing data to help improve **transparency, compliance, and responsiveness**.

This project delivers a full analytical pipeline — from raw data to actionable business recommendations — covering:

- 📁 **6,080 RTI records** spanning 11 years (2014–2024)
- 🏭 **13 HPCL departments** including Mumbai Refinery, LPG Division (Indane), Retail Marketing, Vigilance, Projects & Pipelines, and more
- 🔍 **15 SQL analytical queries** on an SQLite database
- 📈 **14 production-quality visualisations** in HPCL brand colours
- 📊 **6-page Power BI dashboard** with **28 DAX measures**
- 📄 **3 structured Jupyter notebooks** covering data generation, EDA, and SQL analysis

---

## 🎯 Business Objectives

- Analyze RTI filing trends across years, months, and departments
- Measure compliance with the 30-day RTI response deadline
- Identify departments with the highest breach rates
- Study rejection reasons and appeal outcomes
- Evaluate online vs offline filing adoption
- Highlight opportunities for **Section 4 proactive disclosure**
- Support better decision-making through dashboards and SQL analysis

---

## 🔑 Key Findings

| # | Finding | Metric |
|---|---------|--------|
| 1 | RTI filings grew steadily over the decade | **+66%** — 430 (2014) → 714 (2024) |
| 2 | COVID-19 caused a severe compliance breakdown | Dropped from **83.4% → 56.3%** in 2020 |
| 3 | Vigilance is the worst-performing department | **44.5% breach rate** on the 30-day deadline |
| 4 | Projects & Pipelines also critical | **34.3% breach rate** |
| 5 | January, March & October are peak filing months | Together = **31%** of annual filings |
| 6 | Online filing adoption nearly doubled | **25.3% (2014) → 52.1% (2024)** |
| 7 | Section 8(1)(j) is the most cited rejection reason | **32.3%** of all rejections |
| 8 | 15.8% of RTIs escalate to First Appeals | Of those, **50%** are rejected again at appeal stage |
| 9 | Proactive disclosure can eliminate 20.7% of RTI load | 5 recurring categories → **~1,261 RTIs** reducible |
| 10 | Maharashtra accounts for 22% of all filers | Driven by HPCL HQ + Mumbai Refinery proximity |

---

## 📂 Dataset Overview

The dataset models real RTI filing behaviour at HPCL with HPCL-specific departments, categories, and distributions. It includes:

- Filing details
- Department allocation
- Applicant information
- Geographic information
- Filing mode
- Response time and status
- Disposal outcome
- Rejection reason
- Appeal tracking
- Engineered compliance features

### Important fields

- `RTI_ID` — Unique ID in the format `HPCL-RTI-XXXXX`
- `Filing_Date` — Date the RTI was filed
- `Department` — HPCL department receiving the RTI
- `Category` — Type of information sought
- `Applicant_Type` — Individual / Journalist / NGO / Lawyer / Business
- `State` — State from which RTI was filed
- `Mode_of_Filing` — Online / Offline / By Post
- `PIO_Assigned` — Public Information Officer handling the RTI
- `Response_Time_Days` — Days taken to respond
- `Response_Status` — On-Time / Delayed / Pending
- `Disposal_Type` — Info Provided / Partially Provided / Rejected / Transferred
- `Rejection_Reason` — RTI Act section cited if rejected
- `First_Appeal_Filed` — Yes / No
- `First_Appeal_Outcome` — Upheld / Partially Upheld / Rejected
- `Second_Appeal_CIC` — Escalated to Central Information Commission
- `Compliant_Response` — Engineered compliance flag based on the 30-day rule
- `Breach_Days` — Engineered days past the deadline
- `Financial_Year` — Engineered Indian financial year field
- `Proactive_Disclosure_Candidate` — Engineered flag for Section 4 disclosure

---

## 🧱 Project Architecture

The project is structured into four major stages:

1. **Data Generation**  
   Synthetic HPCL-style RTI data was created with realistic filing distributions and seasonality.

2. **Cleaning & EDA**  
   The dataset was cleaned, enriched with engineered features, and analyzed through 14 charts.

3. **SQL Analysis**  
   15 analytical SQL queries were used to investigate volume, compliance, appeals, geography, and COVID impact.

4. **Power BI Dashboard**  
   A 6-page executive dashboard was created with 28 DAX measures for interactive business analysis.

---

## 📊 Dashboard Structure

The dashboard is organized into **six analytical pages**, each serving a specific business requirement:

### 1️⃣ Executive Overview
**Purpose:** Provide a high-level snapshot of RTI performance.

**Key Elements:**
- KPI cards
- Yearly filing trend
- Disposal breakdown
- Overall compliance indicators

**Business Value:**  
Gives senior management a quick view of the overall RTI workload and response quality.

---

### 2️⃣ Filing Trends
**Purpose:** Analyze filing behaviour across months and years.

**Key Elements:**
- Month × Year heatmap
- Peak filing month analysis
- Digital adoption trend
- Monthly filing distribution

**Business Value:**  
Helps identify seasonal spikes so the department can plan resources in advance.

---

### 3️⃣ Department Intelligence
**Purpose:** Evaluate workload and compliance department-wise.

**Key Elements:**
- RTI volume by department
- Department compliance rate
- Geographic distribution of filers
- Department-level comparisons

**Business Value:**  
Highlights which departments receive the most RTIs and which ones struggle with deadlines.

---

### 4️⃣ Compliance & Response
**Purpose:** Measure how effectively RTIs are answered within the legal timeframe.

**Key Elements:**
- On-time vs breached responses
- Average response time by department
- Breach distribution
- Compliance trend over time

**Business Value:**  
Supports internal monitoring and helps reduce deadline breaches.

---

### 5️⃣ Appeal Analysis
**Purpose:** Study escalation patterns after initial RTI disposal.

**Key Elements:**
- RTI → First Appeal → CIC funnel
- First appeal outcome distribution
- Appeal trends by department
- Rejection and escalation behaviour

**Business Value:**  
Shows how often decisions are contested and where response quality needs improvement.

---

### 6️⃣ Insights & Recommendations
**Purpose:** Convert analytics into action.

**Key Elements:**
- Proactive disclosure opportunity
- High-impact recommendations
- Priority-based action points

**Business Value:**  
Helps the organization reduce workload, improve compliance, and strengthen transparency.

---

## 📸 Dashboard Preview

> Built in Power BI with HPCL brand colours — Navy Blue `#003087` · Gold `#F7B500`

| Page | Description |
|------|-------------|
| **P1 — Executive Overview** | KPI cards, yearly trend, disposal analysis |
| **P2 — Filing Trends** | Month-wise heatmap, peak month analysis, digital adoption |
| **P3 — Department Intelligence** | Volume, compliance, and geographic distribution |
| **P4 — Compliance & Response** | Breach analysis, response time trends, and department comparison |
| **P5 — Appeal Analysis** | Appeal funnel, first appeal outcomes, escalation patterns |
| **P6 — Insights & Recommendations** | Proactive disclosure opportunity and key recommendations |

*Dashboard mockup screenshots are available in `visuals/PBI_P*.png`*

---

## 🗃️ Project Structure

```text
hpcl-rti-analytics/
│
├── data/
│   ├── raw/
│   │   └── hpcl_rti_2014_2024.csv
│   └── processed/
│       ├── hpcl_rti_cleaned.csv
│       └── hpcl_rti.db
│
├── notebooks/
│   ├── 01_data_generation.ipynb
│   ├── 02_data_cleaning_eda.ipynb
│   └── 03_sql_analysis.ipynb
│
├── sql/
│   └── rti_analysis_queries.sql
│
├── visuals/
│   ├── 01_yearly_trend.png
│   ├── 02_monthly_heatmap.png
│   ├── 03_monthly_pattern.png
│   ├── 04_department_volume.png
│   ├── 05_department_compliance.png
│   ├── 06_compliance_trend.png
│   ├── 07_disposal_breakdown.png
│   ├── 08_rejection_reasons.png
│   ├── 09_appeal_funnel.png
│   ├── 10_digital_adoption.png
│   ├── 11_covid_impact.png
│   ├── 12_proactive_disclosure.png
│   ├── 13_pio_workload.png
│   ├── 14_state_distribution.png
│   └── PBI_P1–P6_*.png
│
├── dashboard/
│   ├── hpcl_rti_dashboard.pbix
│   ├── dax_measures.txt
│   └── powerbi_build_guide.md
│
├── scripts/
│   ├── generate_dataset.py
│   ├── 02_cleaning_preprocessing.py
│   ├── 03_sql_analysis.py
│   ├── 04_visualisations_p1.py
│   ├── 04_visualisations_p2.py
│   ├── 05_powerbi_mockups.py
│   └── generate_notebooks.py
│
├── requirements.txt
├── .gitignore
└── README.md
