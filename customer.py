import json
from user import User
from system_logger import SystemLogger

class Customer(User):
    customer_count = 0
    _file_not_found_logged = False  # Class variable to track if the error has been logged

    def __init__(self, username, email, password, user_role, customer_id, shipping_address='', phone='', cart=None, order_history=None):
        super().__init__(username, email, password, user_role)
        self.customer_id = customer_id
        self.shipping_address = shipping_address
        self.phone = phone
        self.cart = cart if cart else []
        self.order_history = order_history if order_history else []
        Customer.customer_count += 1

    def login(self):
        SystemLogger.log_info(f"Customer {self.username} logged in.")
        return True

    def logout(self):
        SystemLogger.log_info(f"Customer {self.username} logged out.")
        
    def add_to_cart(self, item):
        self.cart.append(item)
        print(f"Item {item} added to cart.")

    def place_order(self):
        self.order_history.append(self.cart)
        print("Order placed.")

    def view_order_history(self):
        print("Viewing order history:", self.order_history)

    def update_account(self):
        print("Account updated.")

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
