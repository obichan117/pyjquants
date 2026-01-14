"""Decorators for tier-based access control."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import TYPE_CHECKING, Any, TypeVar

from pyjquants.infra.config import Tier
from pyjquants.infra.exceptions import TierError

if TYPE_CHECKING:
    from pyjquants.infra.session import Session

F = TypeVar("F", bound=Callable[..., Any])


def requires_tier(required: Tier) -> Callable[[F], F]:
    """Decorator to check subscription tier before method execution.

    Checks that the session's tier meets the required tier level.
    Raises TierError if the current tier is insufficient.

    Args:
        required: Minimum tier required for this method

    Example:
        @requires_tier(Tier.STANDARD)
        def history_am(self, ...):
            ...
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            # Get session from self (domain classes store it as _session)
            session: Session | None = getattr(self, "_session", None)
            if session is None:
                # Fallback: some objects might store session differently
                raise RuntimeError(
                    f"Cannot check tier: {type(self).__name__} has no _session attribute"
                )

            current_tier = session.tier
            if current_tier < required:
                raise TierError(
                    method=func.__name__,
                    required_tier=required.value,
                    current_tier=current_tier.value,
                )

            return func(self, *args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator
