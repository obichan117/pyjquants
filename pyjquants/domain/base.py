"""Base classes for domain entities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pyjquants.infra.client import JQuantsClient
from pyjquants.infra.session import _get_global_session

if TYPE_CHECKING:
    from pyjquants.infra.session import Session


class DomainEntity:
    """Base class for domain entities with session and client."""

    _session: Session
    _client: JQuantsClient

    def __init__(self, session: Session | None = None) -> None:
        self._session = session or _get_global_session()
        self._client = JQuantsClient(self._session)


class CodeBasedEntity(DomainEntity):
    """Base class for entities identified by a code."""

    code: str

    def __init__(self, code: str, session: Session | None = None) -> None:
        super().__init__(session)
        self.code = code

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.code == other.code
        if isinstance(other, str):
            return self.code == other
        return False

    def __hash__(self) -> int:
        return hash(self.code)

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self.code}')"

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.code})"
