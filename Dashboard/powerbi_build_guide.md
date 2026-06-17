# HPCL RTI Analytics — Power BI Dashboard Build Guide
## 6-Page Dashboard | Brand Colours: #003087 (Navy) · #F7B500 (Gold)

---

## STEP 0 — DATA IMPORT

1. Open **Power BI Desktop**
2. **Home → Get Data → Text/CSV**
3. Select `data/processed/hpcl_rti_cleaned.csv` → Load
4. **Home → Transform Data** (Power Query Editor)
   - Set `Filing_Date`, `Response_Date`, `First_Appeal_Date` → **Date** type
   - Set `Year`, `Month`, `Response_Time_Days`, `Breach_Days` → **Whole Number**
   - Set `Compliance Rate %` computed fields → **Decimal**
   - Close & Apply
5. Rename the table to `rti_data` (right-click in Fields pane → Rename)

---

## STEP 1 — ENTER ALL DAX MEASURES

Go to **Modeling → New Measure** and paste each measure from `dax_measures.txt`.
Create them ALL before building any visuals — visuals reference them by name.

Organise into a **Measure Table** (best practice):
- Home → Enter Data → name it `_Measures` → Load
- Drag all your measures into this table via right-click → Move to table

---

## STEP 2 — THEME & BRAND SETUP

**View → Themes → Customize current theme:**

```
Primary colour   : #003087  (HPCL Navy Blue)
Secondary colour : #F7B500  (HPCL Gold)
Background       : #FAFAFA
Text             : #1A1A2E
Card background  : #FFFFFF
Diverging - Low  : #E74C3C  (Red — breach/bad)
Diverging - High : #27AE60  (Green — compliant/good)
```

Save theme as `HPCL_Theme.json` and apply to all pages.

---

## PAGE 1 — EXECUTIVE OVERVIEW
**Purpose:** Single-glance health check. Senior management view.

### Canvas Setup
- Canvas size: 1280 × 720 px
- Background: #FAFAFA

### Visuals (left to right, top to bottom)

**[TOP BAR — Page Title]**
- Insert → Text Box
- Text: "HPCL RTI Analytics Dashboard | 2014–2024"
- Font: Segoe UI Bold, 18pt, colour #003087
- Position: Top, full width

---

**[ROW 1 — 5 KPI Cards]**

| Card # | Measure | Label | Icon |
|--------|---------|-------|------|
| 1 | Total RTIs | "Total RTIs Filed" | 📄 |
| 2 | Compliance Rate % | "Compliance Rate" | ✅ |
| 3 | Avg Response Days | "Avg Response Days" | ⏱ |
| 4 | First Appeal Rate % | "First Appeal Rate" | ⚠️ |
| 5 | Online Filing % | "Online Filings" | 💻 |

For each card:
- Visual: **Card**
- Format → Data label → Font size 28, Bold, Colour #003087
- Category label → Font 11pt, Colour #7F8C8D
- Card background: White, border radius 8px, shadow enabled

For Compliance Rate card specifically:
- Add a conditional icon: ≥85% = green, 70-84% = amber, <70% = red
- Use the `Compliance Status` measure for conditional formatting

---

**[ROW 2 — LEFT: Line Chart]**

- Visual: **Line Chart**
- X-axis: `Year`
- Y-axis: `Total RTIs` (bar), `Compliance Rate %` (line — secondary axis)
- Secondary line colour: #F7B500
- Primary bars colour: #003087
- Data labels: ON
- Title: "RTI Volume & Compliance Trend (2014–2024)"
- Annotation: Add a reference line at Year=2020, label "COVID-19"
  (Analytics pane → Constant Line → Value 2020)
- Width: 55% of canvas

---

**[ROW 2 — RIGHT: Donut Chart]**

- Visual: **Donut Chart**
- Legend: `Disposal_Type`
- Values: `Total RTIs`
- Colours:
  - Information Provided → #27AE60
  - Partially Provided   → #F7B500
  - Rejected             → #E74C3C
  - Transferred          → #0055A5
- Inner label: `Total RTIs` measure
- Title: "Disposal Breakdown"
- Width: 40% of canvas

---

**[ROW 3 — SLICER: Year]**

- Visual: **Slicer**
- Field: `Year`
- Style: Horizontal tile
- Format: Blue selected tile, white text
- Position: Bottom strip, full width

---

**[BOTTOM — 3 small KPI callouts]**

Use Text Boxes with calculated values embedded:
- "📍 Peak Month: March" (from your EDA)
- "🏭 Most Active Dept: HR & Personnel (18.8%)"
- "📈 Decade Growth: +66%"

---

