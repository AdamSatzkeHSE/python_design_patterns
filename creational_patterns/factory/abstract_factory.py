""" We want to create Buttons for Windows and for MAC-OS"""

from abc import ABC, abstractmethod

# Abstract interfaces

class Button(ABC):
    @abstractmethod
    def paint(self):
        pass

class Checkbox(ABC):
    @abstractmethod
    def paint(self):
        pass

# Concrete classes for Windows
class WindowsButton(Button):
    def paint(self):
        return "Windows Button"
    
class WindowsCheckbox(Checkbox):
    def paint(self):
        return "Windows Checkbox"
    
# Concrete classes for MAC
class MacButton(Button):
    def paint(self):
        return "MAC Button"
    
class MacCheckbox(Checkbox):
    def paint(self):
        return "MAC Checkbox"
    
# GUI Factory
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass

# Concrete Factories

class WindowsFactory(GUIFactory):
    def create_button(self) -> Button:
        return WindowsButton()
    
    def create_checkbox(self):
        return WindowsCheckbox()
    
class MacFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacButton()
    
    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()
    
# Client code
def client_code(factory: GUIFactory):
    button = factory.create_button()
    checkbox = factory.create_checkbox()

    print(button.paint())
    print(checkbox.paint())

if __name__ == "__main__":
    print("Using windows factory")
    client_code(WindowsFactory())

    print("Using Max Factory")
    client_code(MacFactory())

# Abstract Factory defines the interface (GUIFactory) for creating products.
# Concrete Factories (WindowsFactory, MacFactory) implement that interface.

# Abstract Products (Button, Checkbox) define the product interfaces.

# Concrete Products implement those interfaces.

# Client code only depends on the factory and abstract product interfaces — not the concrete classes.