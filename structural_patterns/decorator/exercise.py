# --- Your task ---
import time

def timed(fn):
    pass

@timed
def slow():
    time.sleep(0.1)
    return "done"

# --- Try it ---
if __name__ == "__main__":
    print(slow())