## PAGE 2 — FILING TRENDS
**Purpose:** Temporal patterns — when are RTIs being filed?

### Visuals

**[TOP LEFT — Matrix Heatmap]**
- Visual: **Matrix**
- Rows: `Month_Name` (sort by `Month` field)
- Columns: `Year`
- Values: `Total RTIs`
- Conditional Formatting on Values:
  - Background colour scale: white → #003087
  - Apply to: Values
- Title: "Monthly × Yearly RTI Heatmap"
- Size: 50% width × 45% height

---

**[TOP RIGHT — Bar Chart: Monthly Pattern]**
- Visual: **Clustered Bar Chart**
- Y-axis: `Month_Name` (sorted by Month number)
- X-axis: `Total RTIs`
- Conditional formatting on bars:
  - If Month IN (1, 3, 10) → colour #F7B500 (peak months)
  - Others → #003087
- Title: "Monthly Filing Pattern — Peak Month Analysis"
- Reference line: Average line (Analytics pane)

---

**[BOTTOM LEFT — Stacked Bar: Digital Adoption]**
- Visual: **Stacked Bar Chart**
- X-axis: `Year`
- Y-axis: `Total RTIs`
- Legend: `Mode_of_Filing`
- Colours:
  - Online (RTI Online Portal) → #003087
  - Offline (In-Person)        → #F7B500
  - By Post                    → #BDC3C7
- Title: "Digital Adoption — Filing Mode Trend"

---

**[BOTTOM RIGHT — Line Chart: Online % Trend]**
- Visual: **Line Chart**
- X-axis: `Year`
- Y-axis: `Online Filing %` (DAX measure)
- Data labels: ON (show % values)
- Line colour: #003087, thick (3px)
- Shaded area: ON, alpha 15%
- Title: "Online Filing Share Growth (%)"

---

**[SLICERS]**
- Year: Horizontal tile (top right corner)
- Quarter: Dropdown

---

## PAGE 3 — DEPARTMENT INTELLIGENCE
**Purpose:** Which departments are driving RTI volume and who's compliant?

### Visuals

**[TOP — Horizontal Bar: Volume]**
- Visual: **Bar Chart (Horizontal)**
- Y-axis: `Department`
- X-axis: `Total RTIs`
- Sort: Descending by Total RTIs
- Data labels: ON — show value + %
- Colour: #0055A5 standard, #F7B500 for top 3
- Title: "RTI Volume by Department"
- Width: 48%

---

**[TOP RIGHT — Horizontal Bar: Compliance Rate]**
- Visual: **Bar Chart (Horizontal)**
- Y-axis: `Department`
- X-axis: `Compliance Rate %`
- Conditional formatting on bars:
  - ≥ 85% → #27AE60 (Green)
  - 70–84% → #F7B500 (Amber)
  - < 70% → #E74C3C (Red)
- Reference line at 80% (Analytics pane → Constant Line)
- Title: "Compliance Rate by Department"
- Data labels: ON
- Width: 48%

---

**[MIDDLE — Table with Conditional Formatting]**
- Visual: **Table**
- Columns:
  - `Department`
  - `Total RTIs` (DAX)
  - `Compliance Rate %` (DAX) — conditional formatting: Red-Amber-Green
  - `Avg Response Days` (DAX) — conditional formatting: Green-Amber-Red (inverted)
  - `Breach Rate %` (DAX) — conditional formatting: Green-Amber-Red
  - `Total First Appeals` (DAX)
- Font: Segoe UI, 10pt
- Header background: #003087, white text
- Alternate row colour: #F0F4FF
- Title: "Department Performance Summary"

---

**[BOTTOM — Map: State Distribution]**
- Visual: **Map** (or Filled Map)
- Location: `State`
- Bubble size: `Total RTIs`
- Bubble colour: #003087
- Title: "Geographic Distribution of RTI Filers"
- Note: If map is unavailable, use a horizontal bar chart (Top 10 States)

---

**[SLICER]**
- Department: Dropdown (top right)
- Year: Tile

---

## PAGE 4 — COMPLIANCE & RESPONSE ANALYSIS
**Purpose:** Deep dive into the 30-day deadline performance

### Visuals

**[TOP LEFT — Gauge: Overall Compliance]**
- Visual: **Gauge**
- Value: `Compliance Rate %`
- Min: 0, Max: 100
- Target: 80 (add a target line at 80%)
- Colour fill:
  - 0–70 → Red
  - 70–85 → Amber
  - 85–100 → Green
- Title: "Overall Compliance Rate"
- Data label: Large, bold, #003087
- Size: 25% width

---

