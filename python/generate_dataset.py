import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta



# Make the dataset reproducible
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# Create Faker object
fake = Faker("en_IN")

customers = []
segments = [
    "Consumer",
    "Corporate",
    "Home Office"
]

genders = [
    "Male",
    "Female"
]

for i in range(1, 501):

    customer = {
        "customer_id": i,
        "customer_name": fake.name(),
        "gender": random.choice(genders),
        "age": random.randint(18, 65),
        "city": fake.city(),
        "state": fake.state(),
        "segment": random.choice(segments)
    }

    customers.append(customer)

customers_df = pd.DataFrame(customers)

customers_df.to_csv(
    "data/customers.csv",
    index=False
)

print("customers.csv created successfully!")

# -------------------- PRODUCTS --------------------

products = []

catalog = {
    "Electronics": {
        "Laptop": ["Dell", "HP", "Lenovo", "Asus"],
        "Smartphone": ["Samsung", "Apple", "OnePlus", "Xiaomi"],
        "Headphones": ["Boat", "Sony", "JBL", "Noise"],
        "Keyboard": ["Logitech", "HP", "Dell", "Redgear"],
        "Mouse": ["Logitech", "Dell", "HP", "Redgear"]
    },
    "Furniture": {
        "Chair": ["Nilkamal", "Godrej", "Ikea"],
        "Table": ["Godrej", "Ikea", "Nilkamal"],
        "Desk": ["Godrej", "Ikea"],
        "Wardrobe": ["Godrej", "Ikea"],
        "Sofa": ["HomeTown", "Ikea"]
    },
    "Clothing": {
        "T-Shirt": ["Nike", "Puma", "Adidas"],
        "Jeans": ["Levis", "Wrangler", "Lee"],
        "Jacket": ["Nike", "Puma"],
        "Kurta": ["FabIndia", "Manyavar"],
        "Shoes": ["Nike", "Adidas", "Puma"]
    },
    "Grocery": {
        "Rice": ["India Gate", "Fortune"],
        "Sugar": ["Madhur", "Trust"],
        "Tea": ["Tata Tea", "Red Label"],
        "Coffee": ["Nescafe", "Bru"],
        "Milk": ["Amul", "Mother Dairy"]
    },
    "Sports": {
        "Football": ["Nivia", "Cosco"],
        "Cricket Bat": ["SG", "SS", "MRF"],
        "Yoga Mat": ["Boldfit", "AmazonBasics"],
        "Dumbbell": ["Kore", "Aurion"],
        "Tennis Racket": ["Yonex", "Wilson"]
    }
}

product_id = 1

for category, subcats in catalog.items():

    for subcategory, brands in subcats.items():

        for brand in brands:

            products.append({

                "product_id": product_id,

                "product_name": f"{brand} {subcategory}",

                "category": category,

                "subcategory": subcategory,

                "brand": brand,

                "cost_price": random.randint(200,5000),

                "selling_price": random.randint(550,7000)

            })

            product_id += 1

products_df = pd.DataFrame(products)

products_df.to_csv("data/products.csv",index=False)

print("products.csv created successfully!")


#-------------------- STORES --------------------

stores = []

cities = [
    ("Delhi","Delhi","North"),
    ("Mumbai","Maharashtra","West"),
    ("Pune","Maharashtra","West"),
    ("Bengaluru","Karnataka","South"),
    ("Chennai","Tamil Nadu","South"),
    ("Hyderabad","Telangana","South"),
    ("Kolkata","West Bengal","East"),
    ("Patna","Bihar","East"),
    ("Lucknow","Uttar Pradesh","North"),
    ("Jaipur","Rajasthan","North")
]

for i in range(1,21):

    city,state,region = random.choice(cities)

    stores.append({

        "store_id":i,

        "store_name":f"Retail Store {i}",

        "city":city,

        "state":state,

        "region":region,

        "manager_name":fake.name()

    })

stores_df = pd.DataFrame(stores)

stores_df.to_csv("data/stores.csv",index=False)

print("stores.csv created successfully!")


##-------------------- ORDERS --------------------

customers_df = pd.read_csv("data/customers.csv")
products_df = pd.read_csv("data/products.csv")
stores_df = pd.read_csv("data/stores.csv")

orders = []

start_date = datetime(2023,1,1)
end_date = datetime(2025,12,31)

for order_id in range(1,10001):

    customer = customers_df.sample(1).iloc[0]
    product = products_df.sample(1).iloc[0]
    store = stores_df.sample(1).iloc[0]

    quantity = random.randint(1,5)

    discount = random.choice([0,5,10,15,20,25,30])

    sales = quantity * product["selling_price"]

    sales_after_discount = sales * (1-discount/100)

    profit = sales_after_discount - (quantity*product["cost_price"])

    random_days = random.randint(
        0,
        (end_date-start_date).days
    )

    order_date = start_date + timedelta(days=random_days)

    orders.append({

        "order_id":order_id,

        "order_date":order_date.date(),

        "customer_id":customer["customer_id"],

        "product_id":product["product_id"],

        "store_id":store["store_id"],

        "quantity":quantity,

        "sales":round(sales_after_discount,2),

        "discount":discount,

        "profit":round(profit,2),

        "payment_mode":random.choice([
            "UPI",
            "Credit Card",
            "Debit Card",
            "Cash",
            "Net Banking"
        ]),

        "order_status":random.choice([
            "Delivered",
            "Delivered",
            "Delivered",
            "Delivered",
            "Cancelled",
            "Returned"
        ])

    })

orders_df = pd.DataFrame(orders)

orders_df.to_csv("data/orders.csv",index=False)

print("orders.csv created successfully!")




# -------------------- RETURNS --------------------

# -------------------- RETURNS --------------------

orders_df = pd.read_csv("data/orders.csv")

returned_orders = orders_df[
    orders_df["order_status"] == "Returned"
]

reasons = [
    "Damaged Product",
    "Wrong Item",
    "Late Delivery",
    "Customer Changed Mind",
    "Defective Product"
]

returns = []

for i, (_, row) in enumerate(returned_orders.iterrows(), start=1):

    returns.append({

        "return_id": i,

        "order_id": row["order_id"],

        "return_status": "Returned",

        "return_reason": random.choice(reasons)

    })

returns_df = pd.DataFrame(returns)

returns_df.to_csv("data/returns.csv", index=False)

print("returns.csv created successfully!")