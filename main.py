from admin import Admin
from customer import Customer
from product import Product
from system_logger import SystemLogger
from payment import Payment
from datetime import datetime  # Only this import from datetime module
import time
import re

def customer_menu(customer):
    while True:
        print(f"\nWelcome! CUSTOMER {customer.customer_id}")
        print("1. View Products\n2. View Order History\n3. Cart\n4. Log Out")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            view_products(customer)  # Pass customer to view_products
        elif choice == "2":
            view_order_history(customer)
        elif choice == "3":
            view_cart(customer)
        elif choice == "4":
            customer.logout()
            break
        else:
            print("Invalid choice. Please try again.")

def view_order_history(customer):
    customer.view_order_history()

def view_cart(customer):
    print(f"\nCart for Customer {customer.customer_id}")
    
    # Load the cart items from the file for the specific customer
    cart_items = []
    with open("cart.txt", "r") as file:
        lines = file.readlines()
        
        in_customer_cart = False
        for line in lines:
            if line.strip() == f"Customer ID: {customer.customer_id}":
                in_customer_cart = True
            elif line.startswith("Customer ID:"):
                in_customer_cart = False
            elif in_customer_cart and line.strip():
                if line.startswith("Products added to Cart:") or line.startswith("Total:"):
                    continue

                match = re.match(r"(.+): (\d+), Price: ([\d.]+)  ---\(([\d.]+)\)", line.strip())
                if match:
                    product_name = match.group(1).strip()
                    quantity = int(match.group(2).strip())
                    unit_price = float(match.group(3).strip())
                    total_price = float(match.group(4).strip())
                    cart_items.append({
                        "product": product_name,
                        "quantity": quantity,
                        "unit_price": unit_price,
                        "total_price": total_price
                    })
                else:
                    print(f"Skipping unrecognized line format: '{line.strip()}'")

    if not cart_items:
        print("Your cart is currently empty.")
        return

    print("\nItems in your cart:")
    for item in cart_items:
        print(f"{item['product']} - Quantity: {item['quantity']}, Unit Price: {item['unit_price']}, Total Price: {item['total_price']}")

    while True:
        print("\nWould you like to:")
        print("1. Check out a product")
        print("2. Check out all products")
        print("3. Delete a product")
        print("4. Back")
        
        choice = input("Enter choice: ").strip()
        if choice == "1":
            product_name = input("Enter the product name you want to check out: ").strip()
            for item in cart_items:
                if item["product"].lower() == product_name.lower():
                    checkout_product(customer, item["product"], item["total_price"])
                    break
            else:
                print(f"Product '{product_name}' not found in the cart.")
            break

        elif choice == "2":
            checkout_all_products(customer, cart_items)
            break

        elif choice == "3":
            product_name = input("Enter the product name you want to delete: ").strip()
            delete_product_from_cart(customer.customer_id, product_name)
            break
        
        elif choice == "4":
            return
        else:
            print("Invalid choice. Please try again.")


def delete_product_price_from_cart(customer_id, product_name):
    """Helper function to find and delete a specific product's price from the total."""
    
    with open("cart.txt", "r") as file:
        lines = file.readlines()

    updated_lines = []
    in_customer_cart = False
    product_total = 0
    product_found = False

    for line in lines:
        if line.strip() == f"Customer ID: {customer_id}":
            in_customer_cart = True
            updated_lines.append(line)
            continue

        if in_customer_cart and line.startswith("Customer ID:"):
            in_customer_cart = False
            updated_lines.append(line)
            continue

        if in_customer_cart and product_name in line:
            match = re.search(rf"{re.escape(product_name)}:\s*(\d+),\s*Price:\s*([\d.]+)", line)
            if match:
                quantity = int(match.group(1))
                price = float(match.group(2))
                product_total = quantity * price
                product_found = True
            continue  # Skip this line to delete the product

        if in_customer_cart and line.startswith("Total:"):
            try:
                existing_total = float(line.split(":")[1].replace(",", "").strip())
                new_total = existing_total - product_total if product_found else existing_total
                updated_lines.append(f"Total: {new_total:,.2f}\n")
            except ValueError:
                updated_lines.append(line)
            continue

        updated_lines.append(line)

    with open("cart.txt", "w") as file:
        file.writelines(updated_lines)

    return product_found, product_total

