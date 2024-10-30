from entity import Entity

class Product(Entity):
    product_count = 0

    def __init__(self, product_id, name, price, stock_quantity, category):
        super().__init__(product_id, 'available')
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity
        self.category = category
        Product.product_count += 1

    def update_stock(self, quantity):
        self.stock_quantity += quantity
        print(f"Stock updated to {self.stock_quantity}.")

    def get_product_info(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock_quantity": self.stock_quantity,
            "category": self.category
        }

    def apply_discount(self, percentage):
        self.price *= (1 - percentage / 100)
        print(f"Discount applied. New price is {self.price}.")

    @classmethod
    def get_total_products(cls):
        return cls.product_count

    @staticmethod
    def track_inventory():
        print("Inventory tracked.")
