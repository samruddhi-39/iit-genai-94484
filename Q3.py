# Q3:
# Given a CSV file Products.csv with columns:
# Write a Python program to:
# a) Read the CSV
# b) Print each row in a clean format
# c) Total number of rows
# d) Total number of products priced above 500
# e) Average price of all products
# f) List all products belonging to a specific category (user input)
# g) Total quantity of all items in stock

import csv
filename = "products.csv"
products = []
with open(filename, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        row["price"] = float(row["price"])
        row["quantity"] = int(row["quantity"])
        products.append(row)

print("\n--- Product List ---")
for p in products:
    print(f"ID: {p['product_id']}, Name: {p['product_name']}, "
          f"Category: {p['category']}, Price: {p['price']}, "
          f"Quantity: {p['quantity']}")

print("\nTotal number of rows:", len(products))

above_500 = sum(1 for p in products if p["price"] > 500)
print("Products priced above 500:", above_500)

avg_price = sum(p["price"] for p in products) / len(products)
print("Average price of all products:", avg_price)

category = input("\nEnter category: ").strip()

print(f"\nProducts in category '{category}':")
found = False
for p in products:
    if p["category"].lower() == category.lower():
        print(f"- {p['product_name']} (Price: {p['price']}, Qty: {p['quantity']})")
        found = True

if not found:
    print("No products found in this category.")

total_quantity = sum(p["quantity"] for p in products)
print("\nTotal quantity of all items in stock:", total_quantity)
