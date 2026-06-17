{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "d73f34cc",
   "metadata": {},
   "source": [
    "# HPCL RTI Analytics — Notebook 3: SQL Analysis\n",
    "## 15 Analytical Queries on HPCL RTI Data (2014–2024)\n",
    "\n",
    "This notebook loads the cleaned dataset into an **SQLite** database and runs 15\n",
    "structured queries covering every dimension of the RTI analysis.\n",
    "SQLite is used for portability — the same queries run unchanged on PostgreSQL/MySQL."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "43bf16b2",
   "metadata": {},
   "source": [
    "## Setup — Load into SQLite"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ef0a919d",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import sqlite3\n",
    "\n",
    "df = pd.read_csv('../data/processed/hpcl_rti_cleaned.csv')\n",
    "conn = sqlite3.connect('../data/hpcl_rti.db')\n",
    "df.to_sql('rti_data', conn, if_exists='replace', index=False)\n",
    "print(f\"Loaded {len(df):,} records into SQLite table [rti_data]\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "2651bcb6",
   "metadata": {},
   "outputs": [],
   "source": [
    "def q(title, sql):\n",
    "    print(f\"{'─'*60}\\n{title}\\n{'─'*60}\")\n",
    "    result = pd.read_sql_query(sql, conn)\n",
    "    print(result.to_string(index=False))\n",
    "    print()\n",
    "    return result"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "05a59f71",
   "metadata": {},
   "source": [
    "## Q1 — Year-wise RTI Volume & Growth Rate"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "638fb152",
   "metadata": {},
   "outputs": [],
   "source": [
    "q(\"Q1 · Year-wise Volume & YoY Growth Rate\", \"\"\"\n",
    "WITH yearly AS (SELECT Year, COUNT(*) AS Total_RTIs FROM rti_data GROUP BY Year)\n",
    "SELECT Year, Total_RTIs,\n",
    "    LAG(Total_RTIs) OVER (ORDER BY Year) AS Prev_Year,\n",
    "    ROUND((Total_RTIs - LAG(Total_RTIs) OVER (ORDER BY Year))*100.0\n",
    "          / LAG(Total_RTIs) OVER (ORDER BY Year), 1) AS YoY_Growth_Pct\n",
    "FROM yearly ORDER BY Year;\n",
    "\"\"\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d8ecf32f",
   "metadata": {},
   "source": [
    "## Q2 — Peak Month Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5b82bb09",
   "metadata": {},
   "outputs": [],
   "source": [
    "q(\"Q2 · Monthly Filing Pattern\", \"\"\"\n",
    "SELECT Month, Month_Name, COUNT(*) AS Total_RTIs,\n",
    "    ROUND(COUNT()*100.0/(SELECT COUNT(*) FROM rti_data),2) AS Pct_of_Total\n",
    "FROM rti_data GROUP BY Month, Month_Name ORDER BY Month;\n",
    "\"\"\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a83d42fe",
   "metadata": {},
   "source": [
    "## Q3 — Department Overview"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "24d31346",
   "metadata": {},
   "outputs": [],
   "source": [
    "q(\"Q3 · Department-wise Volume, Share & Compliance\", \"\"\"\n",
    "SELECT Department, COUNT(*) AS Total_RTIs,\n",
    "    ROUND(COUNT()*100.0/(SELECT COUNT(*) FROM rti_data),1) AS Share_Pct,\n",
    "    ROUND(AVG(CASE WHEN Response_Time_Days>0 THEN Response_Time_Days END),1) AS Avg_Resp_Days,\n",
    "    ROUND(SUM(CASE WHEN Compliant_Response='Yes' THEN 1.0 ELSE 0 END)\n",
    "         /SUM(CASE WHEN Compliant_Response!='Pending' THEN 1.0 ELSE 0 END)*100,1) AS Compliance_Pct\n",
    "FROM rti_data GROUP BY Department ORDER BY Total_RTIs DESC;\n",
    "\"\"\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "45fc245d",
   "metadata": {},
   "source": [
    "## Q4 — Top RTI Categories"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c00db313",
   "metadata": {},
   "outputs": [],
   "source": [
    "q(\"Q4 · Most Frequently Filed RTI Categories\", \"\"\"\n",
    "SELECT Category, COUNT(*) AS Total_RTIs,\n",
    "    ROUND(COUNT()*100.0/(SELECT COUNT(*) FROM rti_data),1) AS Share_Pct\n",
    "FROM rti_data GROUP BY Category ORDER BY Total_RTIs DESC LIMIT 15;\n",
    "\"\"\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c360cc88",
   "metadata": {},
   "source": [
    "## Q5 — Year-wise Compliance Trend"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f48788f5",
   "metadata": {},
   "outputs": [],
   "source": [
    "q(\"Q5 · Compliance Rate by Year (30-day Deadline)\", \"\"\"\n",
    "SELECT Year,\n",
    "    SUM(CASE WHEN Compliant_Response='Yes' THEN 1 ELSE 0 END) AS On_Time,\n",
    "    SUM(CASE WHEN Compliant_Response='No'  THEN 1 ELSE 0 END) AS Breached,\n",
    "    ROUND(SUM(CASE WHEN Compliant_Response='Yes' THEN 1.0 ELSE 0 END)\n",
    "         /SUM(CASE WHEN Compliant_Response!='Pending' THEN 1.0 ELSE 0 END)*100,1) AS Compliance_Pct,\n",
    "    ROUND(AVG(CASE WHEN Response_Time_Days>0 THEN Response_Time_Days END),1) AS Avg_Resp_Days\n",
    "FROM rti_data WHERE Compliant_Response!='Pending' GROUP BY Year ORDER BY Year;\n",
    "\"\"\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d6a1b461",
   "metadata": {},
   "source": [
    "## Q6 — Disposal Breakdown"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b99cd949",
   "metadata": {},
   "outputs": [],
   "source": [
    "q(\"Q6 · Disposal Type Breakdown (Overall)\", \"\"\"\n",
    "SELECT Disposal_Type, COUNT(*) AS Total,\n",
    "    ROUND(COUNT()*100.0/(SELECT COUNT(*) FROM rti_data),1) AS Share_Pct\n",
    "FROM rti_data GROUP BY Disposal_Type ORDER BY Total DESC;\n",
    "\"\"\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f8c69e32",
   "metadata": {},
   "source": [
    "## Q7 — Rejection Section Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9f316c53",
   "metadata": {},
   "outputs": [],
   "source": [
    "q(\"Q7 · Section-wise Rejection Reasons\", \"\"\"\n",
    "SELECT Rejection_Reason, COUNT(*) AS Rejections,\n",
    "    ROUND(COUNT()*100.0/(SELECT COUNT(*) FROM rti_data WHERE Disposal_Type='Rejected'),1) AS Pct\n",
    "FROM rti_data WHERE Disposal_Type='Rejected'\n",
    "GROUP BY Rejection_Reason ORDER BY Rejections DESC;\n",
    "\"\"\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "56a8706c",
   "metadata": {},
   "source": [
    "## Q8 — Appeal Funnel"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b7b7b2fe",
   "metadata": {},
   "outputs": [],
   "source": [
    "q(\"Q8 · RTI Appeal Funnel\", \"\"\"\n",
    "SELECT 'Total RTIs Filed' AS Stage, COUNT(*) AS Count, 100.0 AS Pct FROM rti_data\n",
    "UNION ALL\n",
    "SELECT 'First Appeal Filed',\n",
    "    SUM(CASE WHEN First_Appeal_Filed='Yes' THEN 1 ELSE 0 END),\n",
    "    ROUND(SUM(CASE WHEN First_Appeal_Filed='Yes' THEN 1.0 ELSE 0 END)/COUNT(*)*100,1)\n",
    "FROM rti_data\n",
    "UNION ALL\n",
    "SELECT 'Escalated to CIC',\n",
    "    SUM(CASE WHEN Second_Appeal_CIC='Yes' THEN 1 ELSE 0 END),\n",
    "    ROUND(SUM(CASE WHEN Second_Appeal_CIC='Yes' THEN 1.0 ELSE 0 END)/COUNT(*)*100,2)\n",
    "FROM rti_data;\n",
    "\"\"\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "54d9339d",
   "metadata": {},
   "source": [
    "## Q9 — First Appeal Outcomes"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "20276792",
   "metadata": {},
   "outputs": [],
   "source": [
    "q(\"Q9 · First Appeal Outcome Distribution\", \"\"\"\n",
    "SELECT First_Appeal_Outcome, COUNT(*) AS Count,\n",
    "    ROUND(COUNT()*100.0/(SELECT COUNT(*) FROM rti_data WHERE First_Appeal_Filed='Yes'),1) AS Pct\n",
    "FROM rti_data WHERE First_Appeal_Filed='Yes'\n",
    "GROUP BY First_Appeal_Outcome ORDER BY Count DESC;\n",
    "\"\"\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "4e91dbd7",
   "metadata": {},
   "source": [
    "## Q10 — Highest Breach Rate Departments"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "30a00fdf",
   "metadata": {},
   "outputs": [],
   "source": [
    "q(\"Q10 · Departments with Highest Non-Compliance\", \"\"\"\n",
    "SELECT Department, COUNT(*) AS Total_RTIs,\n",
    "    SUM(CASE WHEN Compliant_Response='No' THEN 1 ELSE 0 END) AS Breached,\n",
    "    ROUND(SUM(CASE WHEN Compliant_Response='No' THEN 1.0 ELSE 0 END)\n",
    "         /SUM(CASE WHEN Compliant_Response!='Pending' THEN 1.0 ELSE 0 END)*100,1) AS Breach_Rate_Pct,\n",
    "    ROUND(AVG(CASE WHEN Breach_Days>0 THEN Breach_Days END),1) AS Avg_Breach_Days\n",
    "FROM rti_data GROUP BY Department ORDER BY Breach_Rate_Pct DESC;\n",
    "\"\"\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "84858568",
   "metadata": {},
   "source": [
    "## Q11 — PIO Performance"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8779fe10",
   "metadata": {},
   "outputs": [],
   "source": [
    "q(\"Q11 · PIO Workload & Compliance\", \"\"\"\n",
    "SELECT PIO_Assigned, COUNT(*) AS RTIs_Handled,\n",
    "    ROUND(AVG(CASE WHEN Response_Time_Days>0 THEN Response_Time_Days END),1) AS Avg_Resp_Days,\n",
    "    ROUND(SUM(CASE WHEN Compliant_Response='Yes' THEN 1.0 ELSE 0 END)\n",
    "         /SUM(CASE WHEN Compliant_Response!='Pending' THEN 1.0 ELSE 0 END)*100,1) AS Compliance_Pct,\n",
    "    SUM(CASE WHEN First_Appeal_Filed='Yes' THEN 1 ELSE 0 END) AS Appeals_Against\n",
    "FROM rti_data GROUP BY PIO_Assigned ORDER BY RTIs_Handled DESC;\n",
    "\"\"\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f12efb4d",
   "metadata": {},
   "source": [
    "## Q12 — Geographic Distribution"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0ef8c8dc",
   "metadata": {},
   "outputs": [],
   "source": [
    "q(\"Q12 · Top 10 States by Filing Volume\", \"\"\"\n",
    "SELECT State, COUNT(*) AS Total_RTIs,\n",
    "    ROUND(COUNT()*100.0/(SELECT COUNT(*) FROM rti_data),1) AS Share_Pct\n",
    "FROM rti_data GROUP BY State ORDER BY Total_RTIs DESC LIMIT 10;\n",
    "\"\"\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "50171689",
   "metadata": {},
   "source": [
    "## Q13 — Digital Adoption"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "67ba1ed6",
   "metadata": {},
   "outputs": [],
   "source": [
    "q(\"Q13 · Online vs Offline Filing Trend by Year\", \"\"\"\n",
    "SELECT Year,\n",
    "    SUM(CASE WHEN Mode_of_Filing='Online (RTI Online Portal)' THEN 1 ELSE 0 END) AS Online,\n",
    "    SUM(CASE WHEN Mode_of_Filing='Offline (In-Person)'        THEN 1 ELSE 0 END) AS Offline,\n",
    "    SUM(CASE WHEN Mode_of_Filing='By Post'                    THEN 1 ELSE 0 END) AS By_Post,\n",
    "    COUNT(*) AS Total,\n",
    "    ROUND(SUM(CASE WHEN Mode_of_Filing='Online (RTI Online Portal)' THEN 1.0 ELSE 0 END)\n",
    "         /COUNT(*)*100,1) AS Online_Pct\n",
    "FROM rti_data GROUP BY Year ORDER BY Year;\n",
    "\"\"\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f3a9fa0c",
   "metadata": {},
   "source": [
    "## Q14 — COVID Impact"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7baff949",
   "metadata": {},
   "outputs": [],
   "source": [
    "q(\"Q14 · COVID-19 Impact — 2019 vs 2020 vs 2021\", \"\"\"\n",
    "SELECT Year, COUNT(*) AS Total_RTIs,\n",
    "    ROUND(AVG(CASE WHEN Response_Time_Days>0 THEN Response_Time_Days END),1) AS Avg_Resp_Days,\n",
    "    ROUND(SUM(CASE WHEN Compliant_Response='Yes' THEN 1.0 ELSE 0 END)\n",
    "         /SUM(CASE WHEN Compliant_Response!='Pending' THEN 1.0 ELSE 0 END)*100,1) AS Compliance_Pct,\n",
    "    SUM(CASE WHEN First_Appeal_Filed='Yes' THEN 1 ELSE 0 END) AS First_Appeals\n",
    "FROM rti_data WHERE Year IN (2019,2020,2021) GROUP BY Year;\n",
    "\"\"\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c30b7a0c",
   "metadata": {},
   "source": [
    "## Q15 — Proactive Disclosure Candidates"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "19aaa6ca",
   "metadata": {},
   "outputs": [],
   "source": [
    "q(\"Q15 · Top Categories for Proactive Disclosure (Section 4, RTI Act)\", \"\"\"\n",
    "SELECT Category, COUNT(*) AS Total_RTIs,\n",
    "    ROUND(COUNT()*100.0/(SELECT COUNT(*) FROM rti_data),1) AS Load_Pct,\n",
    "    ROUND(SUM(CASE WHEN Compliant_Response='Yes' THEN 1.0 ELSE 0 END)\n",
    "         /SUM(CASE WHEN Compliant_Response!='Pending' THEN 1.0 ELSE 0 END)*100,1) AS Compliance_Pct,\n",
    "    SUM(CASE WHEN First_Appeal_Filed='Yes' THEN 1 ELSE 0 END) AS Appeals_Generated\n",
    "FROM rti_data WHERE Proactive_Disclosure_Candidate='Yes'\n",
    "GROUP BY Category ORDER BY Total_RTIs DESC;\n",
    "\"\"\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3302d0a4",
   "metadata": {},
   "outputs": [],
   "source": [
    "conn.close()\n",
    "print(\"All 15 queries executed. SQLite connection closed.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5cd270d5",
   "metadata": {},
   "source": [
    "---\n",
    "## Summary\n",
    "All 15 SQL queries cover the complete analytical scope:\n",
    "- **Volume & Growth** (Q1–Q2): Trend and seasonality\n",
    "- **Department & Category** (Q3–Q4): Where RTIs are coming from\n",
    "- **Compliance** (Q5, Q10): 30-day deadline adherence\n",
    "- **Disposal & Rejection** (Q6–Q7): Information provided vs rejected\n",
    "- **Appeals** (Q8–Q9): Escalation patterns\n",
    "- **Operations** (Q11): PIO performance and workload\n",
    "- **Context** (Q12–Q14): Geography, digital adoption, COVID impact\n",
    "- **Recommendations** (Q15): Proactive disclosure opportunities"
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
