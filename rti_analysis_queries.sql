-- ================================================================
-- HPCL RTI Analytics — SQL Analysis Queries
-- Database : hpcl_rti.db (SQLite)
-- Table    : rti_data
-- Period   : 2014–2024
-- ================================================================

-- ────────────────────────────────────────────────────────────────
-- Q1. YEAR-WISE RTI FILING VOLUME & GROWTH RATE
-- ────────────────────────────────────────────────────────────────
WITH yearly AS (
    SELECT
        Year,
        COUNT(*) AS Total_RTIs
    FROM rti_data
    GROUP BY Year
)
SELECT
    Year,
    Total_RTIs,
    LAG(Total_RTIs) OVER (ORDER BY Year) AS Prev_Year_RTIs,
    ROUND(
        (Total_RTIs - LAG(Total_RTIs) OVER (ORDER BY Year)) * 100.0
        / LAG(Total_RTIs) OVER (ORDER BY Year), 1
    ) AS YoY_Growth_Pct
FROM yearly
ORDER BY Year;


-- ────────────────────────────────────────────────────────────────
-- Q2. MONTHLY FILING PATTERN — PEAK MONTHS ACROSS ALL YEARS
-- ────────────────────────────────────────────────────────────────
SELECT
    Month,
    Month_Name,
    COUNT(*) AS Total_RTIs,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rti_data), 2) AS Pct_of_Total
FROM rti_data
GROUP BY Month, Month_Name
ORDER BY Month;


-- ────────────────────────────────────────────────────────────────
-- Q3. DEPARTMENT-WISE RTI VOLUME, SHARE & AVG RESPONSE TIME
-- ────────────────────────────────────────────────────────────────
SELECT
    Department,
    COUNT(*)                                                AS Total_RTIs,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rti_data), 1) AS Share_Pct,
    ROUND(AVG(CASE WHEN Response_Time_Days > 0
                   THEN Response_Time_Days END), 1)        AS Avg_Response_Days,
    SUM(CASE WHEN Compliant_Response = 'Yes' THEN 1 ELSE 0 END) AS On_Time,
    ROUND(SUM(CASE WHEN Compliant_Response = 'Yes' THEN 1.0 ELSE 0 END)
          / SUM(CASE WHEN Compliant_Response != 'Pending' THEN 1.0 ELSE 0 END) * 100, 1)
                                                            AS Compliance_Rate_Pct
FROM rti_data
GROUP BY Department
ORDER BY Total_RTIs DESC;


-- ────────────────────────────────────────────────────────────────
-- Q4. TOP RTI CATEGORIES — MOST FREQUENTLY ASKED
-- ────────────────────────────────────────────────────────────────
SELECT
    Category,
    COUNT(*)                                                AS Total_RTIs,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rti_data), 1) AS Share_Pct
FROM rti_data
GROUP BY Category
ORDER BY Total_RTIs DESC
LIMIT 15;


-- ────────────────────────────────────────────────────────────────
-- Q5. COMPLIANCE TREND — ON-TIME RESPONSE RATE BY YEAR
-- ────────────────────────────────────────────────────────────────
SELECT
    Year,
    COUNT(*)                                                AS Total_Resolved,
    SUM(CASE WHEN Compliant_Response = 'Yes' THEN 1 ELSE 0 END) AS On_Time,
    SUM(CASE WHEN Compliant_Response = 'No'  THEN 1 ELSE 0 END) AS Breached,
    ROUND(SUM(CASE WHEN Compliant_Response = 'Yes' THEN 1.0 ELSE 0 END)
          / COUNT(*) * 100, 1)                             AS Compliance_Rate_Pct,
    ROUND(AVG(CASE WHEN Response_Time_Days > 0
                   THEN Response_Time_Days END), 1)        AS Avg_Response_Days
FROM rti_data
WHERE Compliant_Response != 'Pending'
GROUP BY Year
ORDER BY Year;


-- ────────────────────────────────────────────────────────────────
-- Q6. DISPOSAL TYPE BREAKDOWN (OVERALL + BY YEAR)
-- ────────────────────────────────────────────────────────────────
-- Overall
SELECT
    Disposal_Type,
    COUNT(*)                                                AS Total,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rti_data), 1) AS Share_Pct
