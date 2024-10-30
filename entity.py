from datetime import datetime

class Entity:
    entity_count = 0

    def __init__(self, id, status):
        self.id = id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.status = status
        Entity.entity_count += 1

    def save(self):
        # Logic to save the entity
        self.updated_at = datetime.now()
        print(f"Entity {self.id} saved.")

    def delete(self):
        # Logic to delete the entity
        Entity.entity_count -= 1
        print(f"Entity {self.id} deleted.")

    @classmethod
    def get_entity_count(cls):
        return cls.entity_count

    @staticmethod
    def log_entity_action(action):
        print(f"Entity action logged: {action}")
