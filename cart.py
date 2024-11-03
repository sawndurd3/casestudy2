class Cart:
    cart_count = 0

    def __init__(self, cart_id, customer_id, items, total_amount):
        self.cart_id = cart_id
        self.customer_id = customer_id
        self.items = items  # List of tuples (product_name, quantity)
        self.total_amount = total_amount
        Cart.cart_count += 1

    def add_to_cart(self, customer_id, product_name, quantity):
        self.items.append((product_name, quantity))
        self.save_cart_to_file(customer_id)

    def save_cart_to_file(self, customer_id):
        with open("cart.txt", "a") as cart_file:
            cart_file.write(f"Customer ID: {customer_id}\n")
            cart_file.write("Products added to Cart:\n")
            for item_name, quantity in self.items:
                cart_file.write(f"{item_name}: {quantity}\n")
            cart_file.write("\n")

    def view_cart(self):
        return self.items

    @classmethod
    def get_total_cart_count(cls):
        return cls.cart_count

    @staticmethod
    def calculate_cart_value(cart):
        return sum(item['price'] for item in cart.items)