FROM rti_data
GROUP BY Disposal_Type
ORDER BY Total DESC;

-- Year-wise
SELECT
    Year,
    SUM(CASE WHEN Disposal_Type = 'Information Provided'               THEN 1 ELSE 0 END) AS Info_Provided,
    SUM(CASE WHEN Disposal_Type = 'Partially Provided'                 THEN 1 ELSE 0 END) AS Partial,
    SUM(CASE WHEN Disposal_Type = 'Rejected'                           THEN 1 ELSE 0 END) AS Rejected,
    SUM(CASE WHEN Disposal_Type = 'Transferred to Concerned Department' THEN 1 ELSE 0 END) AS Transferred
FROM rti_data
GROUP BY Year
ORDER BY Year;


-- ────────────────────────────────────────────────────────────────
-- Q7. REJECTION ANALYSIS — SECTION-WISE BREAKDOWN
-- ────────────────────────────────────────────────────────────────
SELECT
    Rejection_Reason,
    COUNT(*)                                                AS Rejections,
    ROUND(COUNT(*) * 100.0 /
          (SELECT COUNT(*) FROM rti_data WHERE Disposal_Type = 'Rejected'), 1) AS Pct_of_Rejections
FROM rti_data
WHERE Disposal_Type = 'Rejected'
GROUP BY Rejection_Reason
ORDER BY Rejections DESC;


-- ────────────────────────────────────────────────────────────────
-- Q8. APPEAL FUNNEL — FILING → FIRST APPEAL → CIC
-- ────────────────────────────────────────────────────────────────
SELECT
    'Total RTIs Filed'                                      AS Stage,
    COUNT(*)                                                AS Count,
    100.0                                                   AS Pct_of_Filed
FROM rti_data

UNION ALL

SELECT
    'First Appeal Filed',
    SUM(CASE WHEN First_Appeal_Filed = 'Yes' THEN 1 ELSE 0 END),
    ROUND(SUM(CASE WHEN First_Appeal_Filed = 'Yes' THEN 1.0 ELSE 0 END)
          / COUNT(*) * 100, 1)
FROM rti_data

UNION ALL

SELECT
    'Escalated to CIC (Second Appeal)',
    SUM(CASE WHEN Second_Appeal_CIC = 'Yes' THEN 1 ELSE 0 END),
    ROUND(SUM(CASE WHEN Second_Appeal_CIC = 'Yes' THEN 1.0 ELSE 0 END)
          / COUNT(*) * 100, 2)
FROM rti_data;


-- ────────────────────────────────────────────────────────────────
-- Q9. FIRST APPEAL OUTCOME ANALYSIS
-- ────────────────────────────────────────────────────────────────
SELECT
    First_Appeal_Outcome,
    COUNT(*)                                                AS Count,
    ROUND(COUNT(*) * 100.0 /
          (SELECT COUNT(*) FROM rti_data WHERE First_Appeal_Filed = 'Yes'), 1) AS Pct
FROM rti_data
WHERE First_Appeal_Filed = 'Yes'
GROUP BY First_Appeal_Outcome
ORDER BY Count DESC;


-- ────────────────────────────────────────────────────────────────
-- Q10. DEPARTMENTS WITH HIGHEST BREACH RATE (NON-COMPLIANCE)
-- ────────────────────────────────────────────────────────────────
SELECT
    Department,
    COUNT(*)                                                AS Total_RTIs,
    SUM(CASE WHEN Compliant_Response = 'No' THEN 1 ELSE 0 END) AS Breached,
    ROUND(SUM(CASE WHEN Compliant_Response = 'No' THEN 1.0 ELSE 0 END)
          / SUM(CASE WHEN Compliant_Response != 'Pending' THEN 1.0 ELSE 0 END) * 100, 1)
                                                            AS Breach_Rate_Pct,
    ROUND(AVG(CASE WHEN Breach_Days > 0 THEN Breach_Days END), 1)
                                                            AS Avg_Breach_Days
FROM rti_data
GROUP BY Department
ORDER BY Breach_Rate_Pct DESC;


