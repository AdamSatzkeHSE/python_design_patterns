""" The strategy pattern promotes using multiple algorithms to solve a problem.
Its killer feature is that it makes it possible to switch algorithms at runtime transparently

So, if you know that one works better than the other, you can decide which algorithm to use.
"""

""" Real world examples:
- If we want to save money and we leave early, we can go by bus/train
- If we don't mind paying for a parking space and have our own car, we can go by car.
- If we don't have a car but we are in a hurry, we can take a taxi.
"""

""" Strategy to implement an algorithm to check if all characters in a string are unique
"""
import time

def pairs(seq):
    n = len(seq)
    for i in range(n):
        yield seq[i], seq[(i + 1) % n]

SLOW = 3
LIMIT = 5
WARNING = "too bad, you picked the slow algorithm"

# Function for the first alfgorithm
def allUniqueSort(s):
    if len(s) > LIMIT:
        print(WARNING)
        time.sleep(SLOW)

    strStr = sorted(s)
    for (c1, c2) in pairs(strStr):
        if c1 == c2:
            return False
    return True
    
def allUniqueSet(s):
    if len(s) < LIMIT:
        print(WARNING)
        time.sleep(SLOW)
    return True if len(set(s)) == len(s) else False

# Next we define allUnique() function that helps call a chosen algorithm by passing
# the corresponding strategy function

def allUnique(word, strategy):
    return strategy(word)

while True:
    word = None
    while not word:
        word = input("Insert word >")
        if word == "quit":
            print("bye")
            break
        strategy_picked = None
        strategies = {
            "1": allUniqueSet,
            "2": allUniqueSort,
            
        }
        while strategy_picked not in strategies.keys():
            strategy_picked = input("Choose strategy: [1] Use a set, [2] sort and pair")
            try:
                strategy = strategies[strategy_picked]
                print(f"allUnique({word}): {allUnique(word, strategy)}")
            except KeyError as err:
                print(f"Incorrect option")

