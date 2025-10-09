""" Task templates in a project tracker 
Teams often start new tasks that share defaults - labels, checklists.
Instead of rebuilding each from scratch, we clone a prototype and apply a few overrides.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
import copy
import uuid

@dataclass
class Task:
    kind: str                     # "bug", "feature", "hotfix", ...
    title: str
    description: str
    labels: List[str] = field(default_factory=list)
    checklist: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))  # unique identity

    # Prototype-friendly clone: deep by default, with convenient overrides
    def clone(self, **overrides) -> "Task":
        new_obj = copy.deepcopy(self)
        # Give clones a new identity (common in trackers/DBs)
        new_obj.id = str(uuid.uuid4())
        for k, v in overrides.items():
            setattr(new_obj, k, v)
        return new_obj