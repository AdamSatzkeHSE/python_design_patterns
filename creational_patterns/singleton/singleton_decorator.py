""" The more pythonic way is to wrap a class with a Singleton Decorator. """
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class DatabaseConnection:
    def __init__(self):
        print("Connecting to the database...")
        self.connection = "DatabaseConnectionObject"

# test
if __name__ == "__main__":
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()

    print(db1 is db2)
    