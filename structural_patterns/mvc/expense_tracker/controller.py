from typing import Optional
from model import ExpenseRepository
import view

class ExpenseController:
    """Coordinates user inputs with business/data operations (model)
    Keeps app logic so view/model stay decoupled
    """
    def __init__(self, repo: ExpenseRepository):
        self.repo = repo

    def run_once(self) -> bool:
        view.show_menu()
        choice = view.get_choice()

        if choice == "1":
            amount, category, note = view.prompt_new_expense()
            added = self.repo.add(amount, category, note)
            view.notify(f"Added expense {added.id}")
        elif choice == "2":
            view.show_expenses(self.repo.list_all())
        elif choice == "3":
            cat = view.prompt_category()
            view.show_expenses(self.repo.filter_by_category(cat))
        elif choice == "4":
            cat = input("Leave blank for grand total or enter a category: ").strip()
            total = self.repo.total(cat or None)
            view.show_total(total, cat or None)
        elif choice == "5":
            expense_id = view.prompt_expense_id()
            ok = self.repo.delete(expense_id)
            view.notify("Deleted" if ok else "No expense found with that ID.")
        elif choice == "0":
            return False  # stop the loop
        else:
            view.notify("Invalid option. Try again.")
        return True