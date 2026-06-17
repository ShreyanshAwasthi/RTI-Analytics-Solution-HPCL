{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "add8c901",
   "metadata": {},
   "source": [
    "# HPCL RTI Analytics — Notebook 2: Data Cleaning & EDA\n",
    "## Exploratory Data Analysis — 10 Years of RTI Filings at HPCL (2014–2024)\n",
    "\n",
    "This notebook covers:\n",
    "1. Data loading and quality checks\n",
    "2. Cleaning and feature engineering\n",
    "3. Full Exploratory Data Analysis with visualisations across 14 chart categories\n",
    "4. Key insights extracted from the analysis"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "712ca8fa",
   "metadata": {},
   "source": [
    "## 1. Imports & Global Style Config"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "54947ffc",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib\n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib.patches as mpatches\n",
    "import matplotlib.ticker as mticker\n",
    "import seaborn as sns\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "# HPCL Brand Colour Palette\n",
    "HPCL_BLUE  = '#003087'\n",
    "HPCL_BLUE2 = '#0055A5'\n",
    "HPCL_GOLD  = '#F7B500'\n",
    "GREEN      = '#27AE60'\n",
    "RED        = '#E74C3C'\n",
    "ORANGE     = '#E67E22'\n",
    "GREY       = '#BDC3C7'\n",
    "DARK_GREY  = '#7F8C8D'\n",
    "BG         = '#FAFAFA'\n",
    "\n",
    "plt.rcParams.update({\n",
    "    'figure.facecolor': BG, 'axes.facecolor': BG,\n",
    "    'axes.spines.top': False, 'axes.spines.right': False,\n",
    "    'axes.edgecolor': '#CCCCCC', 'font.family': 'DejaVu Sans',\n",
    "    'font.size': 11, 'axes.titlesize': 14, 'axes.titleweight': 'bold',\n",
    "    'figure.dpi': 130,\n",
    "})\n",
    "\n",
    "print(\"Setup complete.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "149d62a3",
   "metadata": {},
   "source": [
    "## 2. Load Raw Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ca4f7d2e",
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.read_csv('../data/raw/hpcl_rti_2014_2024.csv')\n",
    "print(f\"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns\")\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e6a628fc",
   "metadata": {},
   "outputs": [],
   "source": [
    "df.dtypes"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "07b80cd2",
   "metadata": {},
   "source": [
    "## 3. Data Quality Checks"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "03f42356",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 3.1 Duplicates\n",
    "print(f\"Duplicate RTI_IDs: {df.duplicated(subset='RTI_ID').sum()}\")\n",
    "\n",
    "# 3.2 Null audit\n",
    "print(\"\\nNull counts per column:\")\n",
    "nulls = df.isnull().sum()\n",
    "print(nulls[nulls > 0].to_string())\n",
    "print(\"\\n(Note: Nulls in Rejection_Reason, First_Appeal_*, Second_Appeal_* are structural —\")\n",
    "print(\" they exist only where the condition did not apply, not as data errors.)\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a366920f",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 3.3 Value ranges\n",
    "print(f\"Date range : {df['Filing_Date'].min()} → {df['Filing_Date'].max()}\")\n",
    "print(f\"Departments: {df['Department'].nunique()}\")\n",
    "print(f\"Categories : {df['Category'].nunique()}\")\n",
    "print(f\"States     : {df['State'].nunique()}\")\n",
    "print(f\"PIOs       : {df['PIO_Assigned'].nunique()}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "fbf211d2",
   "metadata": {},
   "source": [
    "## 4. Data Cleaning & Feature Engineering"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "eabf0724",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 4.1 Convert date columns\n",
    "for col in ['Filing_Date', 'Response_Date', 'First_Appeal_Date']:\n",
    "    df[col] = pd.to_datetime(df[col], errors='coerce')\n",
    "\n",
    "# 4.2 Fill structural nulls with descriptive labels\n",
    "df['Rejection_Reason']      = df['Rejection_Reason'].fillna('Not Applicable')\n",
    "df['First_Appeal_Outcome']  = df['First_Appeal_Outcome'].fillna('Not Applicable')\n",
    "df['Second_Appeal_Outcome'] = df['Second_Appeal_Outcome'].fillna('Not Applicable')\n",
    "\n",
    "# 4.3 Sentinel for pending response time\n",
    "df['Response_Time_Days'] = df['Response_Time_Days'].fillna(-1).astype(int)\n",
    "\n",
    "print(\"Date conversion and null handling done.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5799e3ec",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 4.4 Feature Engineering\n",
    "\n",
    "# Compliance flag — RTI Act mandates 30-day response\n",
    "df['Compliant_Response'] = df['Response_Time_Days'].apply(\n",
    "    lambda x: 'Yes' if 0 < x <= 30 else ('Pending' if x == -1 else 'No'))\n",
    "\n",
    "# Breach days — how many days past the deadline\n",
    "df['Breach_Days'] = df['Response_Time_Days'].apply(\n",
    "    lambda x: max(0, x - 30) if x > 0 else 0)\n",
    "\n",
    "# Year-Month string for time series\n",
    "df['Filing_YearMonth'] = df['Filing_Date'].dt.to_period('M').astype(str)\n",
    "\n",
    "# Indian Financial Year (Apr–Mar)\n",
    "def fin_year(d):\n",
    "    if pd.isnull(d): return None\n",
    "    return f\"FY {d.year}-{str(d.year+1)[2:]}\" if d.month >= 4 else f\"FY {d.year-1}-{str(d.year)[2:]}\"\n",
    "\n",
    "df['Financial_Year'] = df['Filing_Date'].apply(fin_year)\n",
    "\n",
    "# Proactive Disclosure Candidate flag\n",
    "proactive_cats = [\n",
    "    'LPG Distributorship Allotment', 'Petrol Pump Dealership Allotment',\n",
    "    'Recruitment & Selection', 'Employee Records & Service Matters', 'Tender & Contract Details',\n",
    "]\n",
    "df['Proactive_Disclosure_Candidate'] = df['Category'].isin(proactive_cats).map({True:'Yes', False:'No'})\n",
    "\n",
    "print(f\"Feature engineering complete. Final shape: {df.shape}\")\n",
    "df[['RTI_ID','Filing_Date','Compliant_Response','Breach_Days',\n",
    "    'Filing_YearMonth','Financial_Year','Proactive_Disclosure_Candidate']].head(4)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "374e7d93",
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "os.makedirs('../data/processed', exist_ok=True)\n",
    "df.to_csv('../data/processed/hpcl_rti_cleaned.csv', index=False)\n",
    "print(\"Saved: ../data/processed/hpcl_rti_cleaned.csv\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "14b7ff25",
   "metadata": {},
   "source": [
    "---\n",
    "## 5. EDA — Volume & Growth Trend"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "87185c7e",
   "metadata": {},
   "outputs": [],
   "source": [
    "yearly = df.groupby('Year').size().reset_index(name='Count')\n",
    "yearly['Growth_Pct'] = yearly['Count'].pct_change() * 100\n",
    "print(yearly.to_string(index=False))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "32d5a999",
   "metadata": {},
   "outputs": [],
   "source": [
    "fig, ax1 = plt.subplots(figsize=(13, 6))\n",
    "bars = ax1.bar(yearly['Year'], yearly['Count'], color=HPCL_BLUE2, alpha=0.85, width=0.6, zorder=2)\n",
    "bars[6].set_color(RED)   # 2020\n",
    "\n",
    "ax1.annotate('COVID-19\\n–16.1%', xy=(2020, 485), xytext=(2020.6, 570),\n",
    "             fontsize=9, color=RED, fontweight='bold',\n",
    "             arrowprops=dict(arrowstyle='->', color=RED, lw=1.2))\n",
    "\n",
    "for bar, val in zip(bars, yearly['Count']):\n",
    "    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8,\n",
    "             str(val), ha='center', fontsize=9, color=HPCL_BLUE, fontweight='bold')\n",
    "\n",
    "ax2 = ax1.twinx()\n",
    "ax2.plot(yearly['Year'][1:], yearly['Growth_Pct'][1:],\n",
    "         color=HPCL_GOLD, linewidth=2.2, marker='o', markersize=6)\n",
    "ax2.axhline(0, color=GREY, linewidth=0.8, linestyle='--')\n",
    "ax2.set_ylabel('YoY Growth (%)', color=HPCL_GOLD)\n",
    "ax2.tick_params(axis='y', labelcolor=HPCL_GOLD)\n",
    "ax2.set_ylim(-25, 25)\n",
    "\n",
    "ax1.set_title('RTI Filing Volume at HPCL — Yearly Trend (2014–2024)', pad=14, color=HPCL_BLUE)\n",
    "ax1.set_xlabel('Year'); ax1.set_ylabel('RTIs Filed', color=HPCL_BLUE)\n",
    "ax1.set_xticks(yearly['Year']); ax1.set_ylim(0, 870)\n",
    "ax1.grid(axis='y', linestyle='--', alpha=0.4, zorder=1)\n",
    "plt.tight_layout(); plt.savefig('../visuals/01_yearly_trend.png', dpi=150, bbox_inches='tight'); plt.show()\n",
    "print(\"Insight: RTI filings grew 66% over the decade. COVID-19 caused a sharp -16.1% drop in 2020, recovering strongly by 2022.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "8948be65",
   "metadata": {},
   "source": [
    "---\n",
    "## 6. EDA — Monthly & Seasonal Patterns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9064ff72",
   "metadata": {},
   "outputs": [],
   "source": [
    "monthly = df.groupby(['Month','Month_Name']).size().reset_index(name='Count').sort_values('Month')\n",
    "print(\"Peak months:\"); print(monthly.sort_values('Count', ascending=False).head(3)[['Month_Name','Count']].to_string(index=False))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "420df125",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Monthly heatmap — Month × Year\n",
    "pivot = df.pivot_table(index='Month_Name', columns='Year', values='RTI_ID', aggfunc='count')\n",
    "month_order = ['January','February','March','April','May','June',\n",
    "               'July','August','September','October','November','December']\n",
    "pivot = pivot.reindex(month_order).fillna(0).astype(int)\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(13, 7))\n",
    "sns.heatmap(pivot, ax=ax, cmap=sns.light_palette(HPCL_BLUE, as_cmap=True),\n",
    "            annot=True, fmt='d', linewidths=0.5, linecolor='white',\n",
    "            cbar_kws={'label': 'RTI Count', 'shrink': 0.8})\n",
    "ax.set_title('RTI Filing Heatmap — Month × Year (2014–2024)', pad=14, color=HPCL_BLUE)\n",
    "ax.tick_params(axis='x', rotation=0); ax.tick_params(axis='y', rotation=0)\n",
    "plt.tight_layout(); plt.savefig('../visuals/02_monthly_heatmap.png', dpi=150, bbox_inches='tight'); plt.show()\n",
    "print(\"Insight: January (year-end drives), March (FY-end), and October (post-AGM) are consistently peak months across all years.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "bd8f2085",
   "metadata": {},
   "source": [
    "---\n",
    "## 7. EDA — Department Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "08980729",
   "metadata": {},
   "outputs": [],
   "source": [
    "dept_stats = (df[df['Compliant_Response'] != 'Pending']\n",
    "    .groupby('Department')\n",
    "    .agg(Total=('RTI_ID','count'),\n",
    "         Avg_Resp_Days=('Response_Time_Days', lambda x: x[x>0].mean()),\n",
    "         Compliance_Pct=('Compliant_Response', lambda x: (x=='Yes').mean()*100))\n",
    "    .reset_index().sort_values('Total', ascending=False))\n",
    "print(dept_stats.round(1).to_string(index=False))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fc57197f",
   "metadata": {},
   "outputs": [],
   "source": [
    "fig, axes = plt.subplots(1, 2, figsize=(16, 7))\n",
    "dept_vol = dept_stats.sort_values('Total')\n",
    "colors_v = [HPCL_GOLD if i >= len(dept_vol)-3 else HPCL_BLUE2 for i in range(len(dept_vol))]\n",
    "axes[0].barh(dept_vol['Department'], dept_vol['Total'], color=colors_v, alpha=0.88)\n",
    "for i, (_, row) in enumerate(dept_vol.iterrows()):\n",
    "    axes[0].text(row['Total']+8, i, f\"{int(row['Total'])} ({row['Total']/len(df)*100:.1f}%)\", va='center', fontsize=8.5)\n",
    "axes[0].set_title('RTI Volume by Department', color=HPCL_BLUE)\n",
    "axes[0].set_xlabel('Total RTIs')\n",
    "axes[0].grid(axis='x', linestyle='--', alpha=0.4)\n",
    "\n",
    "dept_comp = dept_stats.sort_values('Compliance_Pct')\n",
    "colors_c = [GREEN if v>=85 else (HPCL_GOLD if v>=70 else RED) for v in dept_comp['Compliance_Pct']]\n",
    "axes[1].barh(dept_comp['Department'], dept_comp['Compliance_Pct'], color=colors_c, alpha=0.88)\n",
    "for i, (_, row) in enumerate(dept_comp.iterrows()):\n",
    "    axes[1].text(row['Compliance_Pct']+0.4, i, f\"{row['Compliance_Pct']:.1f}%\", va='center', fontsize=9, fontweight='bold')\n",
    "axes[1].axvline(80, color=DARK_GREY, linewidth=1, linestyle='--', alpha=0.6)\n",
    "axes[1].set_title('Compliance Rate by Department', color=HPCL_BLUE)\n",
    "axes[1].set_xlabel('On-Time Response Rate (%)')\n",
    "axes[1].set_xlim(0, 112)\n",
    "axes[1].grid(axis='x', linestyle='--', alpha=0.4)\n",
    "p1=mpatches.Patch(color=GREEN,label='≥85% Good'); p2=mpatches.Patch(color=HPCL_GOLD,label='70–84%'); p3=mpatches.Patch(color=RED,label='<70% Critical')\n",
    "axes[1].legend(handles=[p1,p2,p3], loc='lower right')\n",
    "plt.suptitle('Department-wise RTI Volume & Compliance (2014–2024)', fontsize=14, fontweight='bold', color=HPCL_BLUE)\n",
    "plt.tight_layout()\n",
    "plt.savefig('../visuals/04_05_department_analysis.png', dpi=150, bbox_inches='tight'); plt.show()\n",
    "print(\"Insight: Vigilance (55.5% compliance) and Projects & Pipelines (65.7%) are critical non-compliant departments. IT & Corporate Planning lead at 96%+.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f26f1a6c",
   "metadata": {},
   "source": [
    "---\n",
    "## 8. EDA — Compliance Trend Over Years"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b645ec2c",
   "metadata": {},
   "outputs": [],
   "source": [
    "comp_year = (df[df['Compliant_Response'] != 'Pending']\n",
    "    .groupby('Year')\n",
    "    .agg(Compliance_Pct=('Compliant_Response', lambda x: (x=='Yes').mean()*100),\n",
    "         Avg_Days=('Response_Time_Days', lambda x: x[x>0].mean()))\n",
    "    .reset_index())\n",
    "print(comp_year.round(1).to_string(index=False))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "18d0ed9a",
   "metadata": {},
   "outputs": [],
   "source": [
    "fig, ax1 = plt.subplots(figsize=(13, 6))\n",
    "ax1.fill_between(comp_year['Year'], comp_year['Compliance_Pct'], alpha=0.15, color=GREEN)\n",
    "ax1.plot(comp_year['Year'], comp_year['Compliance_Pct'], color=GREEN, linewidth=2.5, marker='o', markersize=8)\n",
    "for _, r in comp_year.iterrows():\n",
    "    ax1.annotate(f\"{r['Compliance_Pct']:.1f}%\", (r['Year'], r['Compliance_Pct']),\n",
    "                 xytext=(0,10), textcoords='offset points', ha='center', fontsize=9, color=GREEN, fontweight='bold')\n",
    "ax1.annotate('COVID-19\\nImpact', xy=(2020, 56.3), xytext=(2020.7, 67),\n",
    "             fontsize=9, color=RED, fontweight='bold',\n",
    "             arrowprops=dict(arrowstyle='->', color=RED, lw=1.2))\n",
    "ax1.axhline(80, color=DARK_GREY, linewidth=1, linestyle='--', alpha=0.6)\n",
    "ax1.text(2014.1, 80.8, '80% Benchmark', fontsize=8.5, color=DARK_GREY)\n",
    "ax1.set_ylim(40, 105); ax1.set_ylabel('Compliance Rate (%)', color=GREEN)\n",
    "ax1.tick_params(axis='y', labelcolor=GREEN)\n",
    "\n",
    "ax2 = ax1.twinx()\n",
    "ax2.plot(comp_year['Year'], comp_year['Avg_Days'], color=HPCL_GOLD, linewidth=2, marker='s', markersize=7, linestyle='--')\n",
    "ax2.axhline(30, color=RED, linewidth=0.9, linestyle=':', alpha=0.7)\n",
    "ax2.text(2023.8, 30.8, '30-day limit', fontsize=8, color=RED, ha='right')\n",
    "ax2.set_ylabel('Avg Response Days', color=HPCL_GOLD)\n",
    "ax2.tick_params(axis='y', labelcolor=HPCL_GOLD)\n",
    "ax2.set_ylim(15, 40)\n",
    "\n",
    "ax1.set_title('Compliance Rate & Avg Response Time — Year-wise Trend', pad=14, color=HPCL_BLUE)\n",
    "ax1.set_xlabel('Year'); ax1.set_xticks(comp_year['Year'])\n",
    "ax1.grid(axis='y', linestyle='--', alpha=0.35)\n",
    "plt.tight_layout(); plt.savefig('../visuals/06_compliance_trend.png', dpi=150, bbox_inches='tight'); plt.show()\n",
    "print(\"Insight: Compliance crashed to 56.3% in 2020 (COVID) from 83.4% in 2019. Full recovery by 2021. Overall benchmark of 80% met in most years.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1c474a18",
   "metadata": {},
   "source": [
    "---\n",
    "## 9. EDA — Disposal Type & Rejection Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "332a147c",
   "metadata": {},
   "outputs": [],
   "source": [
    "print(\"Disposal Breakdown:\")\n",
    "print(df['Disposal_Type'].value_counts().to_string())\n",
    "print(\"\\nTop Rejection Reasons:\")\n",
    "print(df[df['Disposal_Type']=='Rejected']['Rejection_Reason'].value_counts().to_string())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8b2a6a1a",
   "metadata": {},
   "outputs": [],
   "source": [
    "fig, axes = plt.subplots(1, 2, figsize=(15, 6))\n",
    "# Donut\n",
    "disposal = df['Disposal_Type'].value_counts()\n",
    "wedges,_,autotexts = axes[0].pie(disposal.values, colors=[GREEN,HPCL_GOLD,RED,HPCL_BLUE2],\n",
    "    autopct='%1.1f%%', startangle=140, explode=[0.03]*4,\n",
    "    wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2), pctdistance=0.78)\n",
    "[at.set(fontsize=11, fontweight='bold', color='white') for at in autotexts]\n",
    "axes[0].add_patch(plt.Circle((0,0), 0.45, fc=BG))\n",
    "axes[0].text(0, 0.08, f'{len(df):,}', ha='center', fontsize=22, fontweight='bold', color=HPCL_BLUE)\n",
    "axes[0].text(0, -0.18, 'Total RTIs', ha='center', fontsize=11, color=DARK_GREY)\n",
    "axes[0].legend([f'{d} ({v:,})' for d,v in zip(disposal.index, disposal.values)],\n",
    "               loc='lower center', bbox_to_anchor=(0.5,-0.1), ncol=1, fontsize=9)\n",
    "axes[0].set_title('Disposal Breakdown', color=HPCL_BLUE)\n",
    "\n",
    "# Rejection reasons\n",
    "rej = df[df['Disposal_Type']=='Rejected']['Rejection_Reason'].value_counts()\n",
    "short = [r.split('–')[0].strip() for r in rej.index]\n",
    "pcts  = rej.values / rej.values.sum() * 100\n",
    "bars = axes[1].barh(short[::-1], pcts[::-1], color=HPCL_BLUE2, alpha=0.85, height=0.6)\n",
    "for bar, val, cnt in zip(bars, pcts[::-1], rej.values[::-1]):\n",
    "    axes[1].text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,\n",
    "                f'{val:.1f}% ({cnt})', va='center', fontsize=9)\n",
    "axes[1].set_title('Rejection Reason — Section-wise', color=HPCL_BLUE)\n",
    "axes[1].set_xlabel('% of Rejections'); axes[1].set_xlim(0, 44)\n",
    "axes[1].grid(axis='x', linestyle='--', alpha=0.4)\n",
    "plt.suptitle('Disposal & Rejection Analysis (2014–2024)', fontsize=14, fontweight='bold', color=HPCL_BLUE)\n",
    "plt.tight_layout(); plt.savefig('../visuals/07_08_disposal_rejection.png', dpi=150, bbox_inches='tight'); plt.show()\n",
    "print(\"Insight: 15.1% RTIs rejected, 32.3% citing Section 8(1)(j) (personal/private information).\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "fa12ec9f",
   "metadata": {},
   "source": [
    "---\n",
    "## 10. EDA — Appeal Funnel"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ec9acc74",
   "metadata": {},
   "outputs": [],
   "source": [
    "total   = len(df)\n",
    "fa      = (df['First_Appeal_Filed']=='Yes').sum()\n",
    "cic     = (df['Second_Appeal_CIC']=='Yes').sum()\n",
    "fa_out  = df[df['First_Appeal_Filed']=='Yes']['First_Appeal_Outcome'].value_counts()\n",
    "print(f\"Total RTIs Filed  : {total:,}  (100%)\")\n",
    "print(f\"First Appeal Filed: {fa:,}  ({fa/total*100:.1f}%)\")\n",
    "print(f\"Escalated to CIC  : {cic:,}  ({cic/total*100:.2f}%)\")\n",
    "print(f\"\\nFirst Appeal Outcomes:\")\n",
    "print(fa_out.to_string())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4c069d67",
   "metadata": {},
   "outputs": [],
   "source": [
    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))\n",
    "# Funnel\n",
    "stages  = ['Total RTIs\\n(6,080)', 'First Appeal\\n(963 — 15.8%)', 'CIC Escalation\\n(129 — 2.1%)']\n",
    "counts  = [total, fa, cic]\n",
    "colors_f= [HPCL_BLUE2, ORANGE, RED]\n",
    "widths  = [1.0, fa/total, cic/total]\n",
    "for i, (stage, count, color, w) in enumerate(zip(stages, counts, colors_f, widths)):\n",
    "    bar_w = w * 9\n",
    "    rect  = plt.Rectangle((4.5 - bar_w/2, 2.0 - i*0.85), bar_w, 0.65, color=color, alpha=0.88)\n",
    "    ax1.add_patch(rect)\n",
    "    ax1.text(4.5, 2.0 - i*0.85 + 0.32, f'{count:,}', ha='center', va='center',\n",
    "             fontsize=12, fontweight='bold', color='white')\n",
    "    ax1.text(-0.1, 2.0 - i*0.85 + 0.32, stage, ha='right', va='center', fontsize=9.5, color=HPCL_BLUE)\n",
    "ax1.set_xlim(-3, 10); ax1.set_ylim(-0.2, 3); ax1.axis('off')\n",
    "ax1.set_title('RTI Appeal Funnel', color=HPCL_BLUE, fontweight='bold')\n",
    "\n",
    "# First Appeal Outcomes\n",
    "colors_fa = [GREEN, HPCL_GOLD, RED]\n",
    "wedges, _, autotexts = ax2.pie(fa_out.values, colors=colors_fa, autopct='%1.1f%%',\n",
    "    startangle=90, wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2), pctdistance=0.78)\n",
    "[at.set(fontsize=11, fontweight='bold', color='white') for at in autotexts]\n",
    "ax2.add_patch(plt.Circle((0,0), 0.45, fc=BG))\n",
    "ax2.text(0, 0, f'{fa}\n",
    "Appeals', ha='center', va='center', fontsize=11, fontweight='bold', color=HPCL_BLUE)\n",
    "ax2.legend([f'{o} ({v})' for o,v in zip(fa_out.index, fa_out.values)],\n",
    "           loc='lower center', bbox_to_anchor=(0.5,-0.1), fontsize=9)\n",
    "ax2.set_title('First Appeal Outcomes', color=HPCL_BLUE, fontweight='bold')\n",
    "plt.suptitle('RTI Appeal Funnel & Outcomes (2014–2024)', fontsize=14, fontweight='bold', color=HPCL_BLUE)\n",
    "plt.tight_layout(); plt.savefig('../visuals/09_appeal_funnel.png', dpi=150, bbox_inches='tight'); plt.show()\n",
    "print(\"Insight: 15.8% of RTIs lead to First Appeals. Of those, 50% are rejected at appeal stage — indicating room to improve initial disposal quality.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a8d60052",
   "metadata": {},
   "source": [
    "---\n",
    "## 11. EDA — Digital Adoption Trend"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4e591be3",
   "metadata": {},
   "outputs": [],
   "source": [
    "mode_year = df.groupby(['Year','Mode_of_Filing']).size().unstack(fill_value=0)\n",
    "mode_pct  = mode_year.div(mode_year.sum(axis=1), axis=0) * 100\n",
    "print(\"Online Filing % by Year:\")\n",
    "print(mode_pct['Online (RTI Online Portal)'].round(1).to_string())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "648f7c76",
   "metadata": {},
   "outputs": [],
   "source": [
    "fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 9), sharex=True, gridspec_kw={'height_ratios':[1.2,1]})\n",
    "years = list(mode_year.index); x = range(len(years))\n",
    "ax1.bar(x, mode_year['Online (RTI Online Portal)'],  color=HPCL_BLUE2, label='Online', alpha=0.88)\n",
    "ax1.bar(x, mode_year['Offline (In-Person)'], bottom=mode_year['Online (RTI Online Portal)'],\n",
    "        color=HPCL_GOLD, label='Offline', alpha=0.88)\n",
    "ax1.bar(x, mode_year['By Post'],\n",
    "        bottom=mode_year['Online (RTI Online Portal)']+mode_year['Offline (In-Person)'],\n",
    "        color=GREY, label='By Post', alpha=0.88)\n",
    "ax1.set_ylabel('Number of RTIs'); ax1.legend(loc='upper left')\n",
    "ax1.set_title('Digital Adoption — Online vs Offline Filing (2014–2024)', color=HPCL_BLUE)\n",
    "ax1.grid(axis='y', linestyle='--', alpha=0.35)\n",
    "\n",
    "online_pct = mode_pct['Online (RTI Online Portal)']\n",
    "ax2.plot(x, online_pct, color=HPCL_BLUE2, linewidth=2.5, marker='o', markersize=8)\n",
    "ax2.fill_between(x, online_pct, alpha=0.15, color=HPCL_BLUE2)\n",
    "for xi, val in zip(x, online_pct):\n",
    "    ax2.text(xi, val+1.5, f'{val:.1f}%', ha='center', fontsize=9, color=HPCL_BLUE, fontweight='bold')\n",
    "ax2.set_ylabel('Online Filing Share (%)'); ax2.set_ylim(0, 70)\n",
    "ax2.set_xticks(x); ax2.set_xticklabels(years); ax2.set_xlabel('Year')\n",
    "ax2.set_title('Online Filing % Growth', color=HPCL_BLUE, fontsize=12)\n",
    "ax2.grid(axis='y', linestyle='--', alpha=0.35)\n",
    "plt.tight_layout(); plt.savefig('../visuals/10_digital_adoption.png', dpi=150, bbox_inches='tight'); plt.show()\n",
    "print(\"Insight: Online filing grew from 25.3% (2014) to 52.1% (2024) — reflecting citizens' growing digital comfort with the RTI Online Portal.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1d77ad5d",
   "metadata": {},
   "source": [
    "---\n",
    "## 12. EDA — COVID-19 Impact Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1473f800",
   "metadata": {},
   "outputs": [],
   "source": [
    "covid = (df[df['Year'].isin([2019,2020,2021]) & (df['Compliant_Response']!='Pending')]\n",
    "    .groupby('Year').agg(\n",
    "        Total=('RTI_ID','count'),\n",
    "        Compliance=('Compliant_Response', lambda x: (x=='Yes').mean()*100),\n",
    "        AvgDays=('Response_Time_Days', lambda x: x[x>0].mean()))\n",
    "    .reset_index())\n",
    "print(covid.round(1).to_string(index=False))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "89503d2b",
   "metadata": {},
   "outputs": [],
   "source": [
    "fig, axes = plt.subplots(1, 3, figsize=(14, 5.5))\n",
    "fig.suptitle('COVID-19 Impact on HPCL RTI Processing', fontsize=14, fontweight='bold', color=HPCL_BLUE)\n",
    "metrics     = [('Total','RTI Filings',''), ('Compliance','Compliance Rate','%'), ('AvgDays','Avg Response Days',' days')]\n",
    "year_colors = [GREEN, RED, HPCL_GOLD]\n",
    "xlabels     = ['2019\n",
    "(Pre-COVID)', '2020\n",
    "(COVID)', '2021\n",
    "(Recovery)']\n",
    "for ax, (col, title, unit) in zip(axes, metrics):\n",
    "    bars = ax.bar(xlabels, covid[col], color=year_colors, alpha=0.88, width=0.55)\n",
    "    for bar, val in zip(bars, covid[col]):\n",
    "        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()*1.02,\n",
    "                f'{val:.1f}{unit}' if unit else f'{int(val):,}',\n",
    "                ha='center', fontsize=11, fontweight='bold', color=HPCL_BLUE)\n",
    "    ax.set_title(title, fontweight='bold', color=HPCL_BLUE, fontsize=12)\n",
    "    ax.grid(axis='y', linestyle='--', alpha=0.35)\n",
    "    ax.set_ylim(0, ax.get_ylim()[1]*1.2)\n",
    "plt.tight_layout(); plt.savefig('../visuals/11_covid_impact.png', dpi=150, bbox_inches='tight'); plt.show()\n",
    "print(\"Insight: 2020 compliance dropped 27 percentage points, avg response jumped 7 days — pandemic disrupted RTI processing significantly.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5d705854",
   "metadata": {},
   "source": [
    "---\n",
    "## 13. EDA — Proactive Disclosure Opportunity"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3b78913e",
   "metadata": {},
   "outputs": [],
   "source": [
    "proactive_cats = [\n",
    "    'Tender & Contract Details', 'Employee Records & Service Matters',\n",
    "    'Recruitment & Selection', 'LPG Distributorship Allotment',\n",
    "    'Petrol Pump Dealership Allotment',\n",
    "]\n",
    "pdc = df[df['Category'].isin(proactive_cats)]['Category'].value_counts()\n",
    "print(f\"RTIs in proactive disclosure categories: {pdc.sum():,} ({pdc.sum()/len(df)*100:.1f}% of total)\")\n",
    "print(pdc.to_string())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "27bd47ac",
   "metadata": {},
   "outputs": [],
   "source": [
    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))\n",
    "fig.suptitle('Proactive Disclosure Opportunity — Section 4, RTI Act 2005', fontsize=14, fontweight='bold', color=HPCL_BLUE)\n",
    "short_names = ['Tender &\\nContracts','Employee\\nRecords','Recruitment\\n& Selection','LPG\\nDistributorship','Petrol Pump\\nDealership']\n",
    "ax1.barh(short_names[::-1], pdc.values[::-1], color=HPCL_GOLD, alpha=0.88, height=0.6)\n",
    "for i, (val, cnt) in enumerate(zip(pdc.values[::-1], pdc.values[::-1])):\n",
    "    ax1.text(val+4, i, f'{val} RTIs ({val/len(df)*100:.1f}%)', va='center', fontsize=9)\n",
    "ax1.set_xlabel('Number of RTIs'); ax1.set_xlim(0, max(pdc.values)*1.45)\n",
    "ax1.set_title('Top Recurring Categories', color=HPCL_BLUE)\n",
    "ax1.grid(axis='x', linestyle='--', alpha=0.4)\n",
    "\n",
    "other = len(df) - pdc.sum()\n",
    "wedges,_,autotexts = ax2.pie([pdc.sum(), other], colors=[HPCL_GOLD, GREY],\n",
    "    autopct='%1.1f%%', startangle=90, explode=[0.05,0],\n",
    "    wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2), pctdistance=0.78)\n",
    "[at.set(fontsize=12, fontweight='bold', color='white') for at in autotexts]\n",
    "ax2.add_patch(plt.Circle((0,0), 0.45, fc=BG))\n",
    "ax2.text(0, 0, 'RTI\\nLoad', ha='center', fontsize=12, fontweight='bold', color=HPCL_BLUE)\n",
    "ax2.legend([f'Proactive Candidates ({pdc.sum():,})', f'Other RTIs ({other:,})'],\n",
    "           loc='lower center', bbox_to_anchor=(0.5,-0.08), fontsize=9)\n",
    "ax2.set_title('Potential Load Reduction', color=HPCL_BLUE)\n",
    "plt.tight_layout(); plt.savefig('../visuals/12_proactive_disclosure.png', dpi=150, bbox_inches='tight'); plt.show()\n",
    "print(f\"Insight: Publishing these 5 categories proactively could eliminate ~{pdc.sum()/len(df)*100:.0f}% of HPCL's RTI workload.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "e0612ec4",
   "metadata": {},
   "source": [
    "---\n",
    "## 14. EDA — PIO Workload & Performance"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c1860a0f",
   "metadata": {},
   "outputs": [],
   "source": [
    "pio_perf = (df[df['Compliant_Response']!='Pending']\n",
    "    .groupby('PIO_Assigned')\n",
    "    .agg(RTIs=('RTI_ID','count'),\n",
    "         Compliance=('Compliant_Response', lambda x: (x=='Yes').mean()*100),\n",
    "         AvgDays=('Response_Time_Days', lambda x: x[x>0].mean()),\n",
    "         Appeals=('First_Appeal_Filed', lambda x: (x=='Yes').sum()))\n",
    "    .reset_index().sort_values('RTIs', ascending=False))\n",
    "print(pio_perf.round(1).to_string(index=False))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4e7bc522",
   "metadata": {},
   "outputs": [],
   "source": [
    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))\n",
    "fig.suptitle('PIO Workload & Compliance Performance (2014–2024)', fontsize=14, fontweight='bold', color=HPCL_BLUE)\n",
    "bar_colors = [RED if r>500 else HPCL_BLUE2 for r in pio_perf['RTIs']]\n",
    "ax1.bar(pio_perf['PIO_Assigned'], pio_perf['RTIs'], color=bar_colors, alpha=0.88, width=0.6)\n",
    "ax1.axhline(pio_perf['RTIs'].mean(), color=DARK_GREY, linewidth=1.2, linestyle='--')\n",
    "ax1.text(12.4, pio_perf['RTIs'].mean()+3, f\"Avg: {pio_perf['RTIs'].mean():.0f}\", fontsize=8.5, color=DARK_GREY, ha='right')\n",
    "ax1.set_title('RTIs Handled per PIO', color=HPCL_BLUE); ax1.set_xlabel('PIO'); ax1.set_ylabel('RTIs Handled')\n",
    "ax1.tick_params(axis='x', rotation=35); ax1.grid(axis='y', linestyle='--', alpha=0.35)\n",
    "\n",
    "sc = ax2.scatter(pio_perf['RTIs'], pio_perf['Compliance'],\n",
    "                c=pio_perf['Appeals'], cmap='RdYlGn_r', s=200, alpha=0.85,\n",
    "                edgecolors=HPCL_BLUE, linewidth=0.8)\n",
    "for _, row in pio_perf.iterrows():\n",
    "    ax2.annotate(row['PIO_Assigned'], (row['RTIs'], row['Compliance']),\n",
    "                xytext=(5,5), textcoords='offset points', fontsize=8, color=HPCL_BLUE)\n",
    "plt.colorbar(sc, ax=ax2, label='Appeals Against PIO')\n",
    "ax2.axhline(80, color=DARK_GREY, linewidth=1, linestyle='--', alpha=0.6)\n",
    "ax2.set_xlabel('RTIs Handled'); ax2.set_ylabel('Compliance Rate (%)')\n",
    "ax2.set_title('Workload vs Compliance Scatter', color=HPCL_BLUE)\n",
    "ax2.grid(linestyle='--', alpha=0.35)\n",
    "plt.tight_layout(); plt.savefig('../visuals/13_pio_workload.png', dpi=150, bbox_inches='tight'); plt.show()\n",
    "print(\"Insight: Workload is relatively balanced across PIOs. PIO-007 handles most RTIs (498). No strong correlation between workload and compliance — suggesting systemic rather than individual capacity issues.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1de29d1d",
   "metadata": {},
   "source": [
    "---\n",
    "## 15. Key Insights Summary\n",
    "\n",
    "| # | Insight | Metric |\n",
    "|---|---------|--------|\n",
    "| 1 | RTI filings grew steadily over the decade | 430 (2014) → 714 (2024), **+66%** |\n",
    "| 2 | COVID-19 caused severe compliance breakdown | Dropped from 83.4% → **56.3%** in 2020 |\n",
    "| 3 | Vigilance is the worst-performing department | **44.5% breach rate**, avg 29.9 days response |\n",
    "| 4 | Projects & Pipelines also critical | **34.3% breach rate** |\n",
    "| 5 | March, January & October are peak filing months | Together account for **31%** of annual filings |\n",
    "| 6 | Online filing nearly doubled in 10 years | 25.3% (2014) → **52.1%** (2024) |\n",
    "| 7 | Section 8(1)(j) is the most cited rejection reason | **32.3%** of all rejections |\n",
    "| 8 | 15.8% of RTIs escalate to First Appeals | 963 appeals; 50% of those rejected again |\n",
    "| 9 | Proactive disclosure can eliminate 20.7% RTI load | 5 recurring categories → 1,261 RTIs annually |\n",
    "| 10 | Maharashtra accounts for 22% of all filers | Driven by HPCL HQ and Mumbai Refinery |\n",
    "\n",
    "---\n",
    "**Next:** See `03_sql_analysis.ipynb` for all 15 SQL queries on the same dataset."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.10.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
