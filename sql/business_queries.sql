CREATE DATABASE retail_analytics;
USE retail_analytics;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    gender VARCHAR(10),
    age INT,
    city VARCHAR(50),
    state VARCHAR(50),
    segment VARCHAR(30)
);
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    subcategory VARCHAR(50),
    cost_price DECIMAL(10,2),
    selling_price DECIMAL(10,2)
);

CREATE TABLE stores (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    region VARCHAR(30),
    manager_name VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    order_date DATE,
    customer_id INT,
    product_id INT,
    store_id INT,
    quantity INT,
    sales DECIMAL(10,2),
    discount DECIMAL(5,2),
    profit DECIMAL(10,2),

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (store_id) REFERENCES stores(store_id)
);
CREATE TABLE returns (
    return_id INT PRIMARY KEY,
    order_id INT,
    return_status VARCHAR(20),
    return_reason VARCHAR(100),

    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);


ALTER TABLE orders
ADD COLUMN payment_mode VARCHAR(30);

ALTER TABLE orders
ADD COLUMN order_status VARCHAR(30);

ALTER TABLE products
ADD brand VARCHAR(50);

SHOW TABLES;
DESC orders;

SHOW VARIABLES LIKE 'secure_file_priv';

SELECT*FROM returns;

SET SQL_SAFE_UPDATES = 0;
DELETE FROM orders;

SET SQL_SAFE_UPDATES = 1;

SHOW VARIABLES LIKE 'secure_file_priv';

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/orders.csv'
INTO TABLE orders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_id, order_date, customer_id, product_id, store_id,
 quantity, sales, discount, profit, payment_mode, order_status)
 ;
 
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/returns.csv'
INTO TABLE returns
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(return_id, order_id, return_status, return_reason);

-- Business Analysis Queries
-- 1. Which month generated the highest revenue?

SELECT
    YEAR(order_date) AS Year,
    MONTHNAME(order_date) AS Month,
    ROUND(SUM(sales),2) AS Revenue
FROM orders
GROUP BY YEAR(order_date), MONTH(order_date), MONTHNAME(order_date)
ORDER BY Revenue DESC
LIMIT 1;

-- 2. How has sales grown month-over-month?

WITH monthly_sales AS
(
SELECT
YEAR(order_date) AS Year,
MONTH(order_date) AS Month,
SUM(sales) AS Revenue
FROM orders
GROUP BY YEAR(order_date),MONTH(order_date)
)

SELECT Year, Month,
ROUND(Revenue,2) AS Revenue,
ROUND(
((Revenue-LAG(Revenue) OVER(ORDER BY Year,Month))
/ LAG(Revenue) OVER(ORDER BY Year,Month))*100,2) 
AS Growth_Percentage
FROM monthly_sales;


-- 3. Which product categories contribute the most revenue?

SELECT
p.category, ROUND(SUM(o.sales),2) AS Revenue,
ROUND( SUM(o.sales)*100/
(SELECT SUM(sales) FROM orders),2
) AS Revenue_Contribution_Percentage
FROM orders o
JOIN products p
ON o.product_id=p.product_id
GROUP BY p.category
ORDER BY Revenue DESC;


-- 4. Which category has the highest profit margin?

SELECT
p.category,
ROUND(SUM(o.sales),2) AS Revenue,
ROUND(SUM(o.profit),2) AS Profit,
ROUND((SUM(o.profit)/SUM(o.sales))*100,2) AS Profit_Margin
FROM orders o
JOIN products p
ON o.product_id=p.product_id
GROUP BY p.category
ORDER BY Profit_Margin DESC;

-- 5. Top 10 revenue-generating products

SELECT
p.product_name,
ROUND(SUM(o.sales),2) AS Revenue
FROM orders o
JOIN products p
ON o.product_id=p.product_id
GROUP BY p.product_name
ORDER BY Revenue DESC
LIMIT 10;


-- 6. Which products generate high sales but low profit?

SELECT
p.product_name,
ROUND(SUM(o.sales),2) AS Revenue,
ROUND(SUM(o.profit),2) AS Profit
FROM orders o
JOIN products p
ON o.product_id=p.product_id
GROUP BY p.product_name
HAVING SUM(o.sales)>500000
AND SUM(o.profit)<50000;


-- 7. Rank products within each category based on revenue
SELECT
p.category,
p.product_name,
ROUND(SUM(o.sales),2) AS Revenue,
RANK() OVER(
PARTITION BY p.category
ORDER BY SUM(o.sales) DESC
) AS Product_Rank
FROM orders o
JOIN products p
ON o.product_id=p.product_id
GROUP BY p.category,p.product_name;

-- 8. Which stores perform above average revenue?

SELECT
s.store_name,
ROUND(SUM(o.sales),2) AS Revenue
FROM orders o
JOIN stores s
ON o.store_id=s.store_id
GROUP BY s.store_name
HAVING SUM(o.sales)>
(SELECT AVG(StoreRevenue)
FROM
(SELECT SUM(sales) AS StoreRevenue
FROM orders
GROUP BY store_id )x );

-- 9. Top 10 customers by lifetime value
SELECT
c.customer_name,
ROUND(SUM(o.sales),2) AS Lifetime_Value
FROM orders o
JOIN customers c
ON o.customer_id=c.customer_id
GROUP BY c.customer_name
ORDER BY Lifetime_Value DESC
LIMIT 10;


-- 10. Overall return rate
SELECT
ROUND(COUNT(DISTINCT r.order_id)*100/
COUNT(DISTINCT o.order_id),2
) AS Return_Rate
FROM orders o
LEFT JOIN returns r
ON o.order_id=r.order_id;


-- 11. Most common return reasons

SELECT
return_reason,
COUNT(*) AS Total_Returns
FROM returns
GROUP BY return_reason
ORDER BY Total_Returns DESC;


-- 12. Which cities generate the highest profit?

SELECT s.city,
ROUND(SUM(o.profit),2) AS Profit
FROM orders o
JOIN stores s
ON o.store_id=s.store_id
GROUP BY s.city
ORDER BY Profit DESC
LIMIT 10;

SELECT
p.product_name,
ROUND(SUM(o.sales),2) AS Revenue,
ROUND(SUM(o.profit),2) AS Profit
FROM orders o
JOIN products p
ON o.product_id = p.product_id
GROUP BY p.product_name
HAVING SUM(o.sales) > 500000
AND SUM(o.profit) < 50000;