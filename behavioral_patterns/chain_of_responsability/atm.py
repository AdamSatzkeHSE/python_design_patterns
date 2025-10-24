""" Chain of responsability
- Sending a request to the first object in the chain
- Object decides whether it should satisfy the request or not
- The object forwards the request to the next object
- This procedure is repeated until we reach the end of the chain
"""
""" CoR provides a chance to a number of different objects to satisfy a specific request.
This is useful when we don't know which object should satisfy a request in advance
"""
class Event:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
class Widget:
    def __init__(self, parent=None):
        self.parent = parent

    def handle(self, event):
        handler = f"handle_{event}"
        if hasattr(self, handler):
            method = getattr(self, handler)
            method(event)
        elif self.parent is not None:
            self.parent.handle(event)
        elif hasattr(self, 'handle_default'):
            self.handle_default(event)

class MainWindow(Widget):
    def handle_close(self, event):
        print(f"MainWindow: {event}")

    def handle_default(self, event):
        print(f"MainWindow Default: {event}")

class SendDialog(Widget):
    def handle_paint(self, event):
        print(f"SendDialog: {event}")

class MsgText(Widget):
    def handle_down(self, event):
        print(f"MsgText: {event}")

""" We create widgets and events. Widget react to the events."""
mw = MainWindow()
sd = SendDialog(mw)
msg = MsgText(sd)

for e in ("down", "paint", "unhandled", "close"):
    evt = Event(e)
    print(f"Sending event -{evt}- to MainWindow")
    mw.handle(evt)
    print(f"Sending event -{evt}- to SendDialog")
    sd.handle(evt)
    print(f"Sending event -{evt}- to MsgText")
    msg.handle(evt)

    