-- Database Initialization & Table Schema Setup
CREATE DATABASE IF NOT EXISTS ecommerce_analytics;
USE ecommerce_analytics;

DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    order_id VARCHAR(50) PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    region VARCHAR(50),
    category VARCHAR(100) NOT NULL,
    sub_category VARCHAR(100) NOT NULL,
    product_name VARCHAR(255),
    quantity INT NOT NULL,
    sales DECIMAL(12,2) NOT NULL,
    profit DECIMAL(12,2) NOT NULL,
    payment_mode VARCHAR(50)
);

CREATE INDEX idx_customer_name ON sales(customer_name);
CREATE INDEX idx_category ON sales(category);
CREATE INDEX idx_order_date ON sales(order_date);