**[TOP CENTRE — Clustered Bar: On-Time vs Breached by Year]**
- Visual: **Clustered Bar Chart**
- X-axis: `Year`
- Y-axis: `On Time RTIs` (series 1, #27AE60) and `Breached RTIs` (series 2, #E74C3C)
- Data labels: ON
- Reference line at X=2020 (COVID annotation)
- Title: "On-Time vs Breached Responses by Year"
- Width: 45%

---

**[TOP RIGHT — Line Chart: Compliance Rate Trend]**
- Visual: **Line Chart**
- X-axis: `Year`
- Y-axis: `Compliance Rate %`
- Line colour: #27AE60
- Shaded area below line: ON
- Reference line: 80% constant line, dashed
- Data labels: ON (show % for each year)
- Title: "Year-wise Compliance Rate Trend"
- Width: 25%

---

**[BOTTOM LEFT — Scatter: Dept Breach Rate vs Avg Breach Days]**
- Visual: **Scatter Chart**
- X-axis: `Breach Rate %`
- Y-axis: `Avg Breach Days`
- Details: `Department` (each dot = one dept)
- Size: `Total RTIs`
- Colour: Red gradient based on Breach Rate %
- Quadrant lines: Draw reference lines at X=25%, Y=10 days
  (Analytics pane → Constant Lines)
- Title: "Breach Rate vs Severity — Department Scatter"
- Width: 48%

---

**[BOTTOM RIGHT — Bar: Avg Response Days by Department]**
- Visual: **Clustered Bar (Horizontal)**
- Y-axis: `Department`
- X-axis: `Avg Response Days`
- Colour conditional: ≤30 → Green, ≤40 → Amber, >40 → Red
- Reference line at X=30 (legal deadline)
- Title: "Avg Response Days by Department"
- Width: 48%

---

**[SLICERS]**
- Year: Tile
- Department: Dropdown
- Compliant_Response: Toggle (Yes / No / Pending)

---

## PAGE 5 — APPEAL ANALYSIS
**Purpose:** How many RTIs are escalating and why?

### Visuals

**[TOP — 3 KPI Cards]**
- Card 1: `Total First Appeals` + `First Appeal Rate %`
- Card 2: `Total CIC Escalations` + `CIC Escalation Rate %`
- Card 3: `Rejection Rate %`

---

**[MIDDLE LEFT — Funnel Chart]**
- Visual: **Funnel**
- Category: (manual — use a custom table)

  Create a new calculated table in Power BI:
  ```
  Appeal Funnel =
  DATATABLE(
      "Stage", STRING,
      "Count", INTEGER,
      "Order", INTEGER,
      {
          {"Total RTIs Filed", 6080, 1},
          {"First Appeal Filed", 963, 2},
          {"CIC Escalation", 129, 3}
      }
  )
  ```
- Drag `Stage` to Category, `Count` to Values
- Funnel colours:
  - Stage 1 → #003087
  - Stage 2 → #E67E22
  - Stage 3 → #E74C3C
- Title: "RTI Appeal Funnel"

---

**[MIDDLE RIGHT — Donut: First Appeal Outcomes]**
- Visual: **Donut Chart**
- Filter: `First_Appeal_Filed = "Yes"`
- Legend: `First_Appeal_Outcome`
- Values: `Total RTIs`
- Colours:
  - Upheld           → #27AE60
  - Partially Upheld → #F7B500
  - Rejected         → #E74C3C
  - Not Applicable   → #BDC3C7 (exclude via filter)
- Title: "First Appeal Outcomes"

---

**[BOTTOM LEFT — Bar: Appeals by Department]**
- Visual: **Clustered Bar (Horizontal)**
- Y-axis: `Department`
- X-axis: `Total First Appeals`
- Sort: Descending
- Colour: #E67E22
- Title: "First Appeals Generated by Department"

---

**[BOTTOM RIGHT — Bar: Appeal Rate by Disposal Type]**
- Visual: **Clustered Bar**
- X-axis: `Disposal_Type`
- Y-axis: `First Appeal Rate %`
- Colour: conditional (higher = more red)
- Data labels: ON (show %)
- Title: "Appeal Rate by Disposal Outcome"
- (Expect: Rejected RTIs will show ~45% appeal rate)

---

**[SLICERS]**
- Year: Tile
- Department: Dropdown

---

## PAGE 6 — INSIGHTS & RECOMMENDATIONS
**Purpose:** The "so what" page — what HPCL should do next

### Visuals

**[TOP — Section Title Text Box]**
"Key Findings & Recommendations for HPCL RTI Department"
Font: Bold, 18pt, #003087

---

**[LEFT — Bar: Proactive Disclosure Candidates]**
- Visual: **Clustered Bar (Horizontal)**
- Filter: `Proactive_Disclosure_Candidate = "Yes"`
- Y-axis: `Category`
- X-axis: `Total RTIs`
- Colour: #F7B500
- Data labels: show count + %
- Title: "Section 4 Proactive Disclosure Candidates"
- Subtitle text box below: "Publishing these 5 categories can eliminate ~20.7% of RTI load"

---

**[RIGHT TOP — KPI Cards (3)]**
- Card 1: `Proactive Disclosure Candidates` — "RTIs Reducible via Section 4"
- Card 2: Vigilance Breach Rate (filtered) — "Vigilance Dept Breach Rate"
  Measure: `CALCULATE([Breach Rate %], rti_data[Department]="Vigilance")`
- Card 3: COVID Compliance Drop
  Measure:
  ```
  COVID Compliance Drop =
  CALCULATE([Compliance Rate %], rti_data[Year]=2019)
  - CALCULATE([Compliance Rate %], rti_data[Year]=2020)
  ```
  Label: "Compliance Drop in 2020 (COVID)"

---

**[RIGHT BOTTOM — Recommendation Table]**

Create a manual table (Enter Data):

| # | Finding | Recommendation | Priority |
|---|---------|----------------|----------|
| 1 | Vigilance dept — 44.5% breach rate | Dedicate additional PIO capacity; set internal 21-day SLA | High |
| 2 | 20.7% RTIs are repetitive | Publish 5 categories under Section 4 proactively | High |
| 3 | March & October are peak months | Pre-deploy additional staff; clear backlog before peak | Medium |
| 4 | Online adoption at 52% | Promote RTI Online Portal; target 70% by 2026 | Medium |
| 5 | 50% of First Appeals rejected again | Improve quality of first-time disposal; review rejection checklist | Medium |
| 6 | COVID exposed fragility | Build contingency RTI processing protocol for disruptions | Low |

- Visual: **Table**
- Priority conditional formatting: High → Red, Medium → Amber, Low → Green
- Header: #003087 background, white text

---

**[BOTTOM — Donut: Repeat Filer Analysis]**
- Visual: **Donut**
- Manually create table:
  - "Repeat Filer: Yes" → 18%
  - "First-time Filer" → 82%
- Or use:
  - Legend: `Is_Repeat_Filer`
  - Values: `Total RTIs`
- Title: "Repeat vs First-Time Filers"

---

## STEP 3 — PAGE NAVIGATION

Add navigation buttons so users can move between pages:

1. **View → Buttons → Navigator → Page Navigator** (Power BI auto-creates)
   - Style: Pills or Tabs
   - Place at top of every page
   - Selected colour: #003087 (blue)
   - Hover colour: #F7B500 (gold)

Page names to use:
- 🏠 Executive Overview
- 📈 Filing Trends
- 🏭 Departments
- ✅ Compliance
- ⚖️ Appeals
- 💡 Insights

---

## STEP 4 — FINAL FORMATTING CHECKLIST

Before export, verify:

- [ ] All pages have the HPCL logo (top-left corner — insert as Image)
- [ ] All chart titles are consistent font (Segoe UI Bold, 13pt, #003087)
- [ ] All axes labels are 10pt, #7F8C8D
- [ ] All cards have white background with subtle border (#E8ECF0)
- [ ] Slicers match across pages (same fields, same style)
- [ ] Year slicer default = "All" (not a specific year)
- [ ] Cross-filtering enabled — clicking any visual filters others on same page
- [ ] Mobile layout configured (View → Mobile Layout) for at least Page 1
- [ ] File saved as: `hpcl_rti_dashboard.pbix`

---

## STEP 5 — EXPORT

1. **Publish to Power BI Service** (optional — needs Power BI account)
   - Home → Publish → Select workspace

2. **Export as PDF** (for report attachment):
   - File → Export → Export to PDF
   - Select "All Pages"
   - Save as `dashboard_export.pdf`

3. **Screenshots for GitHub README**:
   - Take one screenshot per page
   - Save as `dashboard_page1.png` through `dashboard_page6.png`
   - Add to `visuals/` folder in GitHub repo

---

## QUICK REFERENCE — VISUAL TYPE MAPPING

| Analysis | Power BI Visual |
|----------|----------------|
| KPI/Single number | Card |
| Time trend | Line Chart |
| Category comparison | Clustered Bar / Horizontal Bar |
| Part-of-whole | Donut Chart |
| Month × Year pattern | Matrix (with conditional formatting) |
| Funnel/stages | Funnel Chart |
| Correlation | Scatter Chart |
| Performance vs target | Gauge |
| Geographic | Map / Filled Map |
| Detailed data | Table (with conditional formatting) |
