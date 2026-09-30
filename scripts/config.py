import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "password")
DB_NAME = os.getenv("DB_NAME", "ecommerce_analytics")
DB_PORT = os.getenv("DB_PORT", "3306")

INVENTORY_VELOCITY_THRESHOLD = 1500
TOP_VIP_PERCENTILE_LIMIT = 0.20
