"""Adapter Pattern 2
Notifications: send via email or SMS with one Notifier
"""
from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, user: str, message: str) -> None:
        pass

class EmailService:
    def send_email(self, to_addr: str, subject: str, body: str):
        print(f"EMAIL to {to_addr}: {subject}\n{body}")

class SMSService:
    def send_sms(self, number: str, text: str):
        print(f"SMS to {number}: {text}")

class EmailAdapter(Notifier):
    def __init__(self, svc: EmailService):
        self.svc = svc

    def send(self, user_contact: str, message: str) -> None:
        self.svc.send_email(user_contact, "Notification test", message)
    
class SMSAdapter(Notifier):
    def __init__(self, svc: SMSService):
        self.svc = svc

    def send(self, user_contact: str, message: str) -> None:
        self.svc.send_sms(user_contact, message)

# Test
notifier : Notifier = EmailAdapter(EmailService())
notifier.send("max@mustermann.de", "Testing Adapter")
notifier = SMSAdapter(SMSService())
notifier.send("099646459", "2FA code: 123456")

# Emails require a body, SMS just text. The adapters unify them under Notifier.send(contact, message)
# You can use the same client code notifier.send() regardless of delivery method.