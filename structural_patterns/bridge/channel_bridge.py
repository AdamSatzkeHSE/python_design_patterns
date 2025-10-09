""" Notifications vs. Channels
Notification is the abstraction
Channel is the Implementation
"""

from abc import ABC, abstractmethod
from datetime import datetime

# Implementation hierarchy
class Channel(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> None:
        pass

class EmailChannel(Channel):
    def send(self, to: str, subject: str, body: str) -> None:
        print(f"[EMAIL] -> {to}\nSubject: {subject}\n {body}\n")

class SMSChannel(Channel):
    def send(self, to: str, subject: str, body: str) -> None:
        # SMS ignores subject and has length limits (simulated)
        text = (subject + ": " + body)[:160]
        print(f"[SMS] -> {to}\n{text}\n")

class SlackChannel(Channel):
    def __init__(self, room: str="general"):
        self.room = room
    
    def send(self, to: str, subject: str, body: str) -> None:
        print(f"[SLACK]{self.room} @ {to}\n*{subject}*\n{body}\n")

# Abstraction Hierarchy (high-level notifications)
class Notification(ABC):
    """ High level behavior that delegates delivery to a Channel """
    def __init__(self, channel: Channel):
        self.channel = channel

    @abstractmethod
    def notify(self, to: str, title: str, message: str) -> None:
        self.channel.send(to, title, message)

class BasicNotification(Notification):
    def notify(self, to: str, title: str, message: str) -> None:
        self.channel.send(to, title, message)

class AlertNotification(Notification):
    """ Adds metadata, formatting, and a footer, without touching channels. """
    def notify(self, to: str, title: str, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        decorated_title = f"[ALERT] {title}"
        body = f"{message}\n\n - sent at {timestamp}"
        self.channel.send(to, decorated_title, body)

class DigestNotification(Notification):
    """ Accumulates entries and flushes them as a single message """
    def __init__(self, channel: Channel):
        super().__init__(channel)
        self._buffer: list[str] = []

    def add_entry(self, entry: str) -> None:
        self._buffer.append(entry)

    def notify(self, to: str, title: str, message: str) -> None:
        self.add_entry(message)
        # no immediate send; use flush() when you want to deliver
        print("[Digest] queued:", message)

    def flush(self, to: str, title: str) -> None:
        if not self._buffer:
            print("[Digest] nothing to send.")
            return
        combined = "\n • " + "\n • ".join(self._buffer)
        self.channel.send(to, f"[DIGEST] {title}", combined)
        self._buffer.clear()

if __name__ == "__main__":
    # Channels (implementations)
    email = EmailChannel()
    sms = SMSChannel()
    slack = SlackChannel("Python")

    # Abstractions using different channels
    welcome = BasicNotification(email)
    pager = AlertNotification(sms)
    team_digest = DigestNotification(slack)
    goodbye = BasicNotification(sms)
    vodafone_spam = AlertNotification(email)

    welcome.notify("mustermann@musteremail.com", "welcome", "Hello, welcome to this Python Course.")
    pager.notify("client", "alert", "Achtung")
    team_digest.notify("team@company.de", "Weekly report", "Hello team")

""" Why this is a bridge:
- Two independent dimensions: Notification behavior (formatting, batching, retry logic)
- You can add WhatsappChannel, Webhookchannel, without editing any Notification classes.
- You can add RetryingNotification or MarketingNotification
"""
