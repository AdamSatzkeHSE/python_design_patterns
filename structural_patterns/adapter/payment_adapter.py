# Target interface -> What the client expects
class PaymentProcessor:
    def pay(self, amount: float):
        raise NotImplementedError

# The adaptee (existing incompatible system)
class OldPaymentSystem:
    def make_payment(self, money: float):
        print(f"Payment of ${money} done using Old system.")

# Paypal payment fits the expected interface, we can directly integrate it with the new code using inheritance.
class PayPalPayment(PaymentProcessor):
    def pay(self, amount: float):
        print(f"Payment of ${amount} using Paypal.")

# The adapter
class PaymentAdapter(PaymentProcessor):
    def __init__(self, old_system: OldPaymentSystem):
        self.old_system = old_system

    def pay(self, amount: float):
        # Adapt the interface
        self.old_system.make_payment(amount)

# Client Code
old_system = OldPaymentSystem()
adapter = PaymentAdapter(old_system)

adapter.pay(100)

# The client expects a pay() method, but the old system only has make_payment()
# The adapter translates the call

# Advantages:
# - Reuses existing code without modifying it
# - Helps integrate third party or legacy systems

# Disadvantages:
# - Can add extra layers of complexity
# - If overused, code becomes harder to mantain.

# Common questions:
# Why not just call make_payment() directly?
# Because the client code doesnt want to depend on the OldPaymentSystem interface
# Imagine if you have many payment systems: PayPal, Sparkasse, Klarna
# Your app expects a unified interface, f.e. PaymentProcessor.pay(amount)
# Without it, the application has to know about the single method name of each payment interface.
# The adapter hides the differences and gives you a standard interface.

def checkout(processor: PaymentProcessor, amount: float):
    print("checking out...")
    processor.pay()

paypal = PayPalPayment()
old_system_adapter = PaymentAdapter(OldPaymentSystem())
