""" When you need to create one of several realted objects at runtime
based on a configuration file, environment variable. Instead of writing
many if-else blocks, you create an interface that gives you the concrete
implementation back."""

from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount_cents: int, currency: str) -> None:
        pass

class StripeProcessor(PaymentProcessor):
    def charge(self, amount_cents, currency):
        print(f"[Stripe] Charging {amount_cents / 100:.2f} {currency}")

class PayPalProcessor(PaymentProcessor):
    def charge(self, amount_cents, currency):
        print(f"[PayPal] Charging {amount_cents / 100:.2f} {currency}")

class PaymentProcessorFactory:
    _registry = {
        "stripe" : StripeProcessor,
        "paypal" : PayPalProcessor
    }

    @classmethod
    def create(cls, provider: str) -> PaymentProcessor:
        try:
            return cls._registry[provider.lower()]()
        except KeyError:
            raise ValueError(f"Unknown provider: {provider!r}. Options: {list(cls._registry)}")
        
if __name__ == "__main__":
    processor = PaymentProcessorFactory.create("stripe")
    processor.charge(2600, "EUR")

# Why it's good:
# Client code only knows PaymentProcessor
# Adding a provider is just registering a class - no scattered if's