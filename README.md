# E-Commerce Customer Lifetime Value (CLV) & Inventory Optimization Pipeline

An end-to-end data engineering and analytics pipeline built to process transactional e-commerce data, compute Customer Lifetime Value (CLV), isolate high-margin VIP customer cohorts, and automate backend warehouse inventory monitoring[cite: 1].

## Key Achievements & Resume Highlights
• Analyzed 5k e-commerce transactions using MySQL 8.0 to aggregate 533.67M in revenue, maintaining a 14.94% net profit margin
• Engineered SQL CTEs and window functions to compute Customer Lifetime Value, mapping category preferences for top customer cohorts
• Automated Python/Pandas monitoring script using PyMySQL, generating programmatic alerts for warehouse inventory optimization

---

## Project Overview & Key Architecture

The pipeline processes **5,000 transaction records** spanning 731 days (October 2023 – October 2025) across **4,844 unique customers** and **10 distinct product categories**[cite: 1].

### 4-Tier Pipeline Design
1. **Tier 1: Data Hygiene & Ingestion (Excel/CSV)** – Initial cleaning, data validation, and basic baseline modeling
2. **Tier 2: Relational Data Store (MySQL 8.0)** – Schema definition, dual CTEs, and window-function ranking (`ROW_NUMBER() OVER (PARTITION BY ...)`)
3. **Tier 3: Executive Analytics (Power BI)** – Dashboard modeling, payment preference heatmaps, and category profitability share analysis
4. **Tier 4: Automated Backend & Monitoring (Python 3.10+)** – Dynamic database audits via `SQLAlchemy`/`PyMySQL` triggering inventory restock velocity alerts

---

## Analytical Key Metrics

| Metric | Value |
| :--- | :--- |
| **Total Transaction Records** | 5,000 |
| **Total Active Customers** | 4,844 |
| **Total Generated Revenue** | ₹533,666,024.35 (~₹533.67M)|
| **Total Net Profit** | ₹79,708,734.91 (~₹79.71M) |
| **Net Profit Margin** | **14.94%** |
| **Top Performing Category by Profit** | Home Decor (₹8.69M / 10.91% share) |

---

## Setup & Execution Instructions

### Prerequisites
- MySQL Server 8.0+
- Python 3.10+
- Power BI Desktop (optional, for viewing dashboard)

### 1. Database Setup
Execute the SQL schema and analytical transformation files:
```bash
mysql -u root -p < sql/schema.sql
mysql -u root -p < sql/clv_segmentation.sql
