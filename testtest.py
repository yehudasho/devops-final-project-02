from pymongo import MongoClient
MONGO_DB_USERNAME = 'root'
MONGO_DB_PASSWORD = 'maor'
MONGO_DB_HOST = 'localhost'
MONGO_DB_PORT = 27017
MONGO_DB_NAME = 'mydb'
client = MongoClient(f"mongodb://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@{MONGO_DB_HOST}:{MONGO_DB_PORT}")
db = client[MONGO_DB_NAME]
customer_data = [
    {"name": "John Doe", "email": "john@example.com", "phone": "1234567890"},
    {"name": "Jane Smith", "email": "jane@example.com", "phone": "9876543210"}
]
product_data = [
    {"id": "1", "name": "Product 1", "provider": "Provider A"},
    {"id": "2", "name": "Product 2", "provider": "Provider B"}
]
db.customers.insert_many(customer_data)
db.products.insert_many(product_data)

print("Data inserted successfully.")