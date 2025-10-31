from collections import defaultdict

class EventBus:
    def __init__(self):
        self._subs = defaultdict(list)
    
    def subscribe(self, topic, fn):
        self._subs[topic].append(fn)
    
    def publish(self, topic, *args, **kwargs):
        for fn in self._subs.get(topic, []):
            fn(*args, **kwargs)

if __name__ == "__main__":
    bus = EventBus()
    bus.subscribe("price_update", lambda p: print("A:", p))
    bus.subscribe("price_update", lambda p: print("B:", p))
    bus.publish("price_update", 42)