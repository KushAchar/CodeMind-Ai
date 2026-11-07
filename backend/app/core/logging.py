"""Application logging configuration."""

import logging


def configure_logging() -> None:
    """Configure a consistent log format for local and deployed processes."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
