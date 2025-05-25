import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect or create new database
conn = sqlite3.connect("online_sales_data.db")
cursor = conn.cursor()

# Create new sales table
cursor.execute("""
CREATE TABLE IF NOT EXISTS online_sales (
    id INTEGER PRIMARY KEY,
    product TEXT,
    quantity INTEGER,
    price REAL
)
""")

# Insert new sample data (only if table is empty)
cursor.execute("SELECT COUNT(*) FROM online_sales")
if cursor.fetchone()[0] == 0:
    new_data = [
        ("Laptop", 4, 800),
        ("Mouse", 20, 25),
        ("Keyboard", 10, 40),
        ("Laptop", 2, 800),
        ("Mouse", 15, 25),
        ("Keyboard", 5, 40)
    ]
    cursor.executemany("INSERT INTO online_sales (product, quantity, price) VALUES (?, ?, ?)", new_data)
    conn.commit()

# Query for sales summary
query = """
SELECT 
    product, 
    SUM(quantity) AS total_quantity, 
    SUM(quantity * price) AS revenue
FROM online_sales
GROUP BY product
"""
df = pd.read_sql_query(query, conn)

# Print results
print("=== ONLINE STORE SALES SUMMARY ===")
print(df)

# Plot revenue bar chart
df.plot(kind='bar', x='product', y='revenue', legend=False, color='orange')
plt.title("Online Store Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("online_sales_chart.png")
plt.show()

# Close connection
conn.close()
