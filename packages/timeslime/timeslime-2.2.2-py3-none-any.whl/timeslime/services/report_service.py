"""report service"""
from datetime import datetime, timedelta, timezone
import logging
from typing import Optional

from peewee import Database
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from timeslime.models import Setting, Timespan
from timeslime.services.configuration_service import ConfigurationService

class ReportService():
    """class report service"""
    def __init__(
            self,
            database: Database,
            configuration_service: ConfigurationService
        ):
        """create report service"""
        self._connection = database
        self._configuration_service = configuration_service

        models = [Setting, Timespan]
        self._connection.bind(models)

    def report(self, date: Optional[str] = None, report_all: bool = False):
        """report time
        :param date: define since which date we want the report
        :param report_all: report report_all your time (default: False)"""
        logging.info("📊 report your time 📊")
        logging.debug("date: %s", date)
        logging.debug("report_all: %s", report_all)

        console = Console()
        if date and report_all:
            logging.error("Can't combine `--date` and `--all`")
            console.print(Markdown("Can't combine `--date` and `--all`\n\n"
                "You probably want to get all reports with:\n\n"
                "`timeslime report --all`\n\n"
                "or get the report for your specific date\n\n"
                f"`timeslime report --date={date}`"))
            return

        report_timespan_sum = timedelta()

        request_start_date = None
        request_stop_date = None
        if date:
            try:
                request_start_date = datetime.strptime(
                    date,
                    "%Y-%m-%d"
                ).astimezone()
            except ValueError:
                logging.error("`--date` has the wrong format.")
                today = datetime.now(
                    timezone.utc
                ).astimezone().replace(
                    hour=0, minute=0, second=0, microsecond=0
                ).strftime("%Y-%m-%d")
                console.print(Markdown("`--date` has the wrong format.\n\n"
                    "Allowed format is:\n\n"
                    "`timeslime report --date=YYYY-MM-DD`\n\n"
                    "Example for today:\n\n"
                    f"`timeslime report --date={today}`"))
                return
            request_stop_date = request_start_date + timedelta(days=1)
            logging.debug("request_start_date: %s", request_start_date)
            logging.debug("request_stop_date: %s", request_stop_date)
        else:
            request_start_date = datetime.now(
                    timezone.utc
                ).astimezone().replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
            logging.debug("request_start_date: %s", request_start_date)

        table = Table(title="📊 timeslime report 📊", show_footer=True)

        table.add_column("🚀 Start Time", footer="Total")
        table.add_column("🛑 Stop Time")
        table.add_column("💪 Working time")

        output_format = "%H:%M:%S"
        if report_all:
            timespans = Timespan.select()
            output_format = "%Y-%m-%dT%H:%M:%S%z"
        else:
            if not request_stop_date:
                timespans = Timespan.select().where(
                    Timespan.start_time > request_start_date
                )
            else:
                timespans = Timespan.select().where(
                    Timespan.start_time >= request_start_date,
                    Timespan.start_time < request_stop_date,
                )

        # get configured time from today
        weekday = request_start_date.weekday()
        logging.debug("weekday: %s", weekday)
        if self._configuration_service.working_hours is None:
            target_working_time = timedelta()
        else:
            target_working_time = self._configuration_service.working_hours[
                weekday
            ]

        for timespan in timespans:
            if timespan.stop_time:
                report_timespan_sum += timespan.stop_time - timespan.start_time
                table.add_row(
                    timespan.start_time.strftime(output_format),
                    timespan.stop_time.strftime(output_format),
                    str(timespan.stop_time - timespan.start_time),
                )
            else:
                now_with_timezone = datetime.now(timezone.utc).astimezone()
                difference = now_with_timezone - timespan.start_time
                report_timespan_sum += difference
                table.add_row(timespan.start_time.strftime(output_format), "-", str(difference))

        remaining_working_hours = target_working_time - report_timespan_sum
        table.columns[2].footer = str(abs(remaining_working_hours))
        if remaining_working_hours.total_seconds() < 0:
            table.footer_style = "green"
            table.columns[2].footer = str(f"+ {abs(remaining_working_hours)}")

        console.print(table)
