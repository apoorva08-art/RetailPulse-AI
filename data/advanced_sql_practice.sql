-- How does cumulative revenue change over time?

SELECT
    order_date,
    SUM(sales) AS Daily_Revenue,
    SUM(SUM(sales)) OVER(ORDER BY order_date) AS Running_Revenue
FROM orders
GROUP BY order_date;


-- How does cumulative profit change over time?

SELECT
    order_date,
    SUM(profit) AS Daily_Profit,
    SUM(SUM(profit)) OVER(ORDER BY order_date) AS Running_Profit
FROM orders
GROUP BY order_date;


-- Which weekdays generate the highest revenue?

SELECT
    DAYNAME(order_date) AS Weekday,
    ROUND(SUM(sales),2) AS Revenue
FROM orders
GROUP BY DAYNAME(order_date)
ORDER BY Revenue DESC;


-- Do weekends generate more revenue than weekdays?

SELECT
    CASE
        WHEN DAYOFWEEK(order_date) IN (1,7) THEN 'Weekend'
        ELSE 'Weekday'
    END AS Day_Type,
    ROUND(SUM(sales),2) AS Revenue
FROM orders
GROUP BY Day_Type;


-- Which customers belong to each revenue quartile?

SELECT
    c.customer_name,
    ROUND(SUM(o.sales),2) AS Revenue,
    NTILE(4) OVER(ORDER BY SUM(o.sales) DESC) AS Revenue_Quartile
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
GROUP BY c.customer_name;


-- Which payment mode generates the highest revenue?

SELECT
    payment_mode,
    ROUND(SUM(sales),2) AS Revenue
FROM orders
GROUP BY payment_mode
ORDER BY Revenue DESC;


-- Which payment mode generates the highest profit?

SELECT
    payment_mode,
    ROUND(SUM(profit),2) AS Profit
FROM orders
GROUP BY payment_mode
ORDER BY Profit DESC;


-- Which brand generates the highest revenue?

SELECT
    p.brand,
    ROUND(SUM(o.sales),2) AS Revenue
FROM orders o
JOIN products p
ON o.product_id = p.product_id
GROUP BY p.brand
ORDER BY Revenue DESC;


-- Which region has the highest average order value?

SELECT
    s.region,
    ROUND(AVG(o.sales),2) AS Average_Order_Value
FROM orders o
JOIN stores s
ON o.store_id = s.store_id
GROUP BY s.region
ORDER BY Average_Order_Value DESC;


-- Which customer segment receives the highest average discount?

SELECT
    c.segment,
    ROUND(AVG(o.discount),2) AS Average_Discount
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
GROUP BY c.segment
ORDER BY Average_Discount DESC;


-- How do stores rank based on total revenue?

SELECT
    s.store_name,
    ROUND(SUM(o.sales),2) AS Revenue,
    RANK() OVER(ORDER BY SUM(o.sales) DESC) AS Store_Rank
FROM orders o
JOIN stores s
ON o.store_id = s.store_id
GROUP BY s.store_name;


-- Which stores have the highest number of returned orders?

SELECT
    s.store_name,
    COUNT(r.return_id) AS Total_Returns
FROM returns r
JOIN orders o
ON r.order_id = o.order_id
JOIN stores s
ON o.store_id = s.store_id
GROUP BY s.store_name
ORDER BY Total_Returns DESC;


-- Which product is the best seller within each category?

WITH RankedProducts AS
(
SELECT
    p.category,
    p.product_name,
    SUM(o.quantity) AS Quantity_Sold,
    RANK() OVER(
        PARTITION BY p.category
        ORDER BY SUM(o.quantity) DESC
    ) AS Product_Rank
FROM orders o
JOIN products p
ON o.product_id = p.product_id
GROUP BY p.category, p.product_name
)

SELECT *
FROM RankedProducts
WHERE Product_Rank = 1;


-- Which products have the lowest revenue?

SELECT
    p.product_name,
    ROUND(SUM(o.sales),2) AS Revenue
FROM orders o
JOIN products p
ON o.product_id = p.product_id
GROUP BY p.product_name
ORDER BY Revenue
LIMIT 10;


-- Which stores generate the highest profit?

SELECT
    s.store_name,
    ROUND(SUM(o.profit),2) AS Profit
FROM orders o
JOIN stores s
ON o.store_id = s.store_id
GROUP BY s.store_name
ORDER BY Profit DESC;


-- Which brands have the highest profit margin?

SELECT
    p.brand,
    ROUND(SUM(o.sales),2) AS Revenue,
    ROUND(SUM(o.profit),2) AS Profit,
    ROUND((SUM(o.profit)/SUM(o.sales))*100,2) AS Profit_Margin
FROM orders o
JOIN products p
ON o.product_id = p.product_id
GROUP BY p.brand
ORDER BY Profit_Margin DESC;


-- Which customers placed the highest number of orders?

SELECT
    c.customer_name,
    COUNT(o.order_id) AS Total_Orders
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY Total_Orders DESC
LIMIT 10;


-- Which product categories receive the highest average discount?

SELECT
    p.category,
    ROUND(AVG(o.discount),2) AS Average_Discount
FROM orders o
JOIN products p
ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY Average_Discount DESC;