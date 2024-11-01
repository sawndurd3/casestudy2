import json
from user import User
from system_logger import SystemLogger

class Admin(User):

    def __init__(self, username, email, password, user_role, admin_id, permissions=None, department='', role_description='', last_login=None):
        super().__init__(username, email, password, user_role)
        self.admin_id = admin_id
        self.permissions = permissions if permissions else []
        self.department = department
        self.role_description = role_description
        self.last_login = last_login

    def login(self):
        SystemLogger.log_info(f"Admin {self.username} logged in.")
        return True

    def logout(self):
        SystemLogger.log_info(f"Admin {self.username} logged out.")

    def reset_password(self):
            new_password = input(f"Enter new password for admin {self.username}: ")
            self._User__password = new_password  # Access the private password attribute
            print(f"Password for admin {self.username} has been reset.")
            SystemLogger.log_info(f"Admin {self.username}'s password reset.")
            
            self.save_admin_data(self)

    def add_product(self):
        print("Product added.")

    def remove_product(self):
        print("Product removed.")

    def manage_users(self):
        print("Managing users.")

    def generate_reports(self):
        print("Generating reports.")

    @classmethod
    def load_admin_data(cls):
        """Loads admin data from JSON file."""
        try:
            with open("admin_data.json", "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            SystemLogger.log_error("Admin data file not found.")
            return {}

    @classmethod
    def save_admin_data(cls, admin):
        """Saves the updated admin data back to the JSON file."""
        admin_data = cls.load_admin_data()
        admin_data[str(admin.admin_id)] = {
            "username": admin.username,
            "email": admin._email,
            "password": admin._User__password,
            "user_role": "admin",
            "department": admin.department,
            "role_description": admin.role_description
        }
        with open("admin_data.json", "w") as file:
            json.dump(admin_data, file, indent=4)

    @classmethod
    def authenticate_admin(cls, username, password):
        """Authenticates admin credentials against stored data."""
        admin_data = cls.load_admin_data()
        for admin_id, admin_info in admin_data.items():
            if admin_info["username"] == username and admin_info["password"] == password:
                return Admin(
                    username=admin_info["username"],
                    email=admin_info["email"],
                    password=admin_info["password"],
                    user_role=admin_info["user_role"],
                    admin_id=admin_id,
                    department=admin_info["department"],
                    role_description=admin_info["role_description"]
                )
        SystemLogger.log_error("Admin login failed.")
        return None