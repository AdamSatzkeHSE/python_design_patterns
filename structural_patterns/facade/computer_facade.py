""" The facade design pattern helps us to hide the internal complexity
of our systems and expose only what is necessary to the client through
a simplified interface.

Facade is an abstraction layer implemented over an existing complext system.
"""

""" Example: Boot procedure of a computer. We should have several classes, but
only the Computer class needs to be exposed to the client code.
"""

""" The client only needs to execute the start() method of the Computer class,
all the other complex parts are taken care of by the facade Computer class.
"""
