"""J-Quants API client with generic fetch and parse."""

from __future__ import annotations

import logging
from datetime import date
from typing import TYPE_CHECKING, Any, TypeVar

import pandas as pd

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from pyjquants.adapters.endpoints import Endpoint
    from pyjquants.infra.session import Session

T = TypeVar("T")


class JQuantsClient:
    """Generic client for J-Quants API.

    Provides typed fetch methods that use endpoint definitions
    to automatically parse responses into domain models.

    Example:
        client = JQuantsClient(session)
        bars = client.fetch_list(DAILY_QUOTES, {"code": "7203"})
    """

    def __init__(self, session: Session) -> None:
        """Initialize client with session.

        Args:
            session: Authenticated HTTP session
        """
        self._session = session
        self._model_cache: dict[str, type] = {}

    def _get_model(self, endpoint: Endpoint[T]) -> type[T]:
        """Resolve model class from endpoint definition."""
        model = endpoint.model
        if isinstance(model, str):
            # Lazy import to avoid circular dependencies
            if model not in self._model_cache:
                from pyjquants.domain import models

                self._model_cache[model] = getattr(models, model)
            return self._model_cache[model]
        return model

    # === CORE FETCH METHODS ===

    def fetch_one(self, endpoint: Endpoint[T], params: dict[str, Any] | None = None) -> T | None:
        """Fetch single item from endpoint.

        Args:
            endpoint: Endpoint definition
            params: Query parameters

        Returns:
            Parsed model instance or None if not found/validation fails
        """
        data = self._session.get(endpoint.path, params)
        items = data.get(endpoint.response_key, [])
        if not items:
            return None
        model = self._get_model(endpoint)
        try:
            return model.model_validate(items[0])  # type: ignore[attr-defined, no-any-return]
        except Exception as e:
            logger.warning("Failed to validate %s item: %s", model.__name__, e)
            return None

    def fetch_list(self, endpoint: Endpoint[T], params: dict[str, Any] | None = None) -> list[T]:
        """Fetch list of items from endpoint.

        Args:
            endpoint: Endpoint definition
            params: Query parameters

        Returns:
            List of parsed model instances
        """
        model = self._get_model(endpoint)

        if endpoint.paginated:
            items = self._session.get_paginated(endpoint.path, params, endpoint.response_key)
        else:
            data = self._session.get(endpoint.path, params)
            items = data.get(endpoint.response_key, [])

        result: list[T] = []
        for item in items:
            try:
                result.append(model.model_validate(item))  # type: ignore[attr-defined]
            except Exception as e:
                logger.warning("Failed to validate %s item: %s", model.__name__, e)
                continue
        return result

    def fetch_dataframe(
        self, endpoint: Endpoint[T], params: dict[str, Any] | None = None
    ) -> pd.DataFrame:
        """Fetch data as pandas DataFrame.

        Args:
            endpoint: Endpoint definition
            params: Query parameters

        Returns:
            DataFrame with parsed data
        """
        items = self.fetch_list(endpoint, params)
        if not items:
            return pd.DataFrame()

        data = []
        for item in items:
            if hasattr(item, "to_dict"):
                data.append(item.to_dict())
            elif hasattr(item, "model_dump"):
                data.append(item.model_dump())
            else:
                data.append(dict(item))  # type: ignore[call-overload]

        df = pd.DataFrame(data)
        if "date" in df.columns:
            df = df.sort_values("date").reset_index(drop=True)
        return df

    # === PARAM HELPERS ===

    @staticmethod
    def date_params(
        code: str | None = None,
        start: date | None = None,
        end: date | None = None,
    ) -> dict[str, str]:
        """Build common date range params.

        Args:
            code: Stock code
            start: Start date
            end: End date

        Returns:
            Dict of query parameters
        """
        params: dict[str, str] = {}
        if code:
            params["code"] = code
        if start:
            params["from"] = start.strftime("%Y%m%d")
        if end:
            params["to"] = end.strftime("%Y%m%d")
        return params
