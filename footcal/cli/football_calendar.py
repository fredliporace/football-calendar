"""football_calendar CLI."""

import click

from footcal.parsers import ESPNParser


@click.group()  # type: ignore
@click.option(  # type: ignore
    "--name",
    "-n",
    type=click.STRING,
    help="Calendar name.",
    default="Calendar",
    show_default=True,
)
@click.option(  # type: ignore
    "--url",
    "-u",
    type=click.STRING,
    help="URL for fixtures.",
    required=True,
    default="https://www.espn.com.br/futebol/time/calendario/_/id/3445/fluminense",
    show_default=True,
)
def footcal(name: str, url: str) -> None:  # pylint: disable=unused-argument
    """Create an icalendar from web fixtures.

    The calendar is dumped to stdout.
    """


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
@click.pass_context  # type: ignore
def espn(ctx: click.core.Context, delta_hour: click.INT, locale: click.STRING) -> None:
    """Fixures from ESPN website."""
    parser = ESPNParser(delta_hour=delta_hour, locale=locale)
    calendar = parser.get_calendar(
        url=ctx.parent.params["url"], calendar_name=ctx.parent.params["name"]
    )
    print(calendar.to_ical().decode("utf-8"))


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
