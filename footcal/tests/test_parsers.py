"""test parsers."""
import pytest

from footcal.parsers import ESPNParser, Parser


def test_parser_subclasses() -> None:
    """test_parser_subclasses."""
    subclasses = Parser.__subclasses__()
    assert sorted([subclass.__name__ for subclass in subclasses]) == ["ESPNParser"]


def test_parser() -> None:
    """test_parser.

    This instantiates a concrete class but only test features from base class.
    """
    parser = ESPNParser()
    with pytest.raises(RuntimeError):
        parser.get_matches(url="http://google.com/error.html")


def test_espn_parser() -> None:
    """test_espn_parser."""
    espn = ESPNParser(delta_hour=1)
    matches = espn.get_matches(
        url="https://www.espn.com.br/futebol/time/calendario/_/id/3445/fluminense"
    )
    assert len(matches) == 33
