""" employees_iterator.py
Iterate over a company's hierarchy"""

from typing import List, Iterator

class Employee:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def __repr__(self):
        return f"{self.name} ({self.position})"
    
# Aggregate 1: Department
class Department:
    def __init__(self, name: str):
        self.name = name
        self._employees: List[Employee] = []

    def add_employee(self, employee: Employee):
        self._employees.append(employee)

    def __iter__(self) -> Iterator[Employee]:
        """ Iterate through employees of this department."""
        return iter(self._employees)
    

# Iterator
class CompanyIterator(Iterator):
    def __init__(self, departments: List[Department]):
        self._departments = departments
        self._dept_index = 0
        self._employee_iter = iter(self._departments[0]) if departments else None

    def __next__(self) -> Employee:
        if not self._departments:
            raise StopIteration
        
        try:
            # Try to get next employee from current department
            return next(self._employee_iter)
        except StopIteration:
            # Move to the next department
            self._dept_index += 1
            if self._dept_index >= len(self._departments):
                raise StopIteration
            self._employee_iter = iter(self._departments[self._dept_index])
            return next(self._employee_iter)
    
    def __iter__(self):
        return self
        
# Aggregate 2: Company
class Company:
    def __init__(self, name: str):
        self.name = name
        self._departments = []

    def add_department(self, department: Department):
        self._departments.append(department)

    def __iter__(self) -> CompanyIterator:
        """ Return an iterator to loop through all employees in all deparments"""
        return CompanyIterator(self._departments)
    
# Usage

if __name__ == "__main__":
    # Create departments
    dev = Department("Development")
    dev.add_employee(Employee("Alice", "Backend Developer"))
    dev.add_employee(Employee("Bob", "Frontend Developer"))

    hr = Department("Human Resources")
    hr.add_employee(Employee("Clara", "Recruiter"))
    hr.add_employee(Employee("David", "HR Manager"))

    sales = Department("Sales")
    sales.add_employee(Employee("Eve", "Sales Executive"))

    # Create company
    company = Company("TechNova")
    company.add_department(dev)
    company.add_department(hr)
    company.add_department(sales)

    print(f"All employees at {company.name}:")
    for emp in company:
        print("->", emp)