import datetime

import click

from custom_types import DATE_TYPE
from maps import TOOTH_MAP, TIME_INTERVAL_MAP, DateRange, DT_PATTERN
from injuries_tables import PERMANENT_DF, PRIMARY_DF

DT_OUT = "%d %b %Y"


def _validate_tooth(tooth, dentition):
    if tooth not in TOOTH_MAP[dentition]:
        raise click.ClickException("Tooth '%s' not recognised as %s dentition" % (tooth, dentition))


def _review_dates(injury, injury_date, df):
    if injury not in df.columns:
        raise click.ClickException("Injury '%s' not recognised" % injury)
    try:
        datetime.datetime.strptime(injury_date, DT_PATTERN)
    except ValueError:
        raise click.ClickException("Injury date '%s' not in correct format '%s'" % (injury_date, DT_PATTERN))

    out = []
    for interval in df.index:
        if interval in TIME_INTERVAL_MAP:
            if df[injury][interval]:
                reviews = TIME_INTERVAL_MAP[interval](injury_date)
                # if a date is given
                if isinstance(reviews, datetime.date):
                    out.append(reviews.strftime(DT_OUT))
                # if a message is given
                elif isinstance(reviews, str):
                    out.append(reviews)
                # if a range that a review should be conducted within is given
                elif isinstance(reviews, DateRange):
                    out.append("Between " + reviews.start.strftime(DT_OUT) + " and " + reviews.end.strftime(DT_OUT))
                # if a list of reviews are given
                elif isinstance(reviews, list):
                    out.extend([r.strftime(DT_OUT) for r in reviews])

    for review_int in list(dict.fromkeys(out)):
        click.echo(review_int)
    if not out:
        click.echo("No follow-up required.")


@click.group()
def cli():
    """
    NHSGGC automation scripts
    """
    pass


@cli.group()
def review_dates():
    """
    for permanent or primary tooth injury.
    """
    pass


@review_dates.command()
@click.option("--tooth", type=click.Choice(TOOTH_MAP['permanent']))
@click.option("--injury", type=click.Choice(sorted(PERMANENT_DF.columns)), default=None)
@click.option("--injury-date", type=DATE_TYPE, required=True)
def permanent(tooth, injury, injury_date):
    """
    Determine follow-up review dates for given tooth, injury, and date that injury occurred.
    """
    _validate_tooth(tooth, "permanent")
    _review_dates(injury, injury_date, df=PERMANENT_DF)


@review_dates.command()
@click.option("--tooth", type=click.Choice(TOOTH_MAP['primary']))
@click.option("--injury", type=click.Choice(sorted(PRIMARY_DF.columns)), default=None)
@click.option("--injury-date", type=DATE_TYPE, required=True)
def primary(tooth, injury, injury_date):
    """
    Determine follow-up review dates for given tooth, injury, and date that injury occurred.
    """
    _validate_tooth(tooth, "primary")
    _review_dates(injury, injury_date, df=PRIMARY_DF)


if __name__ == '__main__':
    cli()
