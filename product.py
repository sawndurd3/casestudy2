class Product:
    product_count = 0
    def __init__(self, product_id, name, price, stock_quantity, category, description, brand, color, size, sku, discount, rating, review):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity
        self.category = category
        self.description = description
        self.brand = brand
        self.color = color
        self.size = size
        self.sku = sku
        self.discount = discount
        self.rating = rating
        self.review = review
        Product.product_count += 1

    @staticmethod
    def update_stock(product_id, new_stock_quantity):
        # Read all product entries from the file
        with open("inventory.txt", "r") as file:
            contents = file.read().strip()

        # Split the contents by double newline to separate each product entry
        product_entries = contents.split("\n\n")
        
        # Update the stock quantity for the product with the matching product_id
        updated_entries = []
        product_found = False
        for entry in product_entries:
            if f"Product ID: {product_id}" in entry:
                # Parse the entry and replace the stock quantity
                lines = entry.split("\n")
                for i, line in enumerate(lines):
                    if line.startswith("Stock Quantity:"):
                        lines[i] = f"Stock Quantity: {new_stock_quantity}"
                        product_found = True
                        break
                updated_entry = "\n".join(lines)
                updated_entries.append(updated_entry)
            else:
                updated_entries.append(entry)
        
        # Write the updated list back to the file
        with open("inventory.txt", "w") as file:
            file.write("\n\n".join(updated_entries) + ("\n\n" if updated_entries else ""))
        
        return product_found  # Return True if the product was found and updated
    
    @staticmethod
    def get_categories():
        # Retrieve unique categories from inventory.txt
        categories = set()
        with open("inventory.txt", "r") as file:
            contents = file.read().strip()
            product_entries = contents.split("\n\n")
            for entry in product_entries:
                lines = entry.split("\n")
                for line in lines:
                    if line.startswith("Category:"):
                        categories.add(line.split(": ")[1])
                        break
        return sorted(categories)
    
    @staticmethod
    def get_product_details_by_name(product_name):
        """
        Retrieves product details by product name.
        """
        with open("inventory.txt", "r") as file:
            contents = file.read().strip()
            product_entries = contents.split("\n\n")
            for entry in product_entries:
                lines = entry.split("\n")
                product_data = {}
                for line in lines:
                    key, value = line.split(": ", 1)
                    product_data[key.strip()] = value.strip()
                if product_data.get("Name").lower() == product_name.lower():
                    return product_data
        return None
    
    @staticmethod
    def get_products_by_category(category):
        # Retrieve products within a specific category
        products = []
        with open("inventory.txt", "r") as file:
            contents = file.read().strip()
            product_entries = contents.split("\n\n")
            for entry in product_entries:
                lines = entry.split("\n")
                product_data = {}
                for line in lines:
                    key, value = line.split(": ")
                    product_data[key.strip()] = value.strip()
                if product_data.get("Category") == category:
                    products.append(product_data)
        return products

    @staticmethod
    def get_product_details(product_id):
        # Retrieve full details for a specific product by product_id
        with open("inventory.txt", "r") as file:
            contents = file.read().strip()
            product_entries = contents.split("\n\n")
            for entry in product_entries:
                lines = entry.split("\n")
                product_data = {}
                for line in lines:
                    key, value = line.split(": ")
                    product_data[key.strip()] = value.strip()
                if product_data.get("Product ID") == product_id:
                    return product_data
        return None

    def apply_discount(self, percentage):
        self.price *= (1 - percentage / 100)
        print(f"Discount applied. New price is {self.price}.")

    @classmethod
    def get_total_products(cls):
        return cls.product_count

    @staticmethod
    def track_inventory():
        print("Inventory tracked.")
