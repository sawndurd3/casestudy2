class Cart:
    cart_count = 0

    def __init__(self, cart_id, customer_id, items, total_amount):
        self.cart_id = cart_id
        self.customer_id = customer_id
        self.items = items  # List of dictionaries with keys: product_name, quantity, price
        self.total_amount = total_amount
        Cart.cart_count += 1

    def add_to_cart(self, customer_id, product_name, quantity, price):
        # Add item to the in-memory items list
        self.items.append({"product_name": product_name, "quantity": quantity, "price": price})
        
        # Append only the new item to the file
        self.append_item_to_file(customer_id, product_name, quantity, price)

    def append_item_to_file(self, customer_id, product_name, quantity, price):
        try:
            with open("cart.txt", "r") as cart_file:
                lines = cart_file.readlines()
        except FileNotFoundError:
            lines = []

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            print("Error: Quantity and price must be numeric values.")
            return

        updated_lines = []
        customer_found = False
        in_customer_section = False
        customer_total = 0
        updated_customer_section = False

        for line in lines:
            if line.strip() == f"Customer ID: {customer_id}":
                customer_found = True
                in_customer_section = True
                updated_lines.append(line)
                continue

            if in_customer_section and line.strip() == "Products added to Cart:":
                updated_lines.append(line)
                line_total = quantity * price
                updated_lines.append(f"{product_name}: {quantity}, Price: {price}  ---({line_total})\n")
                customer_total += line_total
                continue

            if in_customer_section and line.startswith("Total:"):
                existing_total = float(line.split(": ")[1].replace(",", ""))
                customer_total += existing_total
                in_customer_section = False  # End processing this customer
                updated_customer_section = True
                updated_lines.append(f"Total: {customer_total:,.2f}\n")
                continue

            if in_customer_section and line.startswith("Customer ID:"):
                in_customer_section = False  # Ensure we stop processing if a new customer section starts

            updated_lines.append(line)

        if customer_found and not updated_customer_section:
            # Append the total if it wasn't added during the loop
            updated_lines.append(f"Total: {customer_total:,.2f}\n")

        if not customer_found:
            updated_lines.append(f"Customer ID: {customer_id}\n")
            updated_lines.append("Products added to Cart:\n")
            line_total = quantity * price
            updated_lines.append(f"{product_name}: {quantity}, Price: {price}  ---({line_total})\n")
            updated_lines.append(f"Total: {line_total:,.2f}\n")

        with open("cart.txt", "w") as cart_file:
            cart_file.writelines(updated_lines)

    def remove_item(self, item_name):
        # Remove the item from the in-memory list
        self.items = [item for item in self.items if item['product_name'] != item_name]
        print(f"Item {item_name} removed from cart.")

        # Now update the cart.txt file to reflect the change
        self.update_cart_file()

    def update_cart_file(self):
        # Rebuild the cart file with the updated list of items
        try:
            with open("cart.txt", "r") as cart_file:
                lines = cart_file.readlines()
        except FileNotFoundError:
            lines = []

        updated_lines = []
        customer_section_found = False
        in_customer_section = False
        customer_total = 0
        customer_id_found = False  # Flag to track customer section

        for line in lines:
            if line.strip() == f"Customer ID: {self.customer_id}":
                customer_section_found = True
                in_customer_section = True
                updated_lines.append(line)
                continue

            if in_customer_section and line.strip() == "Products added to Cart:":
                updated_lines.append(line)
                # Only include items that are still in the cart
                for item in self.items:
                    line_total = item["quantity"] * item["price"]
                    updated_lines.append(f"{item['product_name']}: {item['quantity']}, Price: {item['price']}  ---({line_total})\n")
                    customer_total += line_total
                continue

            if in_customer_section and line.startswith("Total:"):
                # Remove the old total line and add the new total
                continue  # Skip old total line, it will be added later

            if not in_customer_section:
                updated_lines.append(line)

        # Add the total only once
        if customer_section_found:
            updated_lines.append(f"Total: {customer_total:,.2f}\n")
        else:
            print("...")

        # Write the updated lines back to the file
        with open("cart.txt", "w") as cart_file:
            cart_file.writelines(updated_lines)

    def view_cart(self):
        return self.items

    @classmethod
    def get_total_cart_count(cls):
        return cls.cart_count

    @staticmethod
    def calculate_cart_value(cart):
        return sum(item['price'] * item['quantity'] for item in cart.items)
