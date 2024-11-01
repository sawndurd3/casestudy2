from entity import Entity

class Order(Entity):
    order_count = 0

    def __init__(self, order_id, customer_id, order_details, shipping_status, tracking_number):
        super().__init__(order_id, 'pending')
        self.customer_id = customer_id
        self.order_details = order_details
        self.shipping_status = shipping_status
        self.tracking_number = tracking_number
        Order.order_count += 1

    def add_order_item(self, item):
        self.order_details.append(item)
        print(f"Item {item} added to order.")

    def cancel_order(self):
        self.status = 'canceled'
        print("Order canceled.")

    def track_order(self):
        print(f"Tracking order {self.order_id}: {self.tracking_number}")

    @classmethod
    def get_total_orders(cls):
        return cls.order_count

    @staticmethod
    def order_summary(order):
        return {
            "order_id": order.order_id,
            "status": order.status,
            "customer_id": order.customer_id,
            "shipping_status": order.shipping_status,
            "tracking_number": order.tracking_number
        }
