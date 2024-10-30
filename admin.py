from user import User

class Admin(User):
    admin_count = 0

    def __init__(self, username, email, password, user_id, user_role, admin_id, permissions, department, role_description, last_login=None):
        super().__init__(username, email, password, user_id, user_role)
        self.admin_id = admin_id
        self.permissions = permissions
        self.department = department
        self.role_description = role_description
        self.last_login = last_login
        Admin.admin_count += 1

    def login(self):
        print(f"Admin {self.username} logged in.")

    def logout(self):
        print(f"Admin {self.username} logged out.")

    def reset_password(self):
        print(f"Password for admin {self.username} has been reset.")

    def add_product(self):
        print("Product added.")

    def remove_product(self):
        print("Product removed.")

    def manage_users(self):
        print("Managing users.")

    def generate_reports(self):
        print("Generating reports.")

    @classmethod
    def create_admin(cls, username, email, password, user_id, user_role):
        return cls(username, email, password, user_id, user_role, 0, [], '', '', None)

    @staticmethod
    def get_admin_count():
        return Admin.admin_count
