-- =============================================================================
-- Customer Lifetime Value (CLV) & Top Category Preference Ranking
-- Objective: Compute cumulative revenue/profit per customer and map their 
-- primary product category preference for the Top 20% high-margin cohort.
-- Engine: MySQL 8.0
-- =============================================================================

USE ecommerce_analytics;

WITH CustomerCategoryTotals AS (
    -- Step 1: Calculate aggregate sales & profit per customer per category and rank them
    SELECT 
        customer_name,
        category,
        SUM(sales) AS total_category_sales,
        SUM(profit) AS total_category_profit,
        ROW_NUMBER() OVER (
            PARTITION BY customer_name 
            ORDER BY SUM(sales) DESC
        ) AS category_rank
    FROM sales
    GROUP BY customer_name, category
),
CustomerLifetimeTotals AS (
    -- Step 2: Aggregate macro customer lifetime metrics across all orders
    SELECT 
        customer_name,
        COUNT(order_id) AS total_orders,
        SUM(sales) AS lifetime_revenue,
        SUM(profit) AS total_clv_profit,
        NTILE(5) OVER (ORDER BY SUM(profit) DESC) AS profit_percentile_bucket
    FROM sales
    GROUP BY customer_name
)
-- Step 3: Join lifetime aggregates with primary category preference (Rank 1)
-- Filter for Top 20% (bucket = 1) high-margin customers
SELECT 
    clt.customer_name,
    clt.total_orders,
    clt.lifetime_revenue,
    clt.total_clv_profit,
    ROUND((clt.total_clv_profit / clt.lifetime_revenue) * 100, 2) AS profit_margin_pct,
    cct.category AS primary_shopping_category,
    cct.total_category_sales AS primary_category_revenue
FROM CustomerLifetimeTotals clt
JOIN CustomerCategoryTotals cct 
    ON clt.customer_name = cct.customer_name
WHERE cct.category_rank = 1 
  AND clt.profit_percentile_bucket = 1
ORDER BY clt.total_clv_profit DESC;
