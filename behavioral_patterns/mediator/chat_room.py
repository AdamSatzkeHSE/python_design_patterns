# Implement a simple chat room system using the Mediator pattern where multiple users can send messages to each other through a central mediator — the chat room.

# No user should directly talk to another user; instead, they send messages through the mediator.

# 🧱 Concepts Involved

# Mediator → defines how objects (users) communicate.

# Concrete Mediator → implements message passing logic.

# Colleagues → objects that communicate via the mediator (e.g., User).

# ✅ Your Task

# Implement:

# A ChatRoom class (the Mediator)

# A User class (the Colleague)

# A ChatRoom.send_message() method that delivers messages to all users except the sender.

from typing import List

class ChatRoom:
    """Mediator class that manages message exchange between users."""
    def __init__(self):
        self._users: List["User"] = []

    def register(self, user: "User"):
        self._users.append(user)

    def send_message(self, message: str, sender: "User"):
        for user in self._users:
            if user != sender:
                user.receive(message, sender.name)


class User:
    """Colleague class that communicates via the ChatRoom mediator."""
    def __init__(self, name: str, chatroom: ChatRoom):
        self.name = name
        self.chatroom = chatroom
        self.chatroom.register(self)

    def send(self, message: str):
        print(f"{self.name} sends: {message}")
        self.chatroom.send_message(message, self)

    def receive(self, message: str, sender: str):
        print(f"{self.name} receives from {sender}: {message}")


# --- Demo ---
if __name__ == "__main__":
    room = ChatRoom()

    alice = User("Alice", room)
    bob = User("Bob", room)
    charlie = User("Charlie", room)

    alice.send("Hello, everyone!")
    bob.send("Hi Alice!")
    charlie.send("Hey folks, what's up?")
