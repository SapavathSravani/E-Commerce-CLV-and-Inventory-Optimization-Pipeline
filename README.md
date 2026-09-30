# E-Commerce Customer Lifetime Value (CLV) & Inventory Optimization Pipeline

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?style=for-the-badge&logo=mysql&logoColor=white)
![PowerBI](https://img.shields.io/badge/Power_BI-Desktop-yellow?style=for-the-badge&logo=powerbi&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## Project Overview

Modern e-commerce enterprises generate massive volumes of transactional data daily. However, extracting actionable insights to balance customer retention marketing and inventory logistics remains an operational challenge. 

This project implements an end-to-end multi-tiered data engineering and business analytics pipeline that processes **5,000 enterprise transactional records** (spanning 2023 to 2025) across **4,844 unique customers** and **10 product categories**. 

### Core Business Metrics & Results
* **Total Aggregated Revenue:** ₹533.67 Million
* **Total Net Profit:** ₹79.71 Million
* **Net Profit Margin:** **14.94%**
* **Top Profit-Generating Categories:** Furniture (₹8.69M / 10.91%) & Home Decor (₹8.56M / 10.74%)
* **High-Demand Stock Out Alerts Triggered:** 5 Categories (>1,500 units sold threshold)

---

## Technical Architecture

```text
┌────────────────┐      ┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Source Logs   │ ───► │  MySQL Engine   │ ───► │  Power BI Cockpit │ ───► │ Python Backend  │
│ 5k Trans. CSV  │      │ SQL CTEs & Window│      │  Payment Heatmap │      │ Stock Velocity  │
│ (Raw File)     │      │ Functions (8.0) │      │  Category Share  │      │ Audit & Alerts  │
└────────────────┘      └─────────────────┘      └──────────────────┘      └─────────────────┘l/schema.sql
mysql -u root -p < sql/clv_segmentation.sql

Execution Log Output
 [INFO] Successfully connected to MySQL database engine.
 [INFO] Retrieved 969 Top 20% VIP customer records.
 [INFO] Executing inventory stock velocity audit...

============================================================
         AUTOMATED WAREHOUSE INVENTORY AUDIT REPORT         
============================================================
! ALERT: High demand surge detected in [Furniture]. Units Sold: 1,591 | Action: Trigger automated restocking plan.
! ALERT: High demand surge detected in [Books]. Units Sold: 1,571 | Action: Trigger automated restocking plan.
! ALERT: High demand surge detected in [Kitchen]. Units Sold: 1,544 | Action: Trigger automated restocking plan.
! ALERT: High demand surge detected in [Home Decor]. Units Sold: 1,539 | Action: Trigger automated restocking plan.
! ALERT: High demand surge detected in [Clothing]. Units Sold: 1,513 | Action: Trigger automated restocking plan.
============================================================

 [INFO] Pipeline audit completed successfully.

1. Clone Repository & Setup Environment
git clone [https://github.com/SapavathSravani/ecommerce-clv-inventory-pipeline.git](https://github.com/SapavathSravani/ecommerce-clv-inventory-pipeline.git)
cd ecommerce-clv-inventory-pipeline

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt


