from admin import Admin
from customer import Customer
from system_logger import SystemLogger
import time

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
            print("WELCOME TO EEC STORE!")
            return  # Exit the function if login is successful
        else:
            attempt_count += 1
            print("Invalid credentials.")

            # After the first failed attempt, ask if they want to reset the password
            if attempt_count == 1:
                reset_prompt = input("Would you like to reset your password? (yes/no): ").strip().lower()
                if reset_prompt == "yes":
                    customer_data = Customer.load_customer_data()
                    # Check if user exists in customer data
                    for customer_id, info in customer_data.items():
                        if info["username"] == username:
                            # Create a Customer instance for password reset
                            customer_instance = Customer(
                                username=info["username"],
                                email=info["email"],
                                password=info["password"],
                                user_role=info["user_role"],
                                customer_id=customer_id,
                                shipping_address=info["shipping_address"],
                                phone=info["phone"]
                            )
                            # Reset password and save data
                            customer_instance.reset_password()
                            Customer.save_customer_data(customer_instance)
                            print("Password reset successfully. Please log in with the new password.")
                            
                            # Automatically retry login after password reset
                            return customer_login()

                    print("User not found.")
                    return

    # If all attempts are exhausted, apply a timeout
    print(f"Too many failed attempts. Please wait {timeout} seconds before trying again.")
    time.sleep(timeout)
    print("You may now try logging in again.")

    # After timeout, allow a new login attempt cycle
    customer_login()  # Restart the login process after timeout

def admin_login():
    username = input("Enter username: ")
    attempt_count = 0
    timeout = 10  # 10-second timeout after multiple failed attempts

    while attempt_count < 3:
        password = input("Enter password: ")
        admin = Admin.authenticate_admin(username, password)

        if admin:
            admin.login()
            print("WELCOME TO EEC STORE!")
            return  # Exit the function if login is successful
        else:
            attempt_count += 1
            print("Invalid credentials.")

            # After the first failed attempt, ask if they want to reset the password
            if attempt_count == 1:
                reset_prompt = input("Would you like to reset your password? (yes/no): ").strip().lower()
                if reset_prompt == "yes":
                    admin_data = Admin.load_admin_data()
                    # Check if user exists in admin data
                    for admin_id, info in admin_data.items():
                        if info["username"] == username:
                            # Create an Admin instance for password reset
                            admin_instance = Admin(
                                username=info["username"],
                                email=info["email"],
                                password=info["password"],
                                user_role=info["user_role"],
                                admin_id=admin_id,
                                department=info.get("department", ""),
                                role_description=info.get("role_description", "")
                            )
                            # Reset password and save data
                            admin_instance.reset_password()
                            # Admin data saving is needed here if implemented (similar to Customer)
                            print("Password reset successfully. Please log in with the new password.")
                            
                            # Automatically retry login after password reset
                            return admin_login()

                    print("User not found.")
                    return

    # If all attempts are exhausted, apply a timeout
    print(f"Too many failed attempts. Please wait {timeout} seconds before trying again.")
    time.sleep(timeout)
    print("You may now try logging in again.")

    # After timeout, allow a new login attempt cycle
    admin_login()  # Restart the login process after timeout

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
