from typing import List, Optional
from datetime import datetime
from model import Expense

def show_menu() -> None:
    print("\n=== Expense Tracker ===")
    print("1) Add expense")
    print("2) List all expenses")
    print("3) Filter by category")
    print("4) Show totals")
    print("5) Delete an expense")
    print("0) Quit")

def get_choice() -> str:
    return input("Choose an option: ").strip()

def prompt_new_expense() -> tuple[float, str, str]:
    while True:
        try:
            amount = float(input("Amount (e.g., 12.50): ").strip())
            break
        except ValueError:
            print("Please enter a valid number.")
    category = input("Category (e.g., Food, Transport): ").strip()
    note = input("Note (optional): ").strip()
    return amount, category, note


def prompt_category() -> str:
    return input("Category: ").strip()

def prompt_expense_id() -> str:
    return input("Expense ID to delete: ").strip()

def show_expenses(expenses: List[Expense]) -> None:
    if not expenses:
        print("(No expenses found)")
        return
    print("\nID                                   | Amount   | Category   | Date                | Note")
    print("-" * 95)
    for e in expenses:
        print(f"{e.id} | {e.amount:8.2f} | {e.category:<10} | {e.created_at.strftime('%Y-%m-%d %H:%M')} | {e.note}")

def show_total(amount: float, category: Optional[str] = None) -> None:
    if category:
        print(f"Total for '{category}': {amount:.2f}")
    else:
        print(f"Grand total: {amount:.2f}")

def notify(message: str) -> None:
    print(message)