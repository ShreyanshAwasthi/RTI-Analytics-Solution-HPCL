# GitHub Repository Setup — Step-by-Step
# Run these commands from inside your hpcl-rti-analytics/ folder

# ─────────────────────────────────────────────
# STEP 1 — INITIALISE GIT LOCALLY
# ─────────────────────────────────────────────

git init
git add .
git commit -m "Initial commit: HPCL RTI Analytics — full project"


# ─────────────────────────────────────────────
# STEP 2 — CREATE REPO ON GITHUB
# ─────────────────────────────────────────────

# Go to https://github.com/new
# Repository name  : hpcl-rti-analytics
# Description      : End-to-end RTI filing pattern analysis at HPCL (2014–2024)
#                    using Python, SQL & Power BI | Internship Project
# Visibility       : Public  ← important for portfolio visibility
# README           : DO NOT tick "Add README" (we already have one)
# Click: Create repository


# ─────────────────────────────────────────────
# STEP 3 — PUSH TO GITHUB
# ─────────────────────────────────────────────

# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/hpcl-rti-analytics.git
git branch -M main
git push -u origin main


# ─────────────────────────────────────────────
# STEP 4 — ADD TOPICS (on GitHub website)
# ─────────────────────────────────────────────

# After pushing, go to your repo on GitHub:
# Click the gear icon ⚙️ next to "About"
# Add these topics:
#   python  data-analysis  sql  power-bi  rti  hpcl
#   pandas  matplotlib  data-visualization  internship
#   sqlite  jupyter-notebook  eda  business-analytics

# Description to set:
# "10-year RTI filing pattern analysis at HPCL — Python, SQL & Power BI"


# ─────────────────────────────────────────────
# STEP 5 — BEFORE SHARING YOUR REPO LINK
# ─────────────────────────────────────────────

# 1. Update README.md:
#    - Replace "yourusername" with your actual GitHub username
#    - Replace "your.email@example.com" with your email
#    - Replace the LinkedIn link with your actual profile

# 2. Commit the updated README:
git add README.md
git commit -m "Update contact links in README"
git push


# ─────────────────────────────────────────────
# STEP 6 — AFTER ADDING POWER BI FILE
# ─────────────────────────────────────────────

# After building the dashboard and saving hpcl_rti_dashboard.pbix:
# Copy it to the dashboard/ folder, then:
git add dashboard/hpcl_rti_dashboard.pbix
git commit -m "Add Power BI dashboard — 6 pages, 28 DAX measures"
git push
