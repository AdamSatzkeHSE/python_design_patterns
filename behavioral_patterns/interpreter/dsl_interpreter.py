""" dsl_interpreter.py:

Implement language to decide if a user may perform an action on a resource.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Iterable

# Interpreter
class Expr:
    def interpreter(self, ctx: Dict[str, Any]) -> bool:
        raise NotImplementedError
    
@dataclass(frozen=True)
class And(Expr):
    left: Expr
    right: Expr

    def interpret(self, ctx: Dict[str, Any]) -> bool:
        return self.left.interpret(ctx) and self.right.interpret(ctx)
    
@dataclass(frozen=True)
class Or(Expr):
    left: Expr
    right: Expr
    def interpret(self, ctx: Dict[str, Any]) -> bool:
        return self.left.interpret(ctx) or self.right.interpret(ctx)

@dataclass(frozen=True)
class Not(Expr):
    expr: Expr
    def interpret(self, ctx: Dict[str, Any]) -> bool:
        return not self.expr.interpret(ctx)

@dataclass(frozen=True)
class Comparison(Expr):
    field: str
    op: str
    value: Any
    def interpret(self, ctx: Dict[str, Any]) -> bool:
        left = ctx.get(self.field)
        # Try numeric compare if both look numeric; otherwise string compare (case-insensitive)
        def to_num(x):
            try:
                return float(x)
            except (TypeError, ValueError):
                return None

        lnum, rnum = to_num(left), to_num(self.value)
        if lnum is not None and rnum is not None:
            if self.op == "=":  return lnum == rnum
            if self.op == "!=": return lnum != rnum
            if self.op == ">":  return lnum >  rnum
            if self.op == ">=": return lnum >= rnum
            if self.op == "<":  return lnum <  rnum
            if self.op == "<=": return lnum <= rnum
        else:
            ls = ("" if left is None else str(left)).lower()
            rs = ("" if self.value is None else str(self.value)).lower()
            if self.op == "=":  return ls == rs
            if self.op == "!=": return ls != rs
            # Non-numeric ordering ops are false by default
            return False
        return False

@dataclass(frozen=True)
class InSet(Expr):
    field: str
    values: List[str]  # compare as case-insensitive strings
    def interpret(self, ctx: Dict[str, Any]) -> bool:
        v = ctx.get(self.field)
        if v is None: 
            return False
        return str(v).lower() in {s.lower() for s in self.values}
    
# ---------------- Lexer / Parser ----------------

PRECEDENCE = {"NOT": 3, "AND": 2, "OR": 1}
RIGHT_ASSOC = {"NOT"}

def tokenize(s: str) -> List[str]:
    # insert spaces around parens and braces to split cleanly
    for ch in "(){},":
        s = s.replace(ch, f" {ch} ")
    parts = s.split()
    # Normalize keywords
    normalized: List[str] = []
    for p in parts:
        up = p.upper()
        if up in {"AND", "OR", "NOT", "IN"}:
            normalized.append(up)
        else:
            normalized.append(p)
    # Recombine predicate tokens into single items for easier RPN/AST:
    # Patterns:
    #   field (=|!=|>|>=|<|<=) value
    #   field IN { v1 , v2 , ... }
    i = 0
    tokens: List[str] = []
    def is_op(tok: str) -> bool:
        return tok in ("=", "!=", ">", ">=", "<", "<=")

    while i < len(normalized):
        t = normalized[i]
        # Merge >=, <=, != if user wrote them without space (e.g., "age>=3") — optional
        for op in (">=", "<=", "!=", ">", "<", "="):
            if op in t and not t in ("(", ")", "{", "}", ",") and not t.upper() in ("AND","OR","NOT","IN"):
                # split field<op>value to tokens if it's of that shape
                field, sep, rest = t.partition(op)
                if sep:
                    normalized[i:i+1] = [field, sep, rest]
                    t = field
                break

        # Look for "field IN { ... }"
        if (i + 3 < len(normalized) and
            normalized[i+1] == "IN" and normalized[i+2] == "{"):
            field = t
            i += 3
            vals: List[str] = []
            while i < len(normalized) and normalized[i] != "}":
                if normalized[i] != ",":
                    vals.append(normalized[i].strip().strip('"').strip("'"))
                i += 1
            if i == len(normalized) or normalized[i] != "}":
                raise ValueError("Unclosed set in IN {...}")
            tokens.append(f"INSET::{field}::" + "|".join(vals))
            i += 1
            continue

        # Look for "field op value"
        if i + 2 < len(normalized) and is_op(normalized[i+1]):
            field, op, value = normalized[i], normalized[i+1], normalized[i+2]
            tokens.append(f"CMP::{field}::{op}::{value}")
            i += 3
            continue

        # Otherwise pass through parentheses/ops/identifiers
        tokens.append(t)
        i += 1

    return tokens

def to_rpn(tokens: Iterable[str]) -> List[str]:
    out: List[str] = []
    ops: List[str] = []
    for t in tokens:
        if t == "(":
            ops.append(t)
        elif t == ")":
            while ops and ops[-1] != "(":
                out.append(ops.pop())
            if not ops:
                raise ValueError("Mismatched parentheses")
            ops.pop()
        elif t in PRECEDENCE:
            while (ops and ops[-1] in PRECEDENCE and
                   (PRECEDENCE[ops[-1]] > PRECEDENCE[t] or
                    (PRECEDENCE[ops[-1]] == PRECEDENCE[t] and t not in RIGHT_ASSOC))):
                out.append(ops.pop())
            ops.append(t)
        else:
            out.append(t)
    while ops:
        op = ops.pop()
        if op in ("(", ")"):
            raise ValueError("Mismatched parentheses")
        out.append(op)
    return out

def rpn_to_ast(rpn: List[str]) -> Expr:
    stack: List[Expr] = []
    for t in rpn:
        if t == "AND" or t == "OR":
            if len(stack) < 2:
                raise ValueError("Insufficient operands")
            b, a = stack.pop(), stack.pop()
            stack.append(And(a, b) if t == "AND" else Or(a, b))
        elif t == "NOT":
            if not stack:
                raise ValueError("Insufficient operands for NOT")
            stack.append(Not(stack.pop()))
        elif t.startswith("CMP::"):
            _, field, op, value = t.split("::", 3)
            # strip quotes if any
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            # Convert numeric literal if possible
            try:
                lit = float(value)
                if lit.is_integer():
                    lit = int(lit)
                value = lit
            except ValueError:
                pass
            stack.append(Comparison(field, op, value))
        elif t.startswith("INSET::"):
            _, field, rest = t.split("::", 2)
            values = rest.split("|") if rest else []
            stack.append(InSet(field, values))
        else:
            raise ValueError(f"Unexpected token: {t}")
    if len(stack) != 1:
        raise ValueError("Invalid expression")
    return stack[0]

def parse(rule: str) -> Expr:
    return rpn_to_ast(to_rpn(tokenize(rule)))

# ---------------- Example usage ----------------

rule = """
(role=admin)
OR
(dept=finance AND resource=reports AND NOT action=delete)
OR
(country IN {DE, FR} AND app_version>=3)
"""

expr = parse(rule)

contexts = [
    # Allowed because role=admin
    {"role": "admin", "dept": "it", "resource": "db", "action": "delete", "country": "US", "app_version": 1},
    # Allowed because finance + reports and not deleting
    {"role": "user", "dept": "finance", "resource": "reports", "action": "view", "country": "US", "app_version": 2},
    # Denied: finance + reports but action=delete (negated)
    {"role": "user", "dept": "finance", "resource": "reports", "action": "delete", "country": "US", "app_version": 2},
    # Allowed: country in {DE,FR} and app_version>=3
    {"role": "user", "dept": "sales", "resource": "dash", "action": "view", "country": "DE", "app_version": 3},
    # Denied: DE but version too low
    {"role": "user", "dept": "sales", "resource": "dash", "action": "view", "country": "DE", "app_version": 2},
]

print([expr.interpret(c) for c in contexts])
# -> [True, True, False, True, False]