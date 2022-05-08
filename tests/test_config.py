"""Test config."""
import pytest

from scrape_glosbe_dict.config import Settings


def test_config_normal():
    """Test config normal."""
    config = Settings()
    assert config.calls == 100
    assert config.period == 900


@pytest.mark.xfail
def test_config_calls_period_str():
    """Test config normal."""
    config = Settings(calls="a", period="b")
    assert config.calls == 100
    assert config.period == 900


def test_config_calls_period_minus():
    """Test config normal."""
    config = Settings(calls=-1, period=-2)
    assert config.calls == 100
    assert config.period == 900
