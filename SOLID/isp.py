class Machine:
    def print(self, document):
        raise NotImplementedError
    def fax(self, document):
        raise NotImplementedError
    def scan(self, document):
        raise NotImplementedError
    
class MultiFunctionPrinter(Machine):
    def print(self, document):
        pass

# Now there is a problem. An old printer cant fax or scan. The client sees this code.
class OldPrinter(Machine):
    def print(self):
        pass

    def fax(self, document):
        raise NotImplementedError("Printer cannot fax")

    def scan(self, document):
        """ Not supported! """
        raise NotImplementedError("Printer cannot scan")
        

# ISP: Solution is to split the base interface into it's actual functionalities.
class Printer:
    def print(self, document):
        pass

class Scanner:
    def scan(self, document):
        pass

class MyPrinter(Printer):
    def myprint(self, document):
        pass
    

