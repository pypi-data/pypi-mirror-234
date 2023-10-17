"""time service"""
from datetime import datetime, timezone
import logging
from peewee import Database
from rich.console import Console
from rich.markdown import Markdown

from timeslime.models import Timespan

CONSOLE = Console()

class TimeService:
    """class for the time service"""
    def __init__(self, database: Database):
        """create configuration service"""
        self._connection = database

        models = [Timespan]
        self._connection.bind(models)
        self._connection.create_tables(models)
        self.current_timespan: Timespan = Timespan.select().where(
            Timespan.stop_time.is_null()
        ).get_or_none()

    def start(self, start_time: str):
        """start time"""
        now_with_timezone = self.__get_time(start_time)
        if self.current_timespan is None:
            self.current_timespan, _ = Timespan.get_or_create(start_time=now_with_timezone)
            self.current_timespan.updated_at = now_with_timezone
            self.current_timespan.save()
        else:
            CONSOLE.print("🛑 stop your time 🛑")
            logging.info("🛑 stop your time 🛑")
            self.current_timespan.stop_time = now_with_timezone
            self.current_timespan.updated_at = now_with_timezone
            self.current_timespan.save()
            self.current_timespan = Timespan.create(start_time=now_with_timezone)
            self.current_timespan.save()
        CONSOLE.print(Markdown("🚀 start your time 🚀\n\n"
            "Execute the following, if you are finished with your work or take a break:\n\n"
            "`timeslime stop`")
        )
        logging.info("🚀 start your time 🚀")

    def stop(self, stop_time: str):
        """stop time"""
        now_with_timezone = self.__get_time(stop_time)
        if self.current_timespan is None:
            CONSOLE.print(Markdown("🚀 execute `timeslime start` before stop 🛑"))
            logging.info("🚀 start your time before stop 🛑")
            return

        CONSOLE.print(Markdown("🛑 stop your time 🛑\n\n"
            "Execute the following, if you are starting with your work again:\n\n"
            "`timeslime start`\n\n"
            "Execute the following, if you want the time report of today:\n\n"
            "`timeslime report`\n\n")
        )
        logging.info("🛑 stop your time 🛑")
        self.current_timespan.stop_time = now_with_timezone
        self.current_timespan.updated_at = now_with_timezone
        self.current_timespan.save()

    def __get_time(self, time_str: str = ""):
        """get time"""
        now_with_timezone = datetime.now(timezone.utc).astimezone()
        if not time_str:
            return now_with_timezone

        try:
            requested_time = datetime.strptime(time_str, "%H:%M")
            now_with_timezone = now_with_timezone.replace(
                hour=requested_time.hour,
                minute=requested_time.minute,
                second=0,
                microsecond=0,

            )

            return now_with_timezone
        except ValueError as value_error:
            raise ValueError(
                "Time must be in the format HH:mm (eg. 8:00)!"
            ) from value_error
