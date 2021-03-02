import sqlite3

#creates entirity of database
#this has to run when application starts

conn = sqlite3.connect("ecommerce.sqlite")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY, email TEXT, address TEXT, city TEXT, state TEXT, zip TEXT)")

cur.execute("CREATE TABLE IF NOT EXISTS products (product_id TEXT PRIMARY KEY, quantity INTEGER, wholesale_cost REAL, sale_price REAL, supplier_id TEXT)")

cur.execute("CREATE TABLE IF NOT EXSISTS order_line_items (order_id INTEGER, product_id TEXT, quantity INTEGER, FOREIGN KEY(order_id) REFERENCES orders(order_id) , FOREIGN KEY(product_id) REFERENCES products(product_id))")
#TODO -- create order_line_items table
conn.close()
