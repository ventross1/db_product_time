import mysql.connector
import random
import string
import time

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="products"
    )


def create_vendors(cursor, vendor_count):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("DELETE FROM product;")
    cursor.execute("DELETE FROM vendor;")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    vendors = [(f"Vendor_{i}",) for i in range(1, vendor_count + 1)]
    cursor.executemany("INSERT INTO vendor (name) VALUES (%s);", vendors)

def generate_products(cursor, n):
    cursor.execute("SELECT id FROM vendor;")
    valid_vendor_ids = [row[0] for row in cursor.fetchall()]
    if not valid_vendor_ids:
        raise ValueError("Tabulka vendor je prázdná. Nejprve vložte výrobce.")
    
    products = []
    for _ in range(n):
        name = ''.join(random.choices(string.ascii_letters, k=10))
        price = round(random.uniform(1, 1000), 2)
        vendor_id = random.choice(valid_vendor_ids)
        products.append((name, price, vendor_id))
    return products

def insert_products(cursor, products):
    cursor.executemany("INSERT INTO product (name, price, vendor_id) VALUES (%s, %s, %s);", products)


def select_vendors(cursor):
    cursor.execute(
        """
        SELECT v.name, COUNT(p.id) as product_count
        FROM vendor v
        LEFT JOIN product p ON v.id = p.vendor_id
        GROUP BY v.id
        ORDER BY product_count DESC;
        """
    )
    return cursor.fetchall()

def measure_performance():
    results = []
    db = connect_to_db()
    cursor = db.cursor()
    vendor_counts = [10, 100, 1000]
    product_counts = [100, 1000, 10000, 100000, 1000000]
    for vendor_count in vendor_counts:
        create_vendors(cursor, vendor_count)
        db.commit()
        for product_count in product_counts:
            products = generate_products(cursor, product_count)
            start_time = time.time()
            insert_products(cursor, products)
            db.commit()
            insert_time = time.time() - start_time

            start_time = time.time()
            select_vendors(cursor)
            select_time = time.time() - start_time
            results.append((vendor_count, product_count, insert_time, select_time))
    cursor.close()
    db.close()
    return results

def main():
    try:
        results = measure_performance()
        print("Výsledky měření výkonu:")
        for result in results:
            print(f"Výrobci: {result[0]}, Produkty: {result[1]}, INSERT: {result[2]:.4f}s, SELECT: {result[3]:.4f}s")
    except Exception as e:
        print(f"Chyba: {e}")

if __name__ == "__main__":
    main()