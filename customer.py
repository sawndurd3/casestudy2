from user import User

class Customer(User):
    customer_count = 0

    def __init__(self, username, email, password, user_id, user_role, cart=None, order_history=None, shipping_address='', billing_address='', phone='', email_notifications=False):
        super().__init__(username, email, password, user_id, user_role)
        self.cart = cart if cart is not None else []
        self.order_history = order_history if order_history is not None else []
        self.shipping_address = shipping_address
        self.billing_address = billing_address
        self.phone = phone
        self.email_notifications = email_notifications
        Customer.customer_count += 1

    def login(self):
        print(f"{self.username} logged in.")

    def logout(self):
        print(f"{self.username} logged out.")

    def reset_password(self):
        print(f"Password for {self.username} has been reset.")

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

    @classmethod
    def create_customer(cls, username, email, password, user_id, user_role):
        return cls(username, email, password, user_id, user_role)

    @staticmethod
    def get_customer_count():
        return Customer.customer_count
