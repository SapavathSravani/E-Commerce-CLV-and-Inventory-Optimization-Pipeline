WITH CustomerCategoryTotals AS (
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
    SELECT 
        customer_name,
        COUNT(order_id) AS total_orders,
        SUM(sales) AS lifetime_revenue,
        SUM(profit) AS total_clv_profit,
        NTILE(5) OVER (ORDER BY SUM(profit) DESC) AS profit_percentile_bucket
    FROM sales
    GROUP BY customer_name
)
SELECT 
    clt.customer_name,
    clt.total_orders,
    clt.lifetime_revenue,
    clt.total_clv_profit,
    cct.category AS primary_shopping_category
FROM CustomerLifetimeTotals clt
JOIN CustomerCategoryTotals cct ON clt.customer_name = cct.customer_name
WHERE cct.category_rank = 1 
  AND clt.profit_percentile_bucket = 1
ORDER BY clt.total_clv_profit DESC;
