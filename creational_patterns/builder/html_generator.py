""" When we want to create an object that is composed of multiple parts and 
the composition needs to be done step by step. The object is not complete unless all its
parts are fully created.

The builder pattern separates the construction of a complex object from its representation
By keeping the construction separate from the representation, the same construction can be used
to create several different represenatations.
"""

# The Builder: The component responsible for creating various parts of a complex object.
# HTML: title, head, body

# The director: The component that controls the building process using a builder instance.
# It calls the builders functions for setting the title, the heading and so on.

# Using different builder instances let's us create different HTML pages without touchgin any of the
# code of the director.


