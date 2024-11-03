from admin import Admin
from customer import Customer
from product import Product
from system_logger import SystemLogger
import time

def customer_menu(customer):
    while True:
        print(f"\nWelcome! CUSTOMER {customer.customer_id}")
        print("1. View Products\n2. View Order History\n3. Cart\n4. Log Out")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            view_products()
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
    # Placeholder function to display order history
    print(f"\nOrder History for Customer {customer.customer_id}")
    # You can replace the following with actual logic to retrieve and display order history
    print("No order history available yet.")

def view_cart(customer):
    # Placeholder function to display the cart
    print(f"\nCart for Customer {customer.customer_id}")
    # You can replace the following with actual logic to retrieve and display cart items
    print("Your cart is currently empty.")

def view_products():
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
        print(f"{i}. {product['Name']}")
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
    
    admin.add_product(product_id, name, price, stock_quantity, category)
    print("\nProduct added successfully!\n")

def update_stock(product):
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
            
            # Create a Product instance
            product = Product(product_id, name, price, stock_quantity, category)
            
            # Update stock quantity using Product's update_stock method
            product.update_stock(new_stock_quantity)
            updated = True
            
            # Add updated product entry to the list
            updated_products.append(f"Product ID: {product.product_id}\n"
                                    f"Name: {product.name}\n"
                                    f"Price: {product.price}\n"
                                    f"Stock Quantity: {product.stock_quantity}\n"
                                    f"Category: {product.category}\n")
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

if __name__ == "__main__":
    main()
