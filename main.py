from customer import Customer
from admin import Admin
from product import Product

# Creating instances of the classes
customer1 = Customer.create_customer("john_doe", "john@example.com", "password123", 1, "customer")
admin1 = Admin.create_admin("admin_user", "admin@example.com", "adminpass", 1, "admin")
product1 = Product(1, "Laptop", 1000.00, 50, "Electronics")

# Using the methods
customer1.login()
customer1.add_to_cart("Laptop")
product1.apply_discount(10)
admin1.login()
