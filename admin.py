# admin.py
import json
from user import User
from system_logger import SystemLogger
from product import Product

class Admin(User):

    def __init__(self, username, email, password, user_role, admin_id, permissions=None, department='', role_description='', last_login=None):
        super().__init__(username, email, password, user_role)
        self.admin_id = admin_id
        self.permissions = permissions if permissions else []
        self.department = department
        self.role_description = role_description
        self.last_login = last_login

    def login(self):
        SystemLogger.log_info(f"Admin {self.username} logged in.")
        return True

    def logout(self):
        SystemLogger.log_info(f"Admin {self.username} logged out.")

    def reset_password(self):
        new_password = input(f"Enter new password for admin {self.username}: ")
        self._User__password = new_password  # Access the private password attribute
        print(f"Password for admin {self.username} has been reset.")
        SystemLogger.log_info(f"Admin {self.username}'s password reset.")
        self.save_admin_data(self)

    def add_product(self, product_id, name, price, stock_quantity, category, description, brand, color, size, sku, discount, rating, review):
        # Create product and write to inventory.txt
        product = Product(product_id, name, price, stock_quantity, category, description, brand, color, size, sku, discount, rating, review)
        with open("inventory.txt", "a") as file:
            file.write(f"Product ID: {product_id}\n"
                       f"Name: {name}\n"
                       f"Price: {price}\n"
                       f"Stock Quantity: {stock_quantity}\n"
                       f"Category: {category}\n"
                       f"Description: {description}\n"
                       f"Brand: {brand}\n"
                       f"Color: {color}\n"
                       f"Size: {size}\n"
                       f"SKU: {sku}\n"
                       f"Discount: {discount}\n"
                       f"Rating: {rating}\n"
                       f"Review: {review}\n\n")
        
        print("Product added successfully to inventory.")
        self.sort_inventory_by_category()

    def sort_inventory_by_category(self):
        # Read all product entries from the file
        with open("inventory.txt", "r") as file:
            contents = file.read().strip()

        # Split the contents by double newline to separate each product entry
        product_entries = contents.split("\n\n")
        
        # Parse each product entry into a dictionary and store them in a list
        products = []
        for entry in product_entries:
            lines = entry.split("\n")
            try:
                product_data = {
                    "Product ID": lines[0].split(": ")[1],
                    "Name": lines[1].split(": ")[1],
                    "Price": float(lines[2].split(": ")[1]),
                    "Stock Quantity": int(lines[3].split(": ")[1]),
                    "Category": lines[4].split(": ")[1],
                    "Description": lines[5].split(": ")[1],
                    "Brand": lines[6].split(": ")[1],
                    "Color": lines[7].split(": ")[1],
                    "Size": lines[8].split(": ")[1],
                    "SKU": lines[9].split(": ")[1],          
                    "Discount": float(lines[10].split(": ")[1]), 
                    "Rating": float(lines[11].split(": ")[1]),     
                    "Review": lines[12].split(": ")[1],          
                }
                products.append(product_data)
            except IndexError:
                print("Error parsing product entry. Please check the file format.")
                continue
            except ValueError as e:
                print(f"Error converting product data: {e}")
                continue

        # Sort the products list by 'Category'
        products = sorted(products, key=lambda x: x["Category"])

        # Write the sorted product entries back to the file in the new format
        with open("inventory.txt", "w") as file:
            for product in products:
                file.write(
                    f"Product ID: {product['Product ID']}\n"
                    f"Name: {product['Name']}\n"
                    f"Price: {product['Price']}\n"
                    f"Stock Quantity: {product['Stock Quantity']}\n"
                    f"Category: {product['Category']}\n"
                    f"Description: {product['Description']}\n"
                    f"Brand: {product['Brand']}\n"
                    f"Color: {product['Color']}\n"
                    f"Size: {product['Size']}\n"
                    f"SKU: {product['SKU']}\n"
                    f"Discount: {product['Discount']}\n"
                    f"Rating: {product['Rating']}\n"
                    f"Review: {product['Review']}\n\n"
                )

    def remove_product(self):
        print("REMOVE PRODUCT")
        product_id = input("Product ID: ")

        # Read all product entries from the file
        with open("inventory.txt", "r") as file:
            contents = file.read().strip()

        # Split the contents by double newline to separate each product entry
        product_entries = contents.split("\n\n")
        
        # Find and remove the product entry with the matching product_id
        updated_entries = []
        product_found = False
        for entry in product_entries:
            if f"Product ID: {product_id}" not in entry:
                updated_entries.append(entry)
            else:
                product_found = True
        
        if product_found:
            # Write the updated list back to the file
            with open("inventory.txt", "w") as file:
                file.write("\n\n".join(updated_entries) + ("\n\n" if updated_entries else ""))
            print(f"Product with ID {product_id} removed successfully.")
        else:
            print(f"No product found with ID {product_id}.")

    def update_stock(self):
        print("UPDATE STOCK")
        product_id = input("Product ID: ")
        try:
            new_stock_quantity = int(input("New Stock Quantity: "))
            # Call Product's update_stock method
            if Product.update_stock(product_id, new_stock_quantity):
                print(f"Stock quantity updated for Product ID {product_id}.")
            else:
                print(f"No product found with ID {product_id}.")
        except ValueError:
            print("Invalid stock quantity. Please enter a valid integer.")
    
    @classmethod
    def load_admin_data(cls):
        try:
            with open("admin_data.json", "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            SystemLogger.log_error("Admin data file not found.")
            return {}

    @classmethod
    def save_admin_data(cls, admin):
        admin_data = cls.load_admin_data()
        admin_data[str(admin.admin_id)] = {
            "username": admin.username,
            "email": admin._email,
            "password": admin._User__password,
            "user_role": "admin",
            "department": admin.department,
            "role_description": admin.role_description
        }
        with open("admin_data.json", "w") as file:
            json.dump(admin_data, file, indent=4)

    @classmethod
    def authenticate_admin(cls, username, password):
        admin_data = cls.load_admin_data()
        for admin_id, admin_info in admin_data.items():
            if admin_info["username"] == username and admin_info["password"] == password:
                return Admin(
                    username=admin_info["username"],
                    email=admin_info["email"],
                    password=admin_info["password"],
                    user_role=admin_info["user_role"],
                    admin_id=admin_id,
                    department=admin_info["department"],
                    role_description=admin_info["role_description"]
                )
        SystemLogger.log_error("Admin login failed.")
        return None
