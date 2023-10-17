""" main script"""
from datetime import datetime, timedelta, timezone
import logging
from os import environ, name, makedirs
from os.path import exists, expanduser, join

import click
from peewee import SqliteDatabase
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from timeslime.models import Setting
from timeslime.services.configuration_service import ConfigurationService
from timeslime.services.synchronize_service import SynchronizeService
from timeslime.services.time_service import TimeService
from timeslime.services.report_service import ReportService


CONSOLE = Console()

@click.group()
@click.option(
    "--loglevel",
    help="Set loglevel (default: WARNING)"
)
@click.option(
    "--database-file-path",
    help="Set database file path"
)
@click.pass_context
def main(ctx, loglevel, database_file_path):
    """⌚ This is timeslime! Have fun tracking your time ⌚

    Read here for further information:\n
        https://gitlab.com/lookslikematrix/timeslime

    If you've any issues report them here:\n
        https://gitlab.com/lookslikematrix/timeslime/-/issues/new
    """
    if loglevel:
        logging.basicConfig(encoding='utf-8', level=loglevel)
    else:
        logging.disable(logging.CRITICAL)

    if not database_file_path:
        if name == "nt":
            database_directory = join(environ["LOCALAPPDATA"], "timeslime")
        else:
            database_directory = join(expanduser("~"), ".local", "share", "timeslime")

        if not exists(database_directory):
            makedirs(database_directory)

        database_file_path = join(database_directory, "timeslime.db")

    database = SqliteDatabase(database_file_path)

    ctx.ensure_object(dict)
    ctx.obj["DATABASE"] = database

@main.command()
@click.option(
    "--weekly-working-hours",
    type=click.INT,
    help="Get/set your weekly working hours",
    is_flag=False,
    flag_value=-1
)
@click.option(
    "--timeslime-server",
    type=click.STRING,
    help="Get/set your timeslime server URL",
    is_flag=False,
    flag_value=None
)
@click.option(
    "--username",
    type=click.STRING,
    help="Get/set your timeslime username",
    is_flag=False,
    flag_value=None
)
@click.option(
    "--password",
    type=click.STRING,
    help="Get/set your timeslime password",
    is_flag=False,
    flag_value=None
)
@click.pass_context
def config(ctx, weekly_working_hours, timeslime_server, username, password):
    """🔧 Get or set timeslime configuration 🔧"""
    configuration_service = ConfigurationService(ctx.obj["DATABASE"])

    if weekly_working_hours is not None and weekly_working_hours >= 0:
        week = timedelta(hours=weekly_working_hours)
        daily_hours = week / 5
        configuration_service.working_hours = [
            daily_hours,
            daily_hours,
            daily_hours,
            daily_hours,
            daily_hours,
            timedelta(),
            timedelta(),
        ]

    if timeslime_server is not None:
        configuration_service.timeslime_server = timeslime_server

    if username is not None:
        configuration_service.username = username

    if password is not None:
        configuration_service.password = password

    if configuration_service.working_hours:
        table = Table(title="🔧 weekly working hours config 🔧")

        table.add_column("😩 Monday")
        table.add_column("🌟 Tuesday")
        table.add_column("🐪 Wednesday")
        table.add_column("💪 Thursday")
        table.add_column("🎉 Friday")
        table.add_column("🌞 Saturday")
        table.add_column("😌 Sunday")

        table.add_row(*map(lambda item: str(item), configuration_service.working_hours))

        CONSOLE.print(table)
    else:
        CONSOLE.print(Markdown(
            "It's seems you forgot to configure your weekly working hours\n\n"
            "You can set them with the following command (e.g for 40 hours per week):\n\n"
            "`timeslime config --weekly-working-hours=40`"
        ))

    if configuration_service.timeslime_server:
        table = Table(title="🔧 timeslime server 🔧")

        table.add_column("🔗 URL")
        table.add_column("👤 Username")
        table.add_column("🔒 Password")

        asterisk_password = ""
        if configuration_service.password is not None:
            asterisk_password = "".rjust(len(configuration_service.password), "*")

        table.add_row(
            configuration_service.timeslime_server,
            configuration_service.username,
            asterisk_password
        )

        CONSOLE.print(table)


