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
    "--timezone",
    "-t",
    type=click.STRING,
    help="Calendar timezone.",
    default="UTC",
    show_default=True,
)
@click.option(  # type: ignore
    "--locale",
    "-l",
    type=click.STRING,
    help="Locale used to parse data such as month abbreviated names.",
    default="pt_BR",
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
def footcal(
    name: click.STRING,  # pylint: disable=unused-argument
    timezone: click.STRING,  # pylint: disable=unused-argument
    locale: click.STRING,  # pylint: disable=unused-argument
    url: click.STRING,  # pylint: disable=unused-argument
) -> None:
    """Create an icalendar from web fixtures.

    The calendar is dumped to stdout.
    """


# mypy disabled where the following error was being
# reported:
#   Untyped decorator makes function "espn" untyped
@footcal.command()  # type: ignore
@click.pass_context  # type: ignore
def espn(ctx: click.core.Context) -> None:
    """Fixures from ESPN website."""
    parser = ESPNParser(
        timezone_id=ctx.parent.params["timezone"], locale=ctx.parent.params["locale"]
    )
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
