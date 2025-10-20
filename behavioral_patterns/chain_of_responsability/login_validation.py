""" We have an API request with some login data (username and password)

You want to process it through a series of checks:
1. Check if the request has all required fields.
2. Check if the user exists in the database.
3. Check if the password is correct.
4. Check if the user account is active.

Each step can:
- handle the request 
- pass it to the next handler if it's valid so far
"""

# Define the base handler
from typing import Optional, Protocol, Any

class Handler(Protocol):
    def set_next(self, nxt: "Handler") -> "Handler":
        pass

    def handle(self, request: dict) -> Any:
        pass

class BaseHandler:
    def __init__(self):
        self._next: Optional[Handler] = None

    def set_next(self, nxt: Handler) -> Handler:
        self._next = nxt
        return nxt
    
    def handle(self, request: dict) -> Any:
        if self._next:
            return self._next.handle(request)
        return {
            "stats": "success", 
            "message": "Request processed successfully"
        }
    
""" Concrete Handlers """
# Check that username and password exist
class FieldValidator(BaseHandler):
    def handle(self, request: dict) -> Any:
        if "username" not in request or "password" not in request:
            return {
                "status": "error",
                "message": "Missing username or password"
            }
        return super().handle(request)
    
# Check if user exists
class UserExistsValidator(BaseHandler):
    def __init__(self, valid_users: dict):
        super().__init__()
        self.valid_users = valid_users

    def handle(self, request: dict) -> Any:
        if request["username"] not in self.valid_users:
            return {
                "status": "error",
                "message": "User does not exist"
            }
        return super().handle(request)

# Check password
class PasswordValidator(BaseHandler):
    def __init__(self, valid_users: dict):
        super().__init__()
        self.valid_users = valid_users

    def handle(self, request: dict) -> Any:
        if self.valid_users[request["username"]] != request["password"]:
            return {
                "status": "error",
                "message": "Invalid password"
            }
        return super().handle(request)
    
# Check if user account is active
class ActiveUserValidator(BaseHandler):
    def __init__(self, active_users: set):
        super().__init__()
        self.active_users = active_users
    
    def handle(self, request: dict) -> Any:
        if request["username"] not in self.active_users:
            return {
                "status": "error",
                "message": "User account inactive"
            }
        return super().handle(request)
    
# Build the chain
users = {
    "alice": "secret123",
    "bob": "password",
    "charlie": "abc123"
}

active_users = {
    "alice", "bob"
}

fields = FieldValidator()
exists = UserExistsValidator(users)
password = PasswordValidator(users)
active = ActiveUserValidator(active_users)
fields.set_next(exists).set_next(password).set_next(active)

requests = [
    {"username": "alice", "password": "secret123"},
    {"username": "bob", "password": "wrongpass"},
    {"username": "charlie", "password": "abc123"},
    {"password": "no_username"},
]

for request in requests:
    result = fields.handle(request)
    print(f"Request: {request} → {result}")


#     Chain of Responsibility pattern summary:

# Each handler decides: “Can I handle this?”

# If not, it passes it along.

# You can add or remove handlers dynamically.

# Ideal for pipelines like:

# Request validation

# Logging

# Event filtering

# Support ticket escalation

# File processing (compression → encryption → sending)