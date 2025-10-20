""" SoC: Separation of concerns.
Split an application into distinct sections, where each sections addresses a separate concern.

Layered design:
- Data Access layer
- Business logic layer
- presentation layer

MVC is a SoC principle applied to OOP
Considered architectural pattern rather than design pattern (broader scope)"""

""" Important, because every all common frameworks use a similar version of it"""

"""
Model: Core component -> Knowledge. Contains and manages business logic, data, state and rules
of the application

View: Visual representation of the model. GUI.

Controller: Link between model and view.
"""

""" 
A good model: 
- Contains all the validation
- handles the state of the application
- has access to application data
- does not depend on the UI

A good controller:
- Updates the model when the user interacts with the view
- Updates the view when the model changes
- Processes the data before delivering it to the model/view
- does not display the data
- does not access the application data directly
- does not contain validation/business rules/ logic
"""

