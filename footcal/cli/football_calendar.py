"""football_calendar CLI."""

import click

from footcal.parsers import ESPNParser


@click.group()  # type: ignore
def footcal() -> None:
    """Create an icalendar from web fixtures."""


# mypy disabled where the following error was being
# reported:
#   Untyped decorator makes function "espn" untyped
@footcal.command()  # type: ignore
@click.option(  # type: ignore
    "--delta_hour",
    "-d",
    type=click.INT,
    help="Delta hours to be applied in match time.",
    default=1,
    show_default=True,
)
@click.option(  # type: ignore
    "--locale",
    "-l",
    type=click.STRING,
    help="Locale used to parse month abbreviated names.",
    default="pt_BR",
    show_default=True,
)
def espn(delta_hour: click.INT, locale: click.STRING) -> None:
    """Fixures from ESPN website."""
    parser = ESPNParser(delta_hour=delta_hour, locale=locale)
    print(
        parser.get_matches(
            url="https://www.espn.com.br/futebol/time/calendario/_/id/3445/fluminense"
        )
    )


# @footcal.command()
# @click.option(
#     "--parser",
#     type=click.Choice(_parser_list),
#     default=_parser_list[0],
#     help="Web fixture parser.",
#     show_default=True,
#     required=True,
# )
# def create_calendar(parser: str):
#     """Create calendar."""
#     print(parser)
#     module = __import__("footcal")
#     parser_class = getattr(module.parsers, parser)
#     parser_instance = parser_class(delta_hour=1)
