import time
from functools import wraps

def timed(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        try:
            return fn(*args, **kwargs)
        finally:
            print(f"{fn.__name__} took {time.time()-t0:.4f}s")
    return wrapper

@timed
def slow():
    time.sleep(0.1)
    return "done"

if __name__ == "__main__":
    print(slow())
