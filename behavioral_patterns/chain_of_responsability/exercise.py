# You’re building a user registration flow. Each incoming RegistrationRequest must pass several validations:

# EmailFormatValidator – email must contain @ and a dot after it

# PasswordStrengthValidator – password must be at least 8 chars and contain a digit

# UniqueEmailValidator – email must not already exist in a (fake) database

# Use Chain of Responsibility so each validator decides to:

# handle (i.e., pass or fail) and optionally

# stop the chain (if it fails), or

# pass to the next validator.

# Requirements

# Create an abstract Handler with set_next(handler) and handle(request).

# Each validator returns either the same request to pass along or raises ValidationError to stop the chain.

# Compose the chain as: EmailFormat -> PasswordStrength -> UniqueEmail.

# Show how to run the chain and handle success/failure.

from abc import ABC, abstractmethod
from dataclasses import dataclass

class ValidationError(Exception):
    pass

@dataclass
class RegistrationRequest:
    email: str
    password: str

class Handler(ABC):
    def __init__(self):
        self._next = None

    def set_next(self, handler: "Handler") -> "Handler":
        # TODO: link the next handler and return it for chaining
        ...

    @abstractmethod
    def handle(self, request: RegistrationRequest) -> RegistrationRequest:
        # TODO: perform check or delegate to next
        ...

# TODO: Implement EmailFormatValidator(Handler)
# TODO: Implement PasswordStrengthValidator(Handler)
# TODO: Implement UniqueEmailValidator(Handler)

if __name__ == "__main__":
    # Fake DB
    existing_emails = {"taken@example.com"}

    # Build chain: EmailFormat -> PasswordStrength -> UniqueEmail
    email = EmailFormatValidator()
    password = PasswordStrengthValidator()
    unique = UniqueEmailValidator(existing_emails)

    # TODO: wire them with set_next

    # Try a few requests and print results
    cases = [
        RegistrationRequest("user@site.com", "abc12345"),
        RegistrationRequest("bademail", "abc12345"),
        RegistrationRequest("user@site.com", "short"),
        RegistrationRequest("taken@example.com", "Strong123"),
    ]

    # TODO: run each through the chain, catching ValidationError

# Why this is Chain of Responsibility

# Each validator focuses on a single responsibility.

# The request flows sequentially until one handler fails (stopping the chain) or the chain ends.

# You can reorder, insert, or remove validators without touching the others.
