import json

class Order:
    order_count = 0

    def __init__(self, order_id, customer_id, order_details, payment_mode, shipping_address, shipping_status='Processing'):
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_details = order_details  # Make sure this gets populated correctly
        self.payment_mode = payment_mode
        self.shipping_address = shipping_address
        self.shipping_status = shipping_status
        Order.order_count += 1

    def add_order_item(self, item):
        self.order_details.append(item)  # Add item to the order
        print(f"Item {item} added to order.")

    def save_order(self):
        order_data = {
            "order_id": self.order_id, 
            "customer_id": self.customer_id, 
            "payment_mode": self.payment_mode, 
            "shipping_address": self.shipping_address, 
            "shipping_status": self.shipping_status, 
            "order_details": self.order_details  # Ensure details are included
        }

        # Convert the order data to a JSON string with double quotes
        order_json = json.dumps(order_data, separators=(',', ':'))  # This formats with proper JSON style

        # Write the formatted JSON string to orders.txt
        with open("orders.txt", "a") as file:
            file.write(f"{order_json}\n")  # Append the JSON-formatted order to the file
        print("Order saved to orders.txt.")

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
