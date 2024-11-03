class Cart:
    cart_count = 0

    def __init__(self, cart_id, customer_id, items, total_amount):
        self.cart_id = cart_id
        self.customer_id = customer_id
        self.items = items
        self.total_amount = total_amount
        Cart.cart_count += 1

    def add_item(self, item):
        self.items.append(item)
        print(f"Item {item} added to cart.")

    def remove_item(self, item):
        self.items.remove(item)
        print(f"Item {item} removed from cart.")

    def view_cart(self):
        return self.items

    @classmethod
    def get_total_cart_count(cls):
        return cls.cart_count

    @staticmethod
    def calculate_cart_value(cart):
        return sum(item['price'] for item in cart.items)
