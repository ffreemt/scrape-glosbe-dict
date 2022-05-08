"""Manage settings."""
# pylint: disable=invalid-name, no-self-argument

from pathlib import Path

from logzero import logger
from pydantic import BaseSettings, validator


class Settings(BaseSettings):  # pylint: disable=too-few-public-methods
    """Manage calls and period in secs for ratelimit."""

    calls: float = 100
    period: float = 900  # 15 min

    class Config:  # pylint: disable=too-few-public-methods
        """Read envs and env."""

        env_prefix = "SCRAPER_"
        env_file = ".env"
        env_file_encoding = "utf-8"

        logger.info(
            "env_prefix: %s, env_file: %s", env_prefix, Path(env_file).absolute()
        )

    @validator("calls")
    def validate_calls(cls, v):  # pylint: disable=no-self-use
        """Validate calls."""
        if not isinstance(v, float):  # wont come to this
            logger.warning("Float only, setting to default 150")
            v = 100
        if v <= 0:
            logger.warning("Makes no sense, setting to default 150")
            v = 100

        return v

    @validator("period")
    def validate_period(cls, v, values):  # pylint: disable=no-self-use
        """Validate period."""
        if not isinstance(v, float):  # unnecessary
            logger.warning("Float only, setting to default 150")
            v = 900
        if v <= 0:
            logger.warning("Makes no sense, setting to default 150")
            v = 900

        if "calls" in values and values["calls"] / v * 3600 > 400:
            logger.warning(
                " calls/period (hr) > 400, this will not likely ply well with glosbe, but we let it pass."
            )

        return v
