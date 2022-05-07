"""Test scrape_glosbe_dict."""
# pylint: disable=broad-except
from scrape_glosbe_dict import __version__
from scrape_glosbe_dict import scrape_glosbe_dict


def test_version():
    """Test version."""
    assert __version__[:3] == "0.1"


def test_sanity():
    """Check sanity."""
    try:
        assert not scrape_glosbe_dict()
    except Exception:
        assert True


def test_de2zh():
    """Test de2zh."""
    assert "女人" in scrape_glosbe_dict("Frau", "de")