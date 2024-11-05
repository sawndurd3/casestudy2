class Order:
    order_count = 0

    def __init__(self, order_id, customer_id, order_details, payment_mode, shipping_address, shipping_status='Processing'):
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_details = order_details
        self.payment_mode = payment_mode
        self.shipping_address = shipping_address
        self.shipping_status = shipping_status
        Order.order_count += 1

    def add_order_item(self, item):
        self.order_details.append(item)
        print(f"Item {item} added to order.")

    def cancel_order(self):
        self.shipping_status = 'Canceled'
        print("Order canceled.")

    def track_order(self):
        print(f"Tracking order {self.order_id}: {self.shipping_status}")

    @classmethod
    def get_total_orders(cls):
        return cls.order_count

    @staticmethod
    def order_summary(order):
        return {
            "order_id": order.order_id,
            "customer_id": order.customer_id,
            "payment_mode": order.payment_mode,
            "shipping_address": order.shipping_address,
            "shipping_status": order.shipping_status,
            "order_details": order.order_details
        }
