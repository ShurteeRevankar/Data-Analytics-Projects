import pandas as pd
# Load datasets
orders = pd.read_csv(r"D:\ReadyNest_Internship\Week2\ReadyNest_Olist_BI\data\olist_orders.csv")
customers = pd.read_csv(r"D:\ReadyNest_Internship\Week2\ReadyNest_Olist_BI\data\olist_customers.csv")
items = pd.read_csv(r"D:\ReadyNest_Internship\Week2\ReadyNest_Olist_BI\data\olist_order_items.csv")
payments = pd.read_csv(r"D:\ReadyNest_Internship\Week2\ReadyNest_Olist_BI\data\olist_order_payments.csv")
products = pd.read_csv(r"D:\ReadyNest_Internship\Week2\ReadyNest_Olist_BI\data\olist_products.csv")


# Merge orders + customers
master = pd.merge(
    orders,
    customers,
    on="customer_id",
    how="left"
)

# Merge master + items
master = pd.merge(
    master,
    items,
    on="order_id",
    how="left"
)

# Merge master + products
master = pd.merge(
    master,
    products,
    on="product_id",
    how="left"
)

# Merge master + payments
master = pd.merge(
    master,
    payments,
    on="order_id",
    how="left"
)

master.to_csv("data/master_olist.csv", index=False)

print("Master dataset created!")

print("\nMaster Dataset Shape:", master.shape)
print("\nColumns:")
print(master.columns.tolist())

print("\nFirst 5 Rows:")
print(master.head())