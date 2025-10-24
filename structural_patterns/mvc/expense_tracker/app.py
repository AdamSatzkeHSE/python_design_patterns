from pathlib import Path
from controller import ExpenseController
from model import ExpenseRepository

def main():
    repo = ExpenseRepository(db_path=Path("./data/expenses.json"))
    controller = ExpenseController(repo)
    keep_going = True
    while keep_going:
        keep_going = controller.run_once()

if __name__ == "__main__":
    main()
    