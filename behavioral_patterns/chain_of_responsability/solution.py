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
        self._next = handler
        return handler  # allow fluent chaining

    def next(self, request: RegistrationRequest) -> RegistrationRequest:
        if self._next is None:
            return request
        return self._next.handle(request)

    @abstractmethod
    def handle(self, request: RegistrationRequest) -> RegistrationRequest:
        pass


class EmailFormatValidator(Handler):
    def handle(self, request: RegistrationRequest) -> RegistrationRequest:
        email = request.email
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValidationError("Invalid email format.")
        return self.next(request)


class PasswordStrengthValidator(Handler):
    def handle(self, request: RegistrationRequest) -> RegistrationRequest:
        pwd = request.password
        if len(pwd) < 8:
            raise ValidationError("Password must be at least 8 characters.")
        if not any(ch.isdigit() for ch in pwd):
            raise ValidationError("Password must contain at least one digit.")
        return self.next(request)


class UniqueEmailValidator(Handler):
    def __init__(self, existing_emails: set[str]):
        super().__init__()
        self.existing_emails = existing_emails

    def handle(self, request: RegistrationRequest) -> RegistrationRequest:
        if request.email in self.existing_emails:
            raise ValidationError("Email is already registered.")
        # pretend to insert after success (optional)
        # self.existing_emails.add(request.email)
        return self.next(request)


if __name__ == "__main__":
    existing_emails = {"taken@example.com"}

    # Build the chain
    chain = EmailFormatValidator()
    chain.set_next(PasswordStrengthValidator()).set_next(UniqueEmailValidator(existing_emails))

    cases = [
        RegistrationRequest("user@site.com", "abc12345"),          # ✅
        RegistrationRequest("bademail", "abc12345"),               # ❌ email format
        RegistrationRequest("user@site.com", "short"),             # ❌ password length
        RegistrationRequest("taken@example.com", "Strong123"),     # ❌ uniqueness
    ]

    for i, req in enumerate(cases, start=1):
        try:
            chain.handle(req)
            print(f"Case {i}: OK -> {req}")
        except ValidationError as e:
            print(f"Case {i}: FAIL -> {e}")
