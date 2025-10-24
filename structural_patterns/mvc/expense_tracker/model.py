from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import json
from pathlib import Path
import uuid

@dataclass
class Expense:
    id: str
    amount: float
    category: str
    note: str
    created_at: datetime = field(default_factory=datetime.utcnow)

    @staticmethod
    def from_dict(d: dict) -> "Expense":
        return Expense(
            id=d["id"],
            amount=float(d["amount"]),
            category=d["category"],
            note=d.get("note", ""),
            created_at=datetime.fromisoformat(d["created_at"])
        )
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "note": self.note,
            "created_at": self.created_at.isoformat()
        }
    
class ExpenseRepository:
    """ Json file repository to keep the example realistic"""
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            self._write([])

    def _read(self) -> List[Expense]:
        data = json.loads(self.db_path.read_text(encoding="utf-8"))
        return [Expense.from_dict(item) for item in data]
    
    def _write(self, expenses: List[Expense]) -> None:
        data = [e.to_dict() for e in expenses]
        self.db_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def list_all(self) -> List[Expense]:
        return self._read()
    
    
    def add(self, amount: float, category: str, note: str = "") -> Expense:
        expense = Expense(id=str(uuid.uuid4()), amount=amount, category=category, note=note)
        items = self._read()
        items.append(expense)
        self._write(items)
        return expense
    
    def delete(self, expense_id: str) -> bool:
        items = self._read()
        new_items = [e for e in items if e.id != expense_id]
        changed = len(new_items) != len(items)
        if changed:
            self._write(new_items)
        return changed
    
