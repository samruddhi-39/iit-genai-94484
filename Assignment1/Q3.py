import csv

# a) Read the CSV
filename = "products.csv"
products = []

with open(filename, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        row["price"] = float(row["price"])
        row["quantity"] = int(row["quantity"])
        products.append(row)

# b) Print each row in a clean format
print("\n--- Product List ---")
for p in products:
    print(f"ID: {p['product_id']}, Name: {p['product_name']}, "
          f"Category: {p['category']}, Price: {p['price']}, "
          f"Quantity: {p['quantity']}")

# c) Total number of rows
print("\nTotal number of rows:", len(products))

# d) Total number of products priced above 500
above_500 = sum(1 for p in products if p["price"] > 500)
print("Products priced above 500:", above_500)

# e) Average price of all products
avg_price = sum(p["price"] for p in products) / len(products)
print("Average price of all products:", avg_price)

# f) Products belonging to a specific category (user input)
category = input("\nEnter category: ").strip()

print(f"\nProducts in category '{category}':")
found = False
for p in products:
    if p["category"].lower() == category.lower():
        print(f"- {p['product_name']} (Price: {p['price']}, Qty: {p['quantity']})")
        found = True

if not found:
    print("No products found in this category.")

# g) Total quantity of all items in stock
total_quantity = sum(p["quantity"] for p in products)
print("\nTotal quantity of all items in stock:", total_quantity)