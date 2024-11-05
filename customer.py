import json
from datetime import datetime  # Import the datetime class directly
from user import User
from system_logger import SystemLogger
from cart import Cart
from order import Order
import os

class Customer(User):
    customer_count = 0
    _file_not_found_logged = False  # Class variable to track if the error has been logged

    def __init__(self, username, email, password, user_role, customer_id, shipping_address='', phone=''):
        super().__init__(username, email, password, user_role)
        self.customer_id = customer_id
        self.shipping_address = shipping_address
        self.phone = phone
        self.cart = Cart(cart_id=f"{customer_id}_cart", customer_id=customer_id, items=[], total_amount=0)
        self.order_history = []

    def place_order(self, payment_mode="Credit Card"):
        # Create an order and add to order history
        order = Order(
            order_id=f"O{int(datetime.now().timestamp())}",
            customer_id=self.customer_id,
            order_details=self.cart.items,
            payment_mode=payment_mode,
            shipping_address=self.shipping_address
        )
        self.order_history.append(order)
        
        # Save the order to file
        self.save_order_to_file(order)
        
        # Clear cart after placing order
        self.cart.items.clear()
        self.cart.total_amount = 0
        print("Order placed successfully and saved to order history.")


    def save_order_to_file(self, order):
        # Check if orders.txt exists; if not, create it
        if not os.path.exists("orders.txt"):
            with open("orders.txt", "w") as file:
                file.write("")  # Creates the file if it does not exist

        # Append order details to orders.txt
        order_summary = Order.order_summary(order)
        with open("orders.txt", "a") as file:
            file.write(json.dumps(order_summary) + "\n")

    def view_order_history(self):
        try:
            with open("orders.txt", "r") as file:
                print(f"Reading order history for customer {self.customer_id}")  # Debug line
                orders = [json.loads(line) for line in file.readlines()]
                for order in orders:
                    if order["customer_id"] == self.customer_id:
                        print(f"Order ID: {order['order_id']}")
                        
                        # Assuming order_details is a list of items where each item has a 'product_name'
                        product_names = [item['product_name'] for item in order['order_details']]
                        print(f"Products: {', '.join(product_names)}")  # Join the product names with a comma
                        
                        print(f"Payment Mode: {order['payment_mode']}")
                        print(f"Shipping Address: {order['shipping_address']}")
                        print(f"Status: {order['shipping_status']}\n")
        except FileNotFoundError:
            print("No order history available yet.")

    def add_to_cart(self, product_name, quantity):
        self.cart.add_to_cart(self.customer_id, product_name, quantity)

    def login(self):
        SystemLogger.log_info(f"Customer {self.username} logged in.")
        return True

    def logout(self):
        SystemLogger.log_info(f"Customer {self.username} logged out.")
        
    def add_to_cart(self, item):
        self.cart.append(item)
        print(f"Item {item} added to cart.")

    def update_account(self):
        SystemLogger.log_info(f"Customer {self.username} account updated.")

    def reset_password(self):
        new_password = input(f"Enter new password for {self.username}: ")
        self._User__password = new_password
        print(f"Password for {self.username} has been reset.")
        SystemLogger.log_info(f"Customer {self.username}'s password reset.")

        self.save_customer_data(self)

    @classmethod
    def save_customer_data(cls, customer):
        """Saves customer data to JSON file."""
        customer_data = cls.load_customer_data()
        customer_data[str(customer.customer_id)] = {
            "username": customer.username,
            "email": customer._email,
            "password": customer._User__password,
            "user_role": "customer",
            "shipping_address": customer.shipping_address,
            "phone": customer.phone
        }
        with open("customer_data.json", "w") as file:
            json.dump(customer_data, file, indent=4)
            
    @classmethod
    def load_customer_data(cls):
        try:
            with open("customer_data.json", "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            if not cls._file_not_found_logged:
                SystemLogger.log_error("Customer data file not found, writing the file right now...")
                cls._file_not_found_logged = True  # Set to True after the error is logged
            return {}
        
    @classmethod
    def authenticate_customer(cls, username, password):
        """Authenticates customer credentials against stored data."""
        customer_data = cls.load_customer_data()
        for customer_id, customer_info in customer_data.items():
            if customer_info["username"] == username and customer_info["password"] == password:
                return Customer(
                    username=customer_info["username"],
                    email=customer_info["email"],
                    password=customer_info["password"],
                    user_role=customer_info["user_role"],
                    customer_id=customer_id,
                    shipping_address=customer_info["shipping_address"],
                    phone=customer_info["phone"]
                )
        SystemLogger.log_error("Customer login failed.")
        return None

    @classmethod
    def create_new_customer(cls, username, email, password, shipping_address, phone):
        """Creates a new customer and saves their data."""
        customer_id = f"{len(cls.load_customer_data()) + 1:04d}"  # Generate ID starting from 0001
        customer = cls(username, email, password, "customer", customer_id, shipping_address, phone)
        cls.save_customer_data(customer)
        return customer

    @staticmethod
    def get_customer_count():
        return Customer.customer_count