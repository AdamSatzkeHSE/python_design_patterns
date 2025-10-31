# Implement a tiny event bus. Subscribers register callbacks for a price update and get notified when
# publish is called.

# After subscribing 2 listeners, publishing price = 42 should call both.

class EventBus:
    pass

if __name__ == "__main__":
    bus = EventBus()
    bus.subscribe("price_update", lambda p: print("A:", p))
    bus.subscribe("price_udpate", lambda p: print("B:", p))
    bus.publish("price_update", 42)

    