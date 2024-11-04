class Payment:
    payment_count = 0

    def __init__(self, payment_id, order_id, amount, payment_status="pending", payment_method=""):
        self.payment_id = payment_id
        self.order_id = order_id
        self.amount = amount
        self.payment_status = payment_status
        self.payment_method = payment_method
        Payment.payment_count += 1

    def process_payment(self):
        self.payment_status = "completed"
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

    def choose_payment_method(self):
        print("\nChoose your Mode of Payment:")
        print("1: Cash on Delivery")
        print("2: GCash")
        print("3: ATM")
        choice = input("Chosen MOP: ").strip()

        if choice == '1':
            self.payment_method = "Cash on Delivery"
            print("MOP: Cash on Delivery")
        elif choice == '2':
            self.payment_method = "GCash"
            print("MOP: GCash")
            input("GCash Account Name: ")
            input("GCash Account Number: ")
        elif choice == '3':
            self.payment_method = "ATM"
            print("MOP: ATM")
            input("ATM Account Number: ")
            input("ATM Expiration Date (Month/Year): ")
        else:
            print("Invalid choice. Defaulting to Cash on Delivery.")
            self.payment_method = "Cash on Delivery"
        
        print(f"\nYou've successfully chosen your mode of payment, {self.payment_method}. Forwarding you to your order details now...")