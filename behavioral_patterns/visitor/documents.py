# What problem does Visitor solve?

# Imagine you have a bunch of related objects — say, different kinds of documents:
# Invoice
# Report
# Contract
# You want to run different operations on them:
# export to PDF
# calculate total payments
# run compliance checks
# pretty-print
# send to an API

# You could put all those methods inside each class… but then every time you add a new operation, you have to edit all classes. That makes your model classes fat and hard to maintain.

# Visitor flips the axis:
# Keep your object structure stable (your Invoice, Report, …)
# Add new operations without editing those classes
# You do that by creating visitors — one class per operation

# So: Visitor makes it easy to add new operations over a fixed set of object types.

# Each "visitable" class implements an accept(visitor) method:

class SomeElement:
    def accept(self, visitor):
        visitor.visit_some_element(self)

# The visitor then has methods like:
class SomeVisitor:
    def visit_some_element(self, element):
        ...

# That's called double dispatch: The object chooses which visitor method to call,
# based on its own type.

# A real-life example: document processing
# Exercise: tiny "document system" with 3 document types:
# - Invoice
# - Report
# - Contract

# And we want to run two different operations on them:
# 1. Export to text (show in console)
# 2. Calculate cost / value (invoices have amounts, contracts have penalties, reports have
# no value.)

# We can write 2 visitors for that, without chaning classes again.
from abc import ABC, abstractmethod
from datetime import date

class Document(ABC):
    @abstractmethod
    def accept(self, visitor):
        """ Accept a visitor """
        pass

class Invoice(Document):
    def __init__(self, number: str, amount: float):
        self.number = number
        self.amount = amount
    
    def accept(self, visitor):
        return visitor.visit_invoice(self)
    
class Report(Document):
    def __init__(self, title: str, created_at: date):
        self.title = title
        self.created_at = created_at

    def accept(self, visitor):
        return visitor.visit_report(self)
    
class Contract(Document):
    def __init__(self, client: str, monthly_fee: float):
        self.client = client
        self.monthly_fee = monthly_fee

    def accept(self, visitor):
        return visitor.visit_contract(self)
    
# Notice that each class has in common: accept(self, visitor)
# and inside that they call the right method on the visitor.

# The visitor interface:
class DocumentVisitor(ABC):
    @abstractmethod
    def visit_invoice(self, invoice: Invoice):
        pass

    @abstractmethod
    def visit_report(self, report: Report):
        pass

    @abstractmethod
    def visit_contract(self, contract: Contract):
        pass

# Now any concrete visitor must implement these 3 methods

# Visitor 1: Export to text
class TextExportVisitor(DocumentVisitor):
    def visit_invoice(self, invoice: Invoice):
        return f"INVOICE: {invoice.number} - amount: {invoice.amount:.2f} Euros"
    
    def visit_report(self, report: Report):
        return f"REPORT: {report.title} ({report.created_at.isoformat()})"
    
    def visit_contract(self, contract: Contract):
        return f"CONTRACT with {contract.client} - {contract.monthly_fee:.2f} Euro/month"
    
# Visitor 2: Calculate monetary value
# Invoice - value is its amount
# Contract - value is 3 months of fees
# Report - no monetary value -> 0
class ValueVisitor(DocumentVisitor):
    def visit_invoice(self, invoice: Invoice):
        return invoice.amount
    
    def visit_report(self, report: Report):
        return 0.0
    
    def visit_contract(self, contract: Contract):
        return contract.monthly_fee * 3
    
if __name__ == "__main__":
    docs: list[Document] = [
        Invoice("2024-02", 1200),
        Report("Q3 analysis", date(2025, 10, 15)),
        Contract("ACME GmbH", 500)
    ]

    text_visitor = TextExportVisitor()
    value_visitor = ValueVisitor()

    for d in docs:
        print(d.accept(text_visitor))
    
    total_value = sum(d.accept(value_visitor) for d in docs)
    print("Total value:", total_value)

# What happens?:
# Each document calls its own accept method
# Which calls the right method of the visitor
#m Se we get type-specific behavior - no use of isinstance() is necessary

# Why not just use isinstance() ?
def export(doc):
    if isinstance(doc, Invoice):
        ...
    elif isinstance(doc, Report):
        ...

# But that has two problems:
# 1. You get a giant if/else that grows forever
# 2. Every new operation means another giant if/else

# The visitor pattern keeps all logic for one operation in one class

# When to use the Visitor
# - When you have a known set of classes
# - When you want to add operations frequently (export, bill, log, validate)
# - When you want to avoid editing classes every time

# When not to use the Visitor:
# - Your class hierarchy changes a lot (because then every visitor must change)
# - You only need one operation
# - Simple polymorphism works