def checkout_product(customer, product_name, amount):
    # Create a payment instance and choose a payment method
    payment = Payment(payment_id=f"P{datetime.now().timestamp()}", order_id=customer.customer_id, amount=amount)
    payment.choose_payment_method()  # This sets the payment_method attribute
    
    # Process payment
    payment.process_payment()

    # Delete the product from the cart and adjust total
    product_found, product_total = delete_product_price_from_cart(customer.customer_id, product_name)
    
    if product_found:
        print(f"The product '{product_name}' has been checked out and removed from your cart.")
    else:
        print(f"Product '{product_name}' bought by Customer: {customer.username}.")

    # Place and save the order to orders.txt
    customer.place_order(payment_mode=payment.payment_method)  # Pass payment_method from Payment object
    print("Order has been placed and saved to order history. View Order History to check order details.")

def checkout_all_products(customer, cart_items):
    # Calculate total amount for all items
    total_amount = sum(item['total_price'] for item in cart_items)
    
    # Create a payment instance and choose a payment method
    payment = Payment(payment_id=f"P{datetime.now().timestamp()}", order_id=customer.customer_id, amount=total_amount)
    payment.choose_payment_method()  # This sets the payment_method attribute

    # Process payment
    payment.process_payment()

    # Place the order and save it to orders.txt
    customer.place_order(payment_mode=payment.payment_method)  # Pass payment_method from Payment object

    with open("cart.txt", "r") as file:
        lines = file.readlines()

    with open("cart.txt", "w") as file:
        in_customer_cart = False
        for line in lines:
            if line.strip() == f"Customer ID: {customer.customer_id}":
                in_customer_cart = True
                continue
            elif line.startswith("Customer ID:"):
                in_customer_cart = False
                file.write(line)
            elif not in_customer_cart:
                file.write(line)

    # Clear the cart file (assuming other logic for clearing the cart is implemented)
    print("All items in your cart have been checked out and removed.")
    print("Order has been placed and saved to order history. View Order History to check order details.")


def delete_product_from_cart(customer_id, product_name):
    """Delete a specific product from the cart in cart.txt for a given customer 
    and adjust the customer's total price accordingly."""
    
    with open("cart.txt", "r") as file:
        lines = file.readlines()
    
    updated_lines = []
    in_customer_cart = False
    product_total = 0
    product_found = False  # Track if the product was found and deleted

    for line in lines:
        # Check if we are in the specified customer's section
        if line.strip() == f"Customer ID: {customer_id}":
            in_customer_cart = True
            updated_lines.append(line)
            continue

        # If we hit another customer ID, we exit the current customer's section
        if in_customer_cart and line.startswith("Customer ID:"):
            in_customer_cart = False
            updated_lines.append(line)
            continue

        # Process product line within the customer's section
        if in_customer_cart and product_name in line:
            # Use regex to parse the quantity and price for the specific product line
            match = re.search(rf"{re.escape(product_name)}:\s*(\d+),\s*Price:\s*([\d.]+)", line)
            if match:
                quantity = int(match.group(1))
                price = float(match.group(2))
                product_total = quantity * price
                product_found = True
            continue  # Skip adding this line as we want to delete this product

        # Adjust the total line if we're in the customer's section
        if in_customer_cart and line.startswith("Total:"):
            try:
                existing_total = float(line.split(":")[1].replace(",", "").strip())
                new_total = existing_total - product_total if product_found else existing_total
                updated_lines.append(f"Total: {new_total:,.2f}\n")
            except ValueError:
                updated_lines.append(line)
            continue

        # Otherwise, keep the line as it is
        updated_lines.append(line)

    # Write back the updated lines to cart.txt
    with open("cart.txt", "w") as file:
        file.writelines(updated_lines)

    # Provide feedback based on whether the product was found or not
    if product_found:
        print(f"The item '{product_name}' is now deleted from the cart.")
    else:
        print(f"Product '{product_name}' not found in the cart for customer {customer_id}.")

