"""Logging formatter."""

from __future__ import annotations

from typing import Any

import structlog


def get_logger(*args: Any, **initial_values: Any) -> Any:
    """Configure structlog."""

    if not structlog.is_configured():
        structlog.configure_once(
            processors=[
                structlog.stdlib.add_log_level,
                structlog.processors.format_exc_info,
                structlog.processors.TimeStamper(fmt="iso", utc=True),
                structlog.processors.JSONRenderer(),
            ],
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger(*args, **initial_values)
