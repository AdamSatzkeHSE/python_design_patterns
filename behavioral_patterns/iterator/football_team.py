""" 
Iterator is a design pattern in which an iterator is used to traverse a container
and access the container's elements. The iterator pattern decouples algorithms from containers
In some cases, algorithms are necessarily container-specific and thus cannot be decoupled.

- Wikipedia

Iterators in Python are a language feature
"""
""" 
Real World examples:
- Whenever you have a collection of things, and you have to go through the collection by taking those things
one by one, it is an example of the iterator pattern.

So, there are many examples in real life:
- A classroom where the teacher is going to each student to give them their textbook
- A waiter in a restaurant attending to people at the table. and taking the order of each person

Use cases:
- Make it easy to navigate through a collection
- Get the next object in the collection at any point.
- Stop when you are done traversing through the collection.

Source: "Mastering Python Design Patterns", Kamon Ayeva
"""

class FootballTeamIterator:
    def __init__(self, members):
        self.members = members
        self.index = 0

    # def __iter__(self):
    #     return self
    
    def __next__(self):
        if self.index < len(self.members):
            val = self.members[self.index]
            self.index += 1
            return val
        else:
            raise StopIteration()
        
class FootballTeam:
    def __init__(self, members):
        self.members = members
    
    def __iter__(self):
        return FootballTeamIterator(self.members)
    
if __name__ == "__main__":
    members = [f"player{str(x)}" for x in range(1, 23)]
    members = members + ["coach1", "coach2", "coach3"]
    # Two ways
    team = FootballTeam(members)
    team_it = iter(team)

    # With for loop
    print("### With for loop: ###")
    for member in team:
        print(member)

    # Looping with while until StopIteration Exception
    while True:
        print(next(team_it))