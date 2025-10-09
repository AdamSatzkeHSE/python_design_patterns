""" Application that prints documents using a standard interface Printer
There are different printers:
* Old Printer
* Modern Printer

The goal is to print using a uniform interface, without worrying about the printer's internal
details.
"""

# Define the target interface
class Printer:
    """ Target interface expected by the application """
    def print_document(self, content: str):
        raise NotImplementedError

# Define Incompatible classes (Adaptees)
class OldPrinter:
    """ An old printer that only prints plain text """
    def print_text(self, text: str):
        print(f"[OldPrinter] Printing text: {text}")

class ModernPrinter:
    """ A modern printer that expects formatted data """
    def print_data(self, data: dict):
        print(f"[ModernPrinter] Printing with settings: {data}")

# Create adapter classes
# These adapters wrap the existing printer objects and translate calls from
# the Printer interface into what the specific printer expects.

class OldPrinterAdapter(Printer):
    """ Adapter for OldPrinter to match the Printer interface """
    def __init__(self, old_printer: OldPrinter):
        self.old_printer = old_printer

    def print_document(self, content: str):
        # Translate the call to old printer's interface
        print("[Adapter] Converting request for OldPrinter")
        self.old_printer.print_text(content)

class ModernPrinterAdapter(Printer):
    """ Adapter for ModernPrinter to match the Printer interface. """
    def __init__(self, modern_printer: ModernPrinter):
        self.modern_printer = modern_printer

    def print_document(self, content: str):
        # Translate the call into the modern printer's expected data format
        print("[Adapter] Converting request for ModernPrinter")
        data = {"text": content, "font": "Arial", "size": 12}
        self.modern_printer.print_data(data)

# Client Code (Application Layer)
def print_report(printer: Printer, text: str):
    print("Sending print job...")
    printer.print_document(text)
    print("Print job completed.\n")

if __name__ == "__main__":
    old_printer = OldPrinter()
    modern_printer = ModernPrinter()

    old_adapter = OldPrinterAdapter(old_printer)
    modern_adapter = ModernPrinterAdapter(modern_printer)

    # Both work through the same unified interface

    print_report(old_adapter, "Monthly Report")
    print_report(modern_adapter, "Modern Monthly Report")
    

