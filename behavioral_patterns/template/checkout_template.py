""" Template design pattern
Define the skeleton of an algorithm in a base class
and let subclasses fill in the steps.

The base controls the flow; subclasses customize behavior
"""

""" Checkout / Payment processing

1. Validate order
2. Calculate totals
3. Apply discounts
4. Charge the customer
5. Record the transaction
6. Send a receipt
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

class PaymentError(Exception):
    pass

@dataclass
class Order:
    id: str
    items: list[tuple[str, int, float]]
    user_email: str
    total: float = 0.0
    meta: dict = field(default_factory=dict)

class PaymentProcessor(ABC):
    """ Template: defines the algorithm skeleton
    Subclasses customize steps
    """

    def checkout(self, order: Order) -> dict:
        """ Template method: Do not override in subclasses.
        """
        self._log(f"Start checkout for order {order.id}")
        self.validate(order)
        self.compute_total(order)
        self.apply_discounts(order) # optional override
        if self.should_abort(order): # oprtional override
            raise PaymentError("Aborted")
        txn_id = self.charge(order) # abstract (must override)
        self.record(order, txn_id) 
        self.send_receipt(order, txn_id) # can be overriden
        self._log(f"Checkout finished: {txn_id}")

        return {
            "order_id": order.id,
                "txn_id": txn_id,
                "total": order.total
                }
    def validate(self, order: Order):
        if not order.items:
            raise PaymentError("Empty cart.")
        for name, qty, price in order.items:
            if qty <= 0 or price < 0:
                raise PaymentError(f"Invalid line item: {name}")
    
    def compute_total(self, order: Order):
        order.total = sum(q * p for _, q, p in order.items)

    # hooks (optional to override)
    def apply_discounts(self, order: Order):
        """ Optional: subclasses may apply promotions, coupons, etc."""
        coupon = order.meta.get("coupon")
        if coupon == "WELCOME":
            order.total *= 0.9

    def should_abort(self, order: Order) -> bool:
        """ Optional: fraud checks / rate-limits
        """
        return False
    
    @abstractmethod
    def charge(self, order: Order) -> str:
        """ Provider-specific charging: returns a transaction id"""
        pass

    # default implementations (subclasses may override)
    def record(self, order: Order, txn_id: str):
        # pretend we write to a database/audit log
        self._log(f"Recorded {order.id} with txn {txn_id}, total={order.total:.2f}")

    def send_receipt(self, order: Order, txn_id: str):
        # pretend we send email
        self._log(f"Emailed receipt to {order.user_email} txn {txn_id}")

    def _log(self, msg: str):
        print(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}")

    
# Concrete Processors
class StripeProcessor(PaymentProcessor):
    def charge(self, order: Order) -> str:
        # pretend to call Stripe API
        if order.total > 10000:
            raise PaymentError("Stripe limit exceeded for single charge.")
        return f"stripe_{order.id}"
    
class PayPalProcessor(PaymentProcessor):
    def apply_discounts(self, order: Order):
        return super().apply_discounts(order)
        if order.total >= 50:
            order.total -= 5

    def should_abort(self, order: Order) -> bool:
        # simple fraud flag based on metadata
        return order.meta.get("flagged", False)
    

    def charge(self, order: Order) -> str:
        # pretend to call PayPal API
        return f"paypal_{order.id}"
    

# Test
if __name__ == "__main__":
    order = Order(
        id="A1230",
        items=[("Tshirt", 2, 19.99), ("Tasse", 1, 9.99)],
        user_email="max_mustermann@email.de",
        meta={"coupon": "WELCOME"}
    )

    print("---STRIPE---")
    stripe = StripeProcessor()
    result1 = stripe.checkout(order)
    print(result1)

    print("---PAYPAL---")
    order2 = Order(
        id="B456",
        items=[("Hoodie", 1, 59.99)],
        user_email="bob@example.com",
        meta={}  # no coupon; no flags
    )

    paypal = PayPalProcessor()
    result2 = paypal.checkout(order2)
    print(result2)



# checkout() is the template method: it fixes the flow.
# Subclasses must implement charge() and may override hooks (apply_discounts, should_abort, send_receipt).
# The algorithm’s invariants (validate → compute → charge → record → receipt) stay intact.

# When to use

# You have a stable algorithm with varying steps per provider/format/workflow (payments, file importers, exporters, report pipelines).
# You want to prevent flow drift (nobody can “forget” validation or logging) while still allowing customization.
# Pros / Cons

# Pros

# Enforces correct order of steps.
# Centralizes logging/metrics/transactions.
# Clear extension points via hooks.

# Cons

# Uses inheritance; can become rigid if variations multiply.
# Too many hooks = harder to reason about.
# Alternative: If only one step varies, consider Strategy (compose a ChargeStrategy instead of subclassing). 
# Combine both when useful.