-- ────────────────────────────────────────────────────────────────
-- Q11. PIO WORKLOAD ANALYSIS
-- ────────────────────────────────────────────────────────────────
SELECT
    PIO_Assigned,
    COUNT(*)                                                AS RTIs_Handled,
    ROUND(AVG(CASE WHEN Response_Time_Days > 0
                   THEN Response_Time_Days END), 1)        AS Avg_Response_Days,
    ROUND(SUM(CASE WHEN Compliant_Response = 'Yes' THEN 1.0 ELSE 0.0 END)
          / SUM(CASE WHEN Compliant_Response != 'Pending' THEN 1.0 ELSE 0.0 END) * 100, 1)
                                                            AS Compliance_Rate_Pct,
    SUM(CASE WHEN First_Appeal_Filed = 'Yes' THEN 1 ELSE 0 END) AS Appeals_Against
FROM rti_data
GROUP BY PIO_Assigned
ORDER BY RTIs_Handled DESC;


-- ────────────────────────────────────────────────────────────────
-- Q12. STATE-WISE FILING DISTRIBUTION (TOP 10)
-- ────────────────────────────────────────────────────────────────
SELECT
    State,
    COUNT(*)                                                AS Total_RTIs,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rti_data), 1) AS Share_Pct
FROM rti_data
GROUP BY State
ORDER BY Total_RTIs DESC
LIMIT 10;


-- ────────────────────────────────────────────────────────────────
-- Q13. DIGITAL ADOPTION — ONLINE vs OFFLINE TREND BY YEAR
-- ────────────────────────────────────────────────────────────────
SELECT
    Year,
    SUM(CASE WHEN Mode_of_Filing = 'Online (RTI Online Portal)' THEN 1 ELSE 0 END) AS Online,
    SUM(CASE WHEN Mode_of_Filing = 'Offline (In-Person)'        THEN 1 ELSE 0 END) AS Offline,
    SUM(CASE WHEN Mode_of_Filing = 'By Post'                    THEN 1 ELSE 0 END) AS By_Post,
    COUNT(*)                                                AS Total,
    ROUND(SUM(CASE WHEN Mode_of_Filing = 'Online (RTI Online Portal)'
                   THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1)  AS Online_Pct
FROM rti_data
GROUP BY Year
ORDER BY Year;


-- ────────────────────────────────────────────────────────────────
-- Q14. COVID IMPACT — COMPARE 2019 vs 2020
-- ────────────────────────────────────────────────────────────────
SELECT
    Year,
    COUNT(*)                                                AS Total_RTIs,
    ROUND(AVG(CASE WHEN Response_Time_Days > 0
                   THEN Response_Time_Days END), 1)        AS Avg_Response_Days,
    ROUND(SUM(CASE WHEN Compliant_Response = 'Yes' THEN 1.0 ELSE 0 END)
          / SUM(CASE WHEN Compliant_Response != 'Pending' THEN 1.0 ELSE 0 END) * 100, 1)
                                                            AS Compliance_Rate_Pct,
    SUM(CASE WHEN First_Appeal_Filed = 'Yes' THEN 1 ELSE 0 END) AS First_Appeals
FROM rti_data
WHERE Year IN (2019, 2020, 2021)
GROUP BY Year;


-- ────────────────────────────────────────────────────────────────
-- Q15. PROACTIVE DISCLOSURE CANDIDATES
--      Categories to proactively publish under Section 4 RTI Act
-- ────────────────────────────────────────────────────────────────
SELECT
    Category,
    COUNT(*)                                                AS Total_RTIs,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rti_data), 1) AS Load_Pct,
    ROUND(SUM(CASE WHEN Compliant_Response = 'Yes' THEN 1.0 ELSE 0 END)
          / SUM(CASE WHEN Compliant_Response != 'Pending' THEN 1.0 ELSE 0 END) * 100, 1)
                                                            AS Compliance_Pct,
    SUM(CASE WHEN First_Appeal_Filed = 'Yes' THEN 1 ELSE 0 END) AS Appeals_Generated
FROM rti_data
WHERE Proactive_Disclosure_Candidate = 'Yes'
GROUP BY Category
ORDER BY Total_RTIs DESC;
