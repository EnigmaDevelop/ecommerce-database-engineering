import os
import csv
import json
import random
import uuid
from faker import Faker
import psycopg2

# Initialize Faker
fake = Faker()

# Configuration - Extracted directly from your docker-compose.yml
DB_HOST = "localhost"
DB_PORT = 5433  
DB_NAME = "ecommerce_db"
DB_USER = "data_engineer"       
DB_PASSWORD = "de_password123"   

# Data Volume Targets - Downscaled for high-speed local pipeline execution
NUM_USERS = 100_000
NUM_PRODUCTS = 50_000
NUM_ORDERS = 1_000_000

# Constants for Scenario-Driven Data Matching the DBML & Slow Queries
EMAIL_DOMAINS = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']
CATEGORIES = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports']
COLORS = ['Red', 'Blue', 'Black', 'White', 'Green']
SIZES = ['S', 'M', 'L', 'XL', 'XXL']
STATUS_OPTIONS = ['Pending', 'Processing', 'Completed', 'Cancelled', 'Refunded']
TECH_TAGS = ['wireless', 'noise-canceling', 'bluetooth', 'waterproof', 'smart']
GATEWAYS = ['Stripe', 'PayPal', 'Ayden', 'Klarna']

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def generate_users_csv(filename, count):
    print(f"Generating {count} users with strict uniqueness guarantee...")
    generated_emails = set()
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for user_id in range(1, count + 1):
            first_name = fake.first_name()
            last_name = fake.last_name()
            
            while True:
                domain = 'hotmail.com' if random.random() < 0.25 else random.choice(EMAIL_DOMAINS)
                unique_suffix = uuid.uuid4().hex[:5]
                email = f"{first_name.lower()}.{last_name.lower()}_{unique_suffix}@{domain}"
                
                if email not in generated_emails:
                    generated_emails.add(email)
                    break
            
            password_hash = fake.sha256()
            created_at = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([user_id, email, password_hash, first_name, last_name, created_at])
            
    generated_emails.clear()

def generate_products_csv(filename, count):
    print(f"Generating {count} products...")
    product_prices = {}
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for product_id in range(1, count + 1):
            sku = f"SKU-{uuid.uuid4().hex[:8].upper()}-{product_id}"
            category = random.choice(CATEGORIES)
            name = f"{fake.word().capitalize()} {category[:-1] if category.endswith('s') else category}"
            base_price = round(random.uniform(10.0, 15000.0), 2)
            product_prices[product_id] = base_price
            stock_quantity = random.randint(0, 1500)
            created_at = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            
            attributes = {
                "category_group": category,
                "color": random.choice(COLORS),
                "size": random.choice(SIZES),
                "weight_kg": round(random.uniform(0.1, 20.0), 2),
                "manufacturer": fake.company()
            }
            
            if category == 'Electronics':
                if random.random() < 0.4:
                    attributes["tags"] = ["wireless", "noise-canceling", "bluetooth"]
                else:
                    attributes["tags"] = random.sample(TECH_TAGS, k=random.randint(1, 3))
            else:
                attributes["tags"] = [fake.word(), fake.word()]

            writer.writerow([product_id, sku, name, base_price, stock_quantity, created_at, json.dumps(attributes)])
            
    return product_prices

def generate_orders_and_items_csv(orders_filename, items_filename, order_count, num_users, product_prices):
    print(f"Generating {order_count} orders and corresponding order items...")
    num_products = len(product_prices)
    item_id_counter = 1
    
    cached_gateways = GATEWAYS
    cached_statuses = STATUS_OPTIONS
    
    with open(orders_filename, 'w', newline='', encoding='utf-8') as f_ord, \
         open(items_filename, 'w', newline='', encoding='utf-8') as f_itm:
         
        ord_writer = csv.writer(f_ord, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        itm_writer = csv.writer(f_itm, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        
        for order_id in range(1, order_count + 1):
            user_id = random.randint(1, num_users)
            order_status = random.choice(cached_statuses)
            created_at_dt = fake.date_time_between(start_date='-1y', end_date='now')
            created_at = created_at_dt.strftime('%Y-%m-%d %H:%M:%S')
            
            num_items = random.randint(1, 4)
            total_amount = 0.00
            order_items_buffer = []
            
            for _ in range(num_items):
                product_id = random.randint(1, num_products)
                quantity = random.randint(1, 3)
                purchased_price = product_prices.get(product_id, 99.99)
                
                if order_status == 'Cancelled' and random.random() < 0.3:
                    purchased_price = round(random.uniform(2500.0, 6000.0), 2)
                    
                total_amount += float(purchased_price) * quantity
                order_items_buffer.append([item_id_counter, order_id, product_id, quantity, purchased_price])
                item_id_counter += 1
            
            total_amount = round(total_amount, 2)
            
            payment_details = {
                "gateway": random.choice(cached_gateways),
                "transaction_id": f"tx_{uuid.uuid4().hex[:12]}",
                "response_code": "SUCCESS" if order_status != 'Cancelled' else "FAILED_REVERSED",
                "metadata": {"ip_address": fake.ipv4(), "device": random.choice(["desktop", "mobile", "ios"])}
            }
            
            shipping_tracking_history = [
                {"status": "Manifest Created", "timestamp": created_at},
                {"status": "In Transit", "timestamp": fake.date_time_between(start_date=created_at_dt, end_date='now').strftime('%Y-%m-%d %H:%M:%S')}
            ] if order_status == 'Completed' else [{"status": "Failed/Cancelled at Gateway", "timestamp": created_at}]

            ord_writer.writerow([
                order_id, user_id, total_amount, order_status, created_at, 
                json.dumps(payment_details), json.dumps(shipping_tracking_history)
            ])
            
            for item_row in order_items_buffer:
                itm_writer.writerow(item_row)

def bulk_copy_to_db(connection, csv_filename, table_name):
    print(f"Bulk loading {csv_filename} into {table_name} table via Postgres COPY engine...")
    cursor = connection.cursor()
    with open(csv_filename, 'r', encoding='utf-8') as f:
        cursor.copy_expert(f"COPY {table_name} FROM STDIN WITH (FORMAT CSV, DELIMITER ',')", f)
    connection.commit()
    cursor.close()
    print(f"Successfully loaded {table_name}.")

if __name__ == "__main__":
    users_file = "temp_users.csv"
    products_file = "temp_products.csv"
    orders_file = "temp_orders.csv"
    items_file = "temp_order_items.csv"

    try:
        generate_users_csv(users_file, NUM_USERS)
        prod_prices = generate_products_csv(products_file, NUM_PRODUCTS)
        generate_orders_and_items_csv(orders_file, items_file, NUM_ORDERS, NUM_USERS, prod_prices)

        conn = get_db_connection()
        
        bulk_copy_to_db(conn, users_file, "users")
        bulk_copy_to_db(conn, products_file, "products")
        bulk_copy_to_db(conn, orders_file, "orders")
        bulk_copy_to_db(conn, items_file, "order_items")
        
        conn.close()
        print("\n🚀 Day 2 Data Pipeline Executed Successfully at Optimized Volume!")

    except Exception as e:
        print(f"\n❌ Pipeline execution broken: {str(e)}")
        
    finally:
        for f in [users_file, products_file, orders_file, items_file]:
            if os.path.exists(f):
                os.remove(f)
