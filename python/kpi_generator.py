from pathlib import Path
import pandas as pd

# ==========================================
# Load Data
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

orders = pd.read_csv(DATA_DIR / "orders.csv")
products = pd.read_csv(DATA_DIR / "products.csv")
customers = pd.read_csv(DATA_DIR / "customers.csv")
stores = pd.read_csv(DATA_DIR / "stores.csv")
returns = pd.read_csv(DATA_DIR / "returns.csv")

# ==========================================
# Merge Tables
# ==========================================

sales_df = (
    orders
    .merge(products, on="product_id")
    .merge(customers, on="customer_id", suffixes=("", "_customer"))
    .merge(stores, on="store_id", suffixes=("_customer", "_store"))
)

# ==========================================
# Executive KPIs
# ==========================================

total_revenue = sales_df["sales"].sum()
total_profit = sales_df["profit"].sum()
profit_margin = (total_profit / total_revenue) * 100

total_orders = sales_df["order_id"].nunique()

aov = total_revenue / total_orders

return_rate = (
    returns["order_id"].nunique() /
    total_orders
) * 100

top_category = (
    sales_df.groupby("category")["sales"]
    .sum()
    .idxmax()
)

top_product = (
    sales_df.groupby("product_name")["sales"]
    .sum()
    .idxmax()
)

top_customer = (
    sales_df.groupby("customer_name")["sales"]
    .sum()
    .idxmax()
)

top_city = (
    sales_df.groupby("city_store")["profit"]
    .sum()
    .idxmax()
)

top_region = (
    sales_df.groupby("region")["profit"]
    .sum()
    .idxmax()
)

category_margin = (
    sales_df.groupby("category")[["sales", "profit"]]
    .sum()
)

category_margin["profit_margin"] = (
    category_margin["profit"] /
    category_margin["sales"]
) * 100

highest_margin_category = (
    category_margin["profit_margin"]
    .idxmax()
)

top_return_reason = (
    returns["return_reason"]
    .value_counts()
    .idxmax()
)

least_profitable_discount = (
    sales_df.groupby("discount")["profit"]
    .mean()
    .idxmin()
)

# ==========================================
# Additional Business Insights
# ==========================================

top_5_products = (
    sales_df.groupby("product_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .round(2)
    .to_dict()
)

top_5_customers = (
    sales_df.groupby("customer_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .round(2)
    .to_dict()
)

top_5_stores = (
    sales_df.groupby("store_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .round(2)
    .to_dict()
)

top_5_cities = (
    sales_df.groupby("city_store")["profit"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .round(2)
    .to_dict()
)

return_reason_breakdown = (
    returns["return_reason"]
    .value_counts()
    .to_dict()
)

# ==========================================
# KPI Dictionary
# ==========================================

kpis = {

    "Total Revenue": round(total_revenue,2),
    "Total Profit": round(total_profit,2),
    "Profit Margin (%)": round(profit_margin,2),
    "Average Order Value": round(aov,2),
    "Return Rate (%)": round(return_rate,2),

    "Top Revenue Category": top_category,
    "Highest Revenue Product": top_product,
    "Top Customer": top_customer,
    "Highest Profit City": top_city,
    "Highest Profit Region": top_region,
    "Highest Margin Category": highest_margin_category,
    "Most Common Return Reason": top_return_reason,
    "Least Profitable Discount (%)": least_profitable_discount,

    "Top 5 Products by Revenue": top_5_products,
    "Top 5 Customers by Revenue": top_5_customers,
    "Top 5 Stores by Revenue": top_5_stores,
    "Top 5 Cities by Profit": top_5_cities,
    "Return Reason Breakdown": return_reason_breakdown

}

# ==========================================
# Display KPIs
# ==========================================

if __name__ == "__main__":

    print("="*60)
    print("EXECUTIVE KPI SUMMARY")
    print("="*60)

    for key,value in kpis.items():
        print(f"{key:<35}: {value}")