def view_products(customer):
    # Step 1: Display Categories
    categories = Product.get_categories()
    print("\nAvailable Categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    print(f"{len(categories) + 1}. Back")
    
    category_choice = input("On what category would you like to shop? ").strip()
    try:
        category_index = int(category_choice) - 1
        if category_index < 0 or category_index >= len(categories):
            print("Returning to main menu.")
            return
        selected_category = categories[category_index]
    except ValueError:
        print("Invalid input. Returning to main menu.")
        return

    # Step 2: Display Products in the Selected Category
    products = Product.get_products_by_category(selected_category)
    if not products:
        print(f"No products available in the {selected_category} category.")
        return

    print(f"\nProducts in {selected_category} category:")
    for i, product in enumerate(products, 1):
        print(f"{i}. {product['Name']} - Price: {product['Price']}")
    print(f"{len(products) + 1}. Back")

    product_choice = input("What product are you interested in? ").strip()
    try:
        product_index = int(product_choice) - 1
        if product_index < 0 or product_index >= len(products):
            print("Returning to category selection.")
            return
        selected_product = products[product_index]
    except ValueError:
        print("Invalid input. Returning to category selection.")
        return

    # Step 3: Display Product Details
    product_details = Product.get_product_details(selected_product["Product ID"])
    if product_details:
        print("\nProduct Details:")
        for key, value in product_details.items():
            print(f"{key}: {value}")
    else:
        print("Error retrieving product details.")
        return

    # Step 4: Prompt for Add to Cart or Checkout
    print("\n1. Add to Cart\n2. Check Out")
    action_choice = input("What would you like to do with this product? ").strip()

    if action_choice == "1":
        # Add to Cart
        try:
            quantity = int(input("How many items would you like to add? ").strip())
            if quantity <= 0:
                print("Quantity must be a positive integer.")
                return

            # Add the product to the cart with the price
            customer.cart.add_to_cart(
                customer_id=customer.customer_id,
                product_name=selected_product["Name"],
                quantity=quantity,
                price=selected_product["Price"]
            )
            print(f"{quantity} units of {selected_product['Name']} added to your cart.")

        except ValueError:
            print("Invalid quantity. Please enter a positive integer.")
        
    elif action_choice == "2":
        # Check Out
        print("Proceeding to checkout...")
        amount = float(selected_product["Price"])  # Assuming only 1 unit for checkout
        checkout_product(customer, selected_product["Name"], amount)

    else:
        print("Invalid choice. Returning to product view.")


def save_cart_to_file(customer):
    """Saves the current cart items to a cart file named cart_<customer_id>.txt."""
    with open(f"cart_{customer.customer_id}.txt", "w") as cart_file:
        cart_file.write(f"Customer ID: {customer.customer_id}\n")
        cart_file.write("Products added to Cart:\n")
        
        for item in customer.cart:
            cart_file.write(f"{item['name']}: {item['quantity']}\n")

        cart_file.write("\n\n")


def customer_signup():
    print("Sign up as a new customer")
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    shipping_address = input("Enter Shipping Address: ")
    phone = input("Enter Phone: ")

    customer = Customer.create_new_customer(username, email, password, shipping_address, phone)
    SystemLogger.log_info(f"Customer {username} signed up successfully.")
    print("Account created successfully!")

    # Prompt the user to log in after signing up
    login_prompt = input("Would you like to log in now? (yes/no): ").strip().lower()
    if login_prompt == "yes":
        customer_login()
    else:
        print("Thank you for signing up! Please log in whenever you're ready.")

def customer_login():
    username = input("Enter username: ")
    attempt_count = 0
    timeout = 10  # 10-second timeout after multiple failed attempts

    while attempt_count < 3:
        password = input("Enter password: ")
        customer = Customer.authenticate_customer(username, password)

        if customer:
            customer.login()
            customer_menu(customer)  # Call customer menu here
            return
        else:
            attempt_count += 1
            print("Invalid credentials.")
            if attempt_count == 1:
                reset_prompt = input("Would you like to reset your password? (yes/no): ").strip().lower()
                if reset_prompt == "yes":
                    customer_data = Customer.load_customer_data()
                    for customer_id, info in customer_data.items():
                        if info["username"] == username:
                            customer_instance = Customer(
                                username=info["username"],
                                email=info["email"],
                                password=info["password"],
                                user_role=info["user_role"],
                                customer_id=customer_id,
                                shipping_address=info["shipping_address"],
                                phone=info["phone"]
                            )
                            customer_instance.reset_password()
                            Customer.save_customer_data(customer_instance)
                            print("Password reset successfully. Please log in with the new password.")
                            return customer_login()
                    print("User not found.")
                    return

    print(f"Too many failed attempts. Please wait {timeout} seconds before trying again.")
    time.sleep(timeout)
    print("You may now try logging in again.")
    customer_login()

def admin_menu(admin):
    while True:
        print("\nWelcome! ADMIN", admin.admin_id)
        print("1. Add Products\n2. Remove Products\n3. Update Stock\n4. Log Out")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_product(admin)
        elif choice == "2":
            admin.remove_product()
        elif choice == "3":
            admin.update_stock()
        elif choice == "4":
            admin.logout()
            break
        else:
            print("Invalid choice. Please try again.")

def add_product(admin):
    print("ADD PRODUCT")
    product_id = input("Product ID: ")
    name = input("Name: ")
    price = float(input("Price: "))
    stock_quantity = int(input("Stock Quantity: "))
    category = input("Category: ")
    description = input("Description: ")
    brand = input("Brand: ")
    color = input("Color: ")
    size = input("Size: ")
    sku = input("SKU: ")
    discount = float(input("Discount: "))
    rating = float(input("Rating (0-5): "))
    review = input("Review: ")
    
    admin.add_product(product_id, name, price, stock_quantity, category, description, brand, color, size, sku, discount, rating, review)
    print("\nProduct added successfully!\n")

def update_stock(admin):
    print("UPDATE STOCK")
    product_id = input("Enter Product ID to update stock: ")
    new_stock_quantity = int(input("Enter new stock quantity: "))

    # Read all products from inventory.txt to find the specified product
    with open("inventory.txt", "r") as file:
        products = file.read().strip().split("\n\n")

    updated = False
    updated_products = []

    for entry in products:
        lines = entry.split("\n")
        
        # Extract product details
        current_product_id = lines[0].split(": ")[1].strip()
        if current_product_id == product_id:
            # Extract other details
            name = lines[1].split(": ")[1].strip()
            price = float(lines[2].split(": ")[1].strip())
            stock_quantity = int(lines[3].split(": ")[1].strip())
            category = lines[4].split(": ")[1].strip()
            description = lines[5].split(": ")[1].strip()
            brand = lines[6].split(": ")[1].strip()
            color = lines[7].split(": ")[1].strip()
            size = lines[8].split(": ")[1].strip()
            sku = lines[10].split(": ")[1].strip()
            discount = float(lines[11].split(": ")[1].strip())
            rating = float(lines[12].split(": ")[1].strip())
            review = lines[13].split(": ")[1].strip()
            
            # Create a Product instance
            product = Product(product_id, name, price, stock_quantity, category, description, brand, color, size, sku, discount, rating, review)
            
            # Update stock quantity using Product's update_stock method
            product.update_stock(new_stock_quantity)
            updated = True
            
            # Add updated product entry to the list
            updated_products.append(f"Product ID: {product.product_id}\n"
                                    f"Name: {product.name}\n"
                                    f"Price: {product.price}\n"
                                    f"Stock Quantity: {product.stock_quantity}\n"
                                    f"Category: {product.category}\n"
                                    f"Description: {product.description}\n"
                                    f"Brand: {product.brand}\n"
                                    f"Color: {product.color}\n"
                                    f"Size: {product.size}\n"
                                    f"SKU: {product.sku}\n"
                                    f"Discount: {product.discount}\n"
                                    f"Rating: {product.rating}\n"
                                    f"Review: {product.review}\n")
        else:
            # Keep non-matching products as-is
            updated_products.append(entry)

    if updated:
        # Write back all products, with the updated stock, to inventory.txt
        with open("inventory.txt", "w") as file:
            file.write("\n\n".join(updated_products))
        
        print("Stock updated successfully.")
    else:
        print("Product not found.")

def admin_login():
    username = input("Enter username: ")
    attempt_count = 0
    timeout = 10

    while attempt_count < 3:
        password = input("Enter password: ")
        admin = Admin.authenticate_admin(username, password)

        if admin:
            admin.login()
            admin_menu(admin)
            return
        else:
            attempt_count += 1
            print("Invalid credentials.")

            if attempt_count == 1:
                reset_prompt = input("Would you like to reset your password? (yes/no): ").strip().lower()
                if reset_prompt == "yes":
                    admin_data = Admin.load_admin_data()
                    for admin_id, info in admin_data.items():
                        if info["username"] == username:
                            admin_instance = Admin(
                                username=info["username"],
                                email=info["email"],
                                password=info["password"],
                                user_role=info["user_role"],
                                admin_id=admin_id,
                                department=info.get("department", ""),
                                role_description=info.get("role_description", "")
                            )
                            admin_instance.reset_password()
                            return admin_login()

    print(f"Too many failed attempts. Please wait {timeout} seconds before trying again.")
    time.sleep(timeout)
    print("You may now try logging in again.")
    admin_login()

# Main program flow
def main():
    print("WELCOME TO EEC STORE!")
    print("1. customer\n2. admin")
    user_type = input("Enter Online Shopping System as? (customer/admin): ")
    
    if user_type == "1":
        action = input("Do you want to log in or sign up? (login/signup): ")
        if action == "signup":
            customer_signup()
        elif action == "login":
            customer_login()
        else:
            print("Invalid action selected.")
    elif user_type == "2":
        admin_login()
    else:
        print("Invalid selection.")


main()