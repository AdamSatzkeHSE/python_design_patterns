# Create a Config class that behaves like a Singleton.
# Storing a key in one instance must be visible from another.

# Implement Config so that all instances share the same single instance.
# Expected:
#   Config().set("env", "prod")
#   print(Config().get("env"))  # -> "prod"

class Config:
    pass

if __name__ == "__main__":
    c1 = Config()
    c2 = Config()

    c1.set("env", "prod")
    print("env from c2:", c2.get("env"))