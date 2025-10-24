""" security_proxy.py
Security (access control) proxy example that wraps a document
store.

The proxy enforces role-based permissions, per-user rate limiting and auditing before delegating to the
real service.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
import time
from collections import defaultdict, deque

# Subject interface
class DocumentService(ABC):
    @abstractmethod
    def get_doc(self, doc_id: str) -> str:
        pass

    @abstractmethod
    def put_doc(self, doc_id: str) -> None:
        pass

    @abstractmethod
    def delete_doc(self, doc_id: str) -> None:
        pass

# Real subject (the thing we protect)
class InMemoryDocumentStore(DocumentService):
    def __init__(self):
        self._db: dict[str, str] = {}

    def get_doc(self, doc_id: str) -> str:
        return self._db[doc_id]

    def put_doc(self, doc_id: str, content: str) -> None:
        self._db[doc_id] = content
    
    def delete_doc(self, doc_id: str) -> None:
        del self._db[doc_id]

# Simple auth model
@dataclass(frozen=True)
class User:
    username: str
    roles: set[str]

# Map roles -> allowed actions
ROLE_PERMS = {
    "READER": {"read"},
    "EDITOR": {"read", "write"},
    "ADMIN": {"read", "write", "delete"},
}

# Proxy with secutity + rate limiting + audit
class SecureDocumentProxy(DocumentService):
    def __init__(self, real: DocumentService):
        self._real = real
        self._audit_log: list[str] = []
        # naive token bucket: max 5 reads per 10 seconds per user
        self._reads_window = 10
        self._reads_limit = 5
        self._reads_hist: dict[str, deque[float]] = defaultdict(deque)

    # --- public API mirrors the subject
    def get_doc(self, doc_id: str, *, user: User) -> str:
        self._check_perm(user, "read")
        self._rate_limit_reads(user)
        self._audit(f"{user.username} READ {doc_id}")
        return self._real.get_doc(doc_id)
    
    def put_doc(self, doc_id: str, content: str, *, user: User) -> None:
        self._check_perm(user, "write")
        self._audit(f"{user.username} WRITE {doc_id}")
        self._real.put_doc(doc_id, content)

    def delete_doc(self, doc_id: str, *, user: User) -> None:
        self._check_perm(user, "delete")
        self._audit(f"{user.username} DELETE {doc_id}")
        self._real.delete_doc(doc_id)

    # helpers
    def _check_perm(self, user: User, action: str) -> None:
        allowed = set().union(*(ROLE_PERMS.get(r, set()) for r in user.roles))
        if action not in allowed:
            self._audit(f"{user.username} DENIED {action.upper()}")
            raise PermissionError
        
    def _rate_limit_reads(self, user: User) -> None:
        now = time.time()
        hist = self._reads_hist[user.username]
        # drop timestamps outside the window
        while hist and now - hist[0] > self._reads_window:
            hist.popleft()
        if len(hist) >= self._reads_limit:
            self._audit(f"{user.username} RATE-LIMITED read")
            raise RuntimeError("read rate limit exceeded")
        hist.append(now)

    def _audit(self, line: str) -> None:
        ts = time.strftime("%H:%M:%S")
        self._audit_log.append(f"[{ts}] {line}")

    def audit_dump(self) -> str:
        return "\n".join(self._audit_log)

if __name__ == "__main__":
    store = InMemoryDocumentStore()
    proxy = SecureDocumentProxy(store)

    admin = User("alice", {"ADMIN"})
    editor = User("bob", {"EDITOR"})
    intern = User("ivy", {"READER"})

    proxy.put_doc("policy", "Write test", user=admin)
    proxy.put_doc("runbook", "Rollback", user=admin)

    # Reader can read, but not write/delete
    print("Reader fetch:", proxy.get_doc("policy", user=intern))
    try:
        proxy.put_doc("policy", "hacked", user=intern)
    except PermissionError as ex:
        print("Denied:", ex)

    # Editor can modify, not delete
    proxy.put_doc("policy", "Always write tests", user=editor)
    try:
        proxy.delete_doc("policy", user=editor)
    except PermissionError as ex:
        print("Denied:", ex)

    # Admin can delete
    proxy.delete_doc("policy", user=admin)

        # Show rate limiting (5 reads allowed in 10s)
    try:
        for _ in range(6):
            _ = proxy.get_doc("runbook", user=intern)
    except RuntimeError as e:
        print("Rate limit triggered:", e)

    print("\n--- AUDIT LOG ---")
    print(proxy.audit_dump())