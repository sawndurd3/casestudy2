from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, username, email, password, user_role):
        self.username = username
        self._email = email
        self.__password = password
        self.user_role = user_role

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