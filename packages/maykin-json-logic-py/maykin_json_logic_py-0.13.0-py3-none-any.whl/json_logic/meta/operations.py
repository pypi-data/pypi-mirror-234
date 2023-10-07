from typing import Protocol

from .base import Operation, register


class OperationProtocol(Protocol):
    _check_registered: bool

    def __post_init__(self) -> None:  # pragma: no cover
        ...


class SkipRegistrationCheck(OperationProtocol):
    def __post_init__(self):
        self._check_registered = False
        super().__post_init__()


@register("var")
class Var(SkipRegistrationCheck, Operation):
    def __repr__(self):
        if self.arguments[0] == "" or self.arguments[0] is None:
            return "$data"
        return f"${self.arguments[0]}"


@register("if")
class If(Operation):
    def __repr__(self):
        if (num_args := len(self.arguments)) <= 2:  # simple if arg0 then arg1 else arg2
            return super().__repr__()

        bits = ["Conditional"]
        # loop over groups of two which map to 'if x1 then x2'
        for i in range(0, num_args - 1, 2):
            condition, outcome = self.arguments[i : i + 2]
            condition_tree = repr(condition).splitlines()
            outcome_tree = repr(outcome).splitlines()

            bits += [
                "  If" if i == 0 else "  Elif",
                f"  ├─ {condition_tree[0]}",
                *[f"  │  {line}" for line in condition_tree[1:]],
                "  └─ Then",
                f"       └─ {outcome_tree[0]}",
                *[f"          {line}" for line in outcome_tree[1:]],
            ]

        if num_args % 2 == 1:
            else_tree = repr(self.arguments[-1]).splitlines()
            bits += [
                "  Else",
                f"  └─ {else_tree[0]}",
                *[f"     {line}" for line in else_tree[1:]],
            ]

        return "\n".join(bits)


@register("missing")
class Missing(SkipRegistrationCheck, Operation):
    pass


@register("missing_some")
class MissingSome(SkipRegistrationCheck, Operation):
    pass
