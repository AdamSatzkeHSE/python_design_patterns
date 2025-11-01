# The state pattern is for those moments when you catch
# yourself writing:

# if self.status == "...":
# ...
# elif, elif, elif, ...

# The state pattern says:
# Instead of checking the state everywhere, make the state itself an object that
# knows how to behave

# When do we need the State?
# Use it when:
# An object's behavior changes depending on its state
# You're doing lots of if current_state == ...
# You want to add new states without touching a giant if in 10 places

# Classic examples: orders, documents, mediaplayers, ATMs, traffic lights

# Example: purchase order lifecycle
# Draft -> can edit, can submit
# Submitted -> can approve, or reject
# Approved -> can ship
# Rejected -> can't do much

# The order object will delegate behavior to its current state

# 1. Without State pattern (bad version):
class Order:
    def __init__(self):
        self.status = "draft"

    def submit(self):
        if self.status == "draft":
            self.status = "submitted"
        else:
            raise ValueError("Can only submit from draft")
        
    def approve(self):
        if self.status == "submitted":
            self.status = "approved"
        else:
            raise ValueError("Can only approve submitted orders")
        
    def reject(self):
        if self.status == "submitted":
            self.status = "rejected"
        else:
            raise ValueError("Can only reject submitted orders")
    
    def ship(self):
        if self.status == "approved":
            print("Shipping order ...")
        else:
            raise ValueError("Can only ship approved orders")
        
# This works... but every new state -> more ifs

# With the state pattern we can split responsabilities
# 1. Order: the thing whose behavior changes
# 2. State interface: what every state must support
# 3. Concrete states: DraftState, SubmittedState, approvedState, RejectedState

from abc import ABC, abstractmethod

class OrderState(ABC):
    @abstractmethod
    def submit(self, order):
        ...
    @abstractmethod
    def approve(self, order):
        ...
    @abstractmethod
    def reject(self, order):
        ...
    @abstractmethod
    def ship(self, order):
        ...
# Each state will decide what's allowed

# The context:
class Order:
    def __init__(self):
        # start in Draft
        self.state: OrderState = DraftState()

    def set_state(self, state: OrderState):
        self.state = state
    
    # delegate behavior to current state
    def submit(self):
        self.state.submit(self)

    def approve(self):
        self.state.approve(self)

    def reject(self):
        self.state.reject(self)

    def ship(self):
        self.state.ship(self)
# The Order doesn't worry which state it's in, it just forward calls


# Concrete States:
class DraftState(OrderState):
    def submit(self, order):
        print("Order Submitted")
        order.set_state(SubmittedState())
    
    def approve(self, order):
        raise ValueError("Can't approve a draft order")
    
    def reject(self, order):
        raise ValueError("Can't reject a draft order")
    
    def ship(self, order):
        raise ValueError("Can't ship a draft order")
    
class SubmittedState(OrderState):
    def submit(self, order):
        raise ValueError("Already submitted")
    
    def approve(self, order):
        print("Order approved")
        order.set_state(ApprovedState())

    def reject(self, order):
        print("Order rejected")
        order.set_state(RejectedState())

    def ship(self, order):
        raise ValueError("Can't ship a submitted order: approve first.")
    

class ApprovedState(OrderState):
    def submit(self, order):
        raise ValueError("Already processed")

    def approve(self, order):
        raise ValueError("Already approved")

    def reject(self, order):
        raise ValueError("Can't reject an approved order")

    def ship(self, order):
        print("Order shipped 📦")
        # maybe stay approved, or move to ShippedState if you want

class RejectedState(OrderState):
    def submit(self, order):
        raise ValueError("Can't submit a rejected order")

    def approve(self, order):
        raise ValueError("Can't approve a rejected order")

    def reject(self, order):
        raise ValueError("Already rejected")

    def ship(self, order):
        raise ValueError("Can't ship a rejected order")
    
if __name__ == "__main__":
    order = Order() # starts as a Draft
    order.submit()  # Draft -> submitted
    order.approve() # Submitted -> Approved
    order.ship()    # Approved -> ship

    # Now if you try to ship too early:
    order = Order()
    order.ship() # raises ValueError: Can't ship a draft order

# This rule lives in the state, not in the order 

# Why this is good:
# - Bevavior is colocated with the state
# - Open to new states
# - No giant if/elif chains
# - Context stays simple

# Real life uses:
# Online orders, workflow approval, game character, media player, document editor

# State vs Strategy: pick which algorithm to use, pick which behavior to use based on current situation of the object

