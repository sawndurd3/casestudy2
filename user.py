from abc import ABC, abstractmethod

class User(ABC):
    user_count = 0

    def __init__(self, username, email, password, user_id, user_role):
        self.username = username
        self._email = email
        self.__password = password
        self.user_id = user_id
        self.user_role = user_role
        User.user_count += 1

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def reset_password(self):
        pass

    @classmethod
    def create_user(cls, username, email, password, user_id, user_role):
        return cls(username, email, password, user_id, user_role)

    @staticmethod
    def get_user_count():
        return User.user_count
