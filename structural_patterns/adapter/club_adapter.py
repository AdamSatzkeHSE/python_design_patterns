""" A club's activities. """

class Club:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"the club {self.name}"
    
    def organize_event(self):
        return "Hires an artist to perform for the people"
    
""" We need to hire different musicians for events """
class Musician:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return f"the musician {self.name}"
    
    def play(self):
        return "Playing music"
    
class Dancer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"The dancer {self.name}"
    
    def dance(self):
        return "Does a dance performance"
    
""" The client code, using these classes, only knows how to call the 
organize_performance() method (on the Club class); it has no idea about play()
or dance() (on the respective class from the external)"""

""" How can we make the code work without changing the Musician and Dancer classes?
We create a generic adapter class that allows us to adapt a number of objects with different
interfaces, into one unified interface."""

class Adapter:
    def __init__(self, obj, adapted_methods):
        self.obj = obj
        self.__dict__.update(adapted_methods)

    def __str__(self):
        return str(self.obj)
    
""" When dealing with the different instances of the classes, we have two cases
- The compatible object that belongs to the Club class needs no adaptation. We can
treat is as is.
- The incompatible objects need to be adapted first, using the Adapter class.
"""

objects = [Club("Jazz Cafe"), Musician("Axl Rose"), Dancer("Shane Sparks")]
for obj in objects:
    if hasattr(obj, "play") or hasattr(obj, "dance"):
        if hasattr(obj, "play"):
            adapted_methods = dict(organize_event=obj.play)
        elif hasattr(obj, "dance"):
            dict(organize_event=obj.dance)
        # referencing the adapted object here
        obj = Adapter(obj, adapted_methods)
    print(f"{obj} {obj.organize_event()}")