@main.command()
@click.argument('start_time', required=False)
@click.pass_context
def start(ctx, start_time):
    """🚀 start your time 🚀"""
    configuration_service = ConfigurationService(ctx.obj["DATABASE"])
    if configuration_service.timeslime_server:
        logging.info("Synchronize before start")
        synchronize_service = SynchronizeService(ctx.obj["DATABASE"], configuration_service)
        synchronize_service.sync()
    time_service = TimeService(ctx.obj["DATABASE"])
    time_service.start(start_time)
    if configuration_service.timeslime_server:
        logging.info("Synchronize after start")
        synchronize_service = SynchronizeService(ctx.obj["DATABASE"], configuration_service)
        synchronize_service.sync()


@main.command()
@click.argument('stop_time', required=False)
@click.pass_context
def stop(ctx, stop_time):
    """🛑 stop your time 🛑"""
    configuration_service = ConfigurationService(ctx.obj["DATABASE"])
    if configuration_service.timeslime_server:
        logging.info("Synchronize before stop")
        synchronize_service = SynchronizeService(ctx.obj["DATABASE"], configuration_service)
        synchronize_service.sync()
    time_service = TimeService(ctx.obj["DATABASE"])
    time_service.stop(stop_time)
    if configuration_service.timeslime_server:
        logging.info("Synchronize after stop")
        synchronize_service = SynchronizeService(ctx.obj["DATABASE"], configuration_service)
        synchronize_service.sync()


@main.command()
@click.option(
    "--date",
    help="Set the date for the report (format: YYYY-MM-DD e.g. 2023-03-31)"
)
@click.option(
    "--all",
    "report_all",
    is_flag=True,
    help="Get a report of all your time"
)
@click.pass_context
def report(ctx, date, report_all):
    """📊 report your time 📊

Example:

    Get a report of today:\n
        timeslime report

    Get a report of all your time\n
        timeslime report --all

    Get a report of a specific day\n
        timeslime report --date=2023-07-25
    """
    configuration_service = ConfigurationService(ctx.obj["DATABASE"])
    if configuration_service.timeslime_server:
        logging.info("Synchronize before report")
        synchronize_service = SynchronizeService(ctx.obj["DATABASE"], configuration_service)
        sync_date = date
        if report_all:
            sync_date = "2000-01-01"
        else:
            if date is None:
                sync_date = str(datetime.now(
                    timezone.utc
                ).astimezone().replace(
                    hour=0, minute=0, second=0, microsecond=0
                ))
            else:
                sync_date = date
        synchronize_service.sync(sync_date)

    report_service = ReportService(ctx.obj["DATABASE"], configuration_service)
    try:
        report_service.report(date, report_all)
    except Setting.DoesNotExist:
        CONSOLE.print(Markdown(
            "It's seems you forgot to configure your weekly working hours\n\n"
            "You can set them with the following command (e.g for 40 hours per week):\n\n"
            "`timeslime config --weekly-working-hours=40`"
        ))


@main.command()
@click.option(
    "--all",
    "sync_all",
    is_flag=True,
    help="Synchronize all your time data"
)
@click.pass_context
def sync(ctx, sync_all):
    """🤝 synchronize your time of today 🤝"""
    configuration_service = ConfigurationService(ctx.obj["DATABASE"])
    if not configuration_service.timeslime_server:
        CONSOLE.print(Markdown(
            "It's seems you forgot to configure your timeslime server\n\n"
            "You can set them with the following command:\n\n"
            "`timeslime config --timeslime-server=https://api.timeslime.com/"
            " --username=USERNAME --password=supersecretpassword`"
        ))
        return
    synchronize_service = SynchronizeService(ctx.obj["DATABASE"], configuration_service)
    sync_date = None
    if sync_all:
        sync_date = "2000-01-01"
    synchronize_service.sync(sync_date)


@main.command()
def version():
    """📦 get version number from timeslime 📦"""
    from timeslime.__version__ import __version__

    CONSOLE.print(__version__)

if __name__ == "__main__":
    main(obj={})
