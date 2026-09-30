"""
E-Commerce Automated Database Auditor & Inventory Velocity Monitor
Author: Senior Data Engineer
Description: Programmatically extracts high-margin VIP customer cohorts and
             monitors inventory turnover rates to trigger automated restock alerts.
"""

import logging
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class InventoryPipelineMonitor:
    def __init__(self):
        self.db_url = f"mysql+pymysql://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
        self.engine = None

    def connect(self):
        try:
            self.engine = create_engine(self.db_url, pool_pre_ping=True)
            logging.info("Successfully connected to MySQL database engine.")
        except SQLAlchemyError as e:
            logging.error(f"Failed to initialize database connection: {e}")
            raise

    def fetch_top_vip_customers(self, percentile: float = config.TOP_VIP_PERCENTILE_LIMIT):
        """Extracts top high-margin customers mapped to primary categories."""
        query = text("""
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
                    NTILE(5) OVER (ORDER BY SUM(profit) DESC) AS profit_bucket
                FROM sales
                GROUP BY customer_name
            )
            SELECT 
                clt.customer_name,
                clt.total_orders,
                clt.lifetime_revenue,
                clt.total_clv_profit,
                cct.category AS primary_category
            FROM CustomerLifetimeTotals clt
            JOIN CustomerCategoryTotals cct ON clt.customer_name = cct.customer_name
            WHERE cct.category_rank = 1 AND clt.profit_bucket = 1
            ORDER BY clt.total_clv_profit DESC;
        """)
        
        try:
            df_vip = pd.read_sql(query, con=self.engine)
            logging.info(f"Retrieved {len(df_vip)} Top 20% VIP customer records.")
            return df_vip
        except SQLAlchemyError as e:
            logging.error(f"Error fetching VIP cohort: {e}")
            return pd.DataFrame()

    def run_inventory_velocity_audit(self, threshold: int = config.INVENTORY_VELOCITY_THRESHOLD):
        """Audits category unit sales velocity and outputs stock alerts."""
        query = text("""
            SELECT category, SUM(quantity) AS total_units_sold
            FROM sales
            GROUP BY category
            HAVING total_units_sold > :threshold
            ORDER BY total_units_sold DESC;
        """)
        
        try:
            df_inventory = pd.read_sql(query, con=self.engine, params={"threshold": threshold})
            
            print("\n" + "="*60)
            print("         AUTOMATED WAREHOUSE INVENTORY AUDIT REPORT         ")
            print("="*60)
            
            if not df_inventory.empty:
                for idx, row in df_inventory.iterrows():
                    print(f" ALERT: High demand surge detected in [{row['category']}]. "
                          f"Units Sold: {int(row['total_units_sold']):,} | "
                          f"Action: Trigger automated restocking plan.")
            else:
                print(" OK: All product category stock velocities are within stable limits.")
            print("="*60 + "\n")
            
        except SQLAlchemyError as e:
            logging.error(f"Error conducting inventory audit: {e}")

    def execute_pipeline(self):
        self.connect()
        logging.info("Running Customer Lifetime Value cohort analysis...")
        _ = self.fetch_top_vip_customers()
        logging.info("Executing inventory stock velocity audit...")
        self.run_inventory_velocity_audit()
        logging.info("Pipeline audit completed successfully.")

if __name__ == "__main__":
    monitor = InventoryPipelineMonitor()
    monitor.execute_pipeline()
