-- PostgreSQL Database Setup Script
-- This script creates the database, user, and tables for the FastAPI application

-- ========================================
-- 1. Create User and Database
-- ========================================
-- Run these commands as postgres superuser
-- sudo -u postgres psql

CREATE USER apiuser WITH PASSWORD 'yourpassword';
CREATE DATABASE apidb OWNER apiuser;
GRANT ALL PRIVILEGES ON DATABASE apidb TO apiuser;

-- ========================================
-- 2. Connect to the database
-- ========================================
-- \c apidb
-- Or: psql -U apiuser -d apidb

-- ========================================
-- 3. Create Tables
-- ========================================

CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX idx_items_name ON items(name);
CREATE INDEX idx_items_created_at ON items(created_at);

-- ========================================
-- 4. Insert Sample Data
-- ========================================

INSERT INTO items (name, description, price, quantity) VALUES
('Laptop', 'High-performance laptop for development', 25000.00, 10),
('Mouse', 'Wireless mouse with ergonomic design', 500.00, 50),
('Keyboard', 'Mechanical keyboard with RGB backlight', 2500.00, 30),
('Monitor', '27-inch 4K display', 8900.00, 15),
('Headphones', 'Noise-cancelling headphones', 3500.00, 25);

-- ========================================
-- 5. Verification Queries
-- ========================================

-- Check table structure
\d items

-- View all items
SELECT * FROM items;

-- Count items
SELECT COUNT(*) as total_items FROM items;

-- Check database size
SELECT pg_size_pretty(pg_database_size('apidb')) as database_size;

-- ========================================
-- 6. Additional Useful Queries
-- ========================================

-- Get items with low stock
-- SELECT * FROM items WHERE quantity < 20;

-- Get total inventory value
-- SELECT SUM(price * quantity) as total_value FROM items;

-- Get average item price
-- SELECT AVG(price) as avg_price FROM items;
