# Step-by-Step Instructions

# Create an interface (abstract class) called DatabaseInterface

# Define a method query(self) that all database classes must implement.

# Create the real object (RealDatabase)

# Implement the query() method to return some sensitive data.

# Create the proxy object (ProxyDatabase)

# It should accept a user_role when initialized.

# When query() is called:

# If the user role is "admin", forward the call to the real database.

# Otherwise, print or raise an “Access Denied” message.

# Test your proxy

# Create two proxy objects: one for an "admin" and one for a "guest".

# Try calling query() on both.


from abc import ABC, abstractmethod

# Step 1: Define the interface
class DatabaseInterface(ABC):
    @abstractmethod
    def query(self):
        pass

# Step 2: Real subject
class RealDatabase(DatabaseInterface):
    def query(self):
        return "Sensitive data: [User Passwords, Credit Card Numbers]"

# Step 3: Proxy
class ProxyDatabase(DatabaseInterface):
    def __init__(self, user_role):
        self.user_role = user_role
        self._real_db = RealDatabase()

    def query(self):
        if self.user_role == "admin":
            return self._real_db.query()
        else:
            return "Access Denied: Insufficient permissions"

# Step 4: Client code
admin_proxy = ProxyDatabase("admin")
guest_proxy = ProxyDatabase("guest")

print(admin_proxy.query())  # should print sensitive data
print(guest_proxy.query())  # should print Access Denied


# Enhance this code by:

# Adding a method log_access() that tracks each access attempt.

# Making the proxy lazy-load the real database only when needed (instantiate RealDatabase inside query()).