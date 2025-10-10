""" CoR pattern
Lets you pass a request thorugh a series of handlers.
Each handler:
- Processes the request or
- Passes it to the next handler in the chain

You use it when:
- you want to decouple senders from receivers
- The handling rules can change
- Multiple handlers might handler a request (or only one should)
"""

""" example: Expense approval
- Team can approve up to 500 Euros
- Manager up to 2500
- Director up to 10000
- CFO anything higher than that
"""

from dataclasses import dataclass
from typing import Optional, Protocol

@dataclass(frozen=True)
class Expense:
    employee: str
    amount: float
    purpose: str

class Handler(Protocol):
    def set_next(self, nxt: "Handler") -> "Handler":
        pass

    def handle(self, request: Expense) -> str:
        pass

class BaseHandler:
    def __init__(self):
        self._next: Optional[Handler] = None

    def set_next(self, nxt: Handler) -> Handler:
        self._next = nxt
        return nxt
    
    def handle(self, request: Expense) -> str:
        if self._next:
            return self._next.handle(request)
        return f"No one could handle expense request of {request.amount:.2f} Euros - rejected."
    
""" Concrete Handlers """
class RoleApprover(BaseHandler):
    def __init__(self, role: str, limit: float) -> None:
        super().__init__()
        self.role = role
        self.limit = limit

    def handle(self, request: Expense) -> str:
        if request.amount <= self.limit:
            return (
                f"{self.role} approved {request.amount:.2f} Euros for "
                f"{request.employee} - {request.purpose}. (limit {self.limit:.0f} Euros.)"
            )
        return super().handle(request)
    
class CFO(BaseHandler):
    def handle(self, request: Expense) -> str:
        # CFO always decides - could add extra logic here
        return (
            f"CFO approved {request.amount:.2f} Euros for "
            f" {request.employee} - {request.purpose}."
        )
    
# Test
team_lead = RoleApprover("Team Lead", 500)
manager = RoleApprover("Manager", 2500)
director = RoleApprover("Director", 10000)
cfo = CFO()

# Wiring the chain and using it.
team_lead.set_next(manager).set_next(director).set_next(cfo)

# Try a few request
cases = [
    Expense("Anna", 120, "Sushi for team"),
    Expense("Benjamin", 1900, "Conference travel"),
    Expense("Charlie", 7800, "New laptops"),
    Expense("Daniela", 25_000, "Project budget")
]

for case in cases:
    print(team_lead.handle(case))

""" Principles seen here:
- Open/Closed: Add a new approver without touching others
- Decoupling: The caller doesn't know who approves it; it just calls handle
- Reusability: Same structure works for logging pipelines, request filters
"""

""" Variations """
# Early stop vs. multi-handler: We stop when one handler approves. If instead you want
# every handler to do something (log -> validate -> transform), return a flag and continue.
class MultiHandler(BaseHandler):
    def handle(self, request: Expense) -> str:
        # do something
        note = f"{self.__class__.__name__} saw {request.amount:.2f}"
        # always forward
        more = super().handle(request)
        return f"{note}\n{more}" if more else note
    

    