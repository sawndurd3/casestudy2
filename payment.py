class Payment:
    payment_count = 0

    def __init__(self, payment_id, order_id, amount, payment_status, payment_method):
        self.payment_id = payment_id
        self.order_id = order_id
        self.amount = amount
        self.payment_status = payment_status
        self.payment_method = payment_method
        Payment.payment_count += 1

    def process_payment(self):
        print(f"Processing payment of {self.amount} for order {self.order_id}.")

    def refund(self):
        self.payment_status = 'refunded'
        print(f"Refund processed for payment {self.payment_id}.")

    def verify_payment(self):
        print(f"Payment {self.payment_id} verified.")

    @classmethod
    def get_total_payments(cls):
        return cls.payment_count

    @staticmethod
    def track_payment_status(payment):
        print(f"Payment status for {payment.payment_id}: {payment.payment_status}")
