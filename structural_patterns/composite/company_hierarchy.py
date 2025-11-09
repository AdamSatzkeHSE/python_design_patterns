""" A manager can have subordinates - employees
A developer has no subordinates
Both managers and developers share common behavior
They have a name, a position, a salary, and we can 
calculate the total salary cost of any manager's
team.
"""

# We want to treat an individual employee and a manager
# with many subordinates in the same way

# We want to call ceo.get_salary()
# or ceo.show_details() without caring if ceo is a leaf or a composite

# Step 1: The component interface
from abc import ABC, abstractmethod
from typing import List

class Employee(ABC):
    """ Abstract base class for all employees
    """
    def __init__(self, name: str, position: str, salary: float):
        self.name = name
        self.position = position
        self.salary = salary

    @abstractmethod
    def get_salary(self) -> float:
        pass

    @abstractmethod
    def show_details(self, indent:int = 0) -> str:
        pass

# Step 2: The leaf
class Developer(Employee):
    def get_salary(self) -> float:
        return self.salary
    
    def show_details(self, indent: int=0) -> str:
        return " " * indent + f"{self.position}: {self.name} - ${self.salary:.2f}"

# Step 3: The Composite Manager has subordinates
class Manager(Employee):
    def __init__(self, name: str, position: str, salary: float):
        super().__init__(name, position, salary)
        self.subordinates: List[Employee] = []

    def add(self, employee: Employee):
        self.subordinates.append(employee)

    def remove(self, employee: Employee):
        self.subordinates.append(employee)

    def get_salary(self) -> float:
        # Include managers own salart + subordinates
        return self.salary + sum(e.get_salary() for e in self.subordinates)
    
    def show_details(self, indent: int=0) -> str:
        header = " " * indent + f"{self.position}: {self.name} - ${self.salary:.2f}"
        if not self.subordinates:
            return header
        
        details = "\n".join(e.show_details(indent + 1) for e in self.subordinates)
        return f"{header}\n{details}"
    
if __name__ == '__main__':
    # Lead employees
    dev1 = Developer("Max", "Frontend", 80_000)
    dev2 = Developer("Bob", "Backend", 85_000)
    dev3 = Developer("Charlie", "Mobile Developer", 100_000)
    
    #$ Managers
    tech_lead = Manager("Daniela", "Tech Lead", 200_000)
    tech_lead.add(dev1)
    tech_lead.add(dev2)

    project_manager = Manager("David", "Project Manager", 200_500)
    project_manager.add(tech_lead)
    project_manager.add(dev3)

    ceo = Manager("Phillip", "CEO", 300_000)
    ceo.add(project_manager)

    print(ceo.show_details())
    print("\nTotal company salary:", f"{ceo.get_salary():.2f}")
