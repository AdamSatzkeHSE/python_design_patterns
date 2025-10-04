""" Real life implementation: 
Checkout service that reads the provider from config/env and supports extra
providers via a plugin/registration decorator
"""

import os
from abc import ABC, abstractmethod
from typing import Callable, Dict, Type

# Domain interface
class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount_cents: int, currency: str, customer_id: str) -> str:
        """ returns a transaction id """
        pass

# Concrete implementations
class StripeProcessor(PaymentProcessor):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("STRIPE_API_KEY", "test_key")

    def charge(self, amount_cents, currency, customer_id):
        # pretend call to stripe SDK here
        tx = f"stripe_{customer_id}_{amount_cents}"
        print(f"[Stripe] {amount_cents / 100:.2f} {currency} for {customer_id} (key={self.api_key[:4]})")
        return tx
    
class PayPalProcessor(PaymentProcessor):
    def __init__(self, client_id: str | None = None):
        self.client_id = client_id or os.getenv("PAYPAL_CLIENT_ID", "test_client")

    def charge(self, amount_cents, currency, customer_id):
        tx = f"paypal_{customer_id}_{amount_cents}"
        print(f"[PayPal] {amount_cents/100:.2f} {currency} for {customer_id} (client={self.client_id[:4]}**)")
        return tx

# Factory with decorator based entry
class PaymentProcessorFactory:
    _registry: Dict[str, Type[PaymentProcessor]] = {}

    @classmethod
    def register(cls, name: str) -> Callable[[Type[PaymentProcessor]], Type[PaymentProcessor]]:
        def decorator(impl: Type[PaymentProcessor]) -> Type[PaymentProcessor]:
            cls._registry[name.lower()] = impl
            return impl
        return decorator
    
    @classmethod
    def create(cls, name: str, **kwargs) -> PaymentProcessor:
        try:
            impl = cls._registry[name.lower()]
        except KeyError as e:
            raise ValueError(f"Unknown provider {name}. Available: {list(cls._registry)}") from e
        return impl
    
if __name__ == "__main__":
    PaymentProcessorFactory.register("stripe")(StripeProcessor)
    PaymentProcessorFactory.register("paypal")(StripeProcessor)

