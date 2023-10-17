"""synchronize service"""
from datetime import datetime, timezone
import logging
from typing import Optional
from urllib.parse import urljoin
from uuid import UUID

from peewee import Database
from requests import Session
from rich.console import Console

from timeslime.models import Setting, State, Timespan
from timeslime.services.configuration_service import ConfigurationService

class SynchronizeService():
    """class synchronize service"""
    def __init__(
            self,
            database: Database,
            configuration_service: ConfigurationService
        ):
        """create synchronize service"""
        self._connection = database
        self._configuration_service = configuration_service

        models = [Setting, State, Timespan]
        self._connection.bind(models)
        self._connection.create_tables(models)

        self.server_url = self._configuration_service.timeslime_server
        if not self.server_url:
            logging.error("Timeslime server is not configured!")

        self.timespan_route = urljoin(self.server_url, "api/v1/timespans")
        self.setting_route = urljoin(self.server_url, "api/v1/settings")

        self.session = Session()
        self.session.auth = (
            self._configuration_service.username,
            self._configuration_service.password
        )


    def sync(self, date: Optional[str] = None):
        """synchronize all data
        :param date: define since when the data should be synchronized"""
        console = Console()
        logging.info("Start synchronization")

        from_date = date
        if date is None:
            time_sync_date = State.get_or_none(key="time_sync_date")
            if not time_sync_date or from_date == "2000-01-01":
                from_date = datetime.now(
                        timezone.utc
                    ).astimezone().replace(
                        hour=0, minute=0, second=0, microsecond=0
                    ).strftime("%Y-%m-%d")
            else:
                from_date = time_sync_date.value

        response_json = self.__get_all_measurements(from_date)
        for measurement in response_json["data"]:
            start_time = None
            stop_time = None
            updated_at = None
            if "start_time" in measurement and measurement["start_time"] is not None:
                start_time = datetime.fromisoformat(measurement["start_time"])
            if "stop_time" in measurement and measurement["stop_time"] is not None:
                stop_time = datetime.fromisoformat(measurement["stop_time"])
            if "updated_at" in measurement and measurement["updated_at"] is not None:
                updated_at = datetime.fromisoformat(measurement["updated_at"])

            logging.debug("check if id: %s exists, if not add data", measurement["id"])
            timespan, created = Timespan.get_or_create(id=measurement["id"])
            if created:
                timespan.start_time = start_time
                timespan.stop_time = stop_time
                timespan.updated_at = updated_at
                timespan.save()
                logging.debug("Create timespan object: %s", timespan.id)
                continue

            logging.debug("check if data is newer on server, if yes update data")
            if timespan.updated_at < updated_at:
                timespan.start_time = start_time
                timespan.stop_time = stop_time
                timespan.updated_at = updated_at
                timespan.save()
                logging.debug("Update local timespan object: %s", timespan.id)
                continue

            logging.debug("check if data is newer local and send data to server")
            if timespan.updated_at != updated_at:
                logging.debug("Update remote timespan object: %s", timespan.id)
                self.__send_measurement(timespan)

        timespans = Timespan.select().where(
            Timespan.start_time > from_date
        )
        for timespan in timespans:
            remote_timespan = list(filter(lambda element: UUID(element["id"]) == timespan.id, response_json["data"]))
            if not remote_timespan:
                logging.info("Timespan object: %s is not on the server", timespan.id)
                self.__send_measurement(timespan)

        if from_date != "2000-01-01":
            time_sync_date, _ = State.get_or_create(key="time_sync_date")
            if time_sync_date.value != from_date:
                time_sync_date.value = from_date
                time_sync_date.save()
        logging.info("Finished synchronization")
        console.print("🤝 successfully synchronized your time and configuration data 🤝")

    def __get_all_measurements(self, from_date: str):
        """get all measurements from server"""

        logging.info("Get all data which are newer than date: %s", from_date)
        response = self.session.get(
            self.timespan_route,
            params={
                "from": from_date
            }
        )
        response.raise_for_status()

        response_json = response.json()
        logging.info("Received %s measurements", len(response_json["data"]))

        return response_json

    def __send_measurement(self, timespan: Timespan):
        """send measurement to server"""
        logging.info("Send timespan object to server: %s", timespan.id)
        start_time_str = None
        if timespan.start_time:
            start_time_str = str(timespan.start_time)

        stop_time_str = None
        if timespan.stop_time:
            stop_time_str = str(timespan.stop_time)

        response = self.session.post(self.timespan_route, json={
                "id": str(timespan.id),
                "start_time": start_time_str,
                "stop_time": stop_time_str,
                "updated_at": str(timespan.updated_at),
            }
        )
        response.raise_for_status()
