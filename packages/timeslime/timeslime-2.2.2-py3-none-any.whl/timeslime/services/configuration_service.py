"""configuration service"""
from ast import literal_eval
from datetime import timedelta

from peewee import Database

from timeslime.models import Setting


class ConfigurationService():
    """class for the configuration service"""
    def __init__(self, database: Database):
        """create configuration service"""
        self._working_hours: list[timedelta] = []
        self._connection = database

        models = [Setting]
        self._connection.bind(models)
        self._connection.create_tables(models)

    def __str_to_timedelta(self, timedelta_string: str) -> timedelta:
        """convert string to timedelta"""
        timedelta_string_array = timedelta_string.split(':')
        return timedelta(
            hours=int(timedelta_string_array[0]),
            minutes=int(timedelta_string_array[1]),
            seconds=int(timedelta_string_array[2])
        )

    def _get_working_hours(self):
        setting = Setting.get_or_none(key="working_hours")
        if setting is None:
            return None

        self._working_hours = list(
            map(
                lambda item: self.__str_to_timedelta(item),
                literal_eval(setting.value)
            )
        )
        return self._working_hours

    def _set_working_hours(self, value: list[timedelta]):
        setting, _ = Setting.get_or_create(key="working_hours")
        setting.value = list(map(lambda item: str(item), value))
        setting.save()

        self._working_hours = value

    working_hours = property(
        fget=_get_working_hours,
        fset=_set_working_hours
    )

    def _get_timeslime_server(self):
        setting = Setting.get_or_none(key="timeslime_server")
        if setting is None:
            return None
        self._timeslime_server = setting.value
        return self._timeslime_server

    def _set_timeslime_server(self, value: str):
        setting, _ = Setting.get_or_create(key="timeslime_server")
        setting.value = value
        setting.save()

        self._working_hours = value

    timeslime_server = property(
        fget=_get_timeslime_server,
        fset=_set_timeslime_server
    )

    def _get_username(self):
        setting = Setting.get_or_none(key="username")
        if setting is None:
            return None
        self._timeslime_server = setting.value
        return self._timeslime_server

    def _set_username(self, value: str):
        setting, _ = Setting.get_or_create(key="username")
        setting.value = value
        setting.save()

        self._working_hours = value

    username = property(
        fget=_get_username,
        fset=_set_username
    )

    def _get_password(self):
        setting = Setting.get_or_none(key="password")
        if setting is None:
            return None
        self._timeslime_server = setting.value
        return self._timeslime_server

    def _set_password(self, value: str):
        setting, _ = Setting.get_or_create(key="password")
        setting.value = value
        setting.save()

        self._working_hours = value

    password = property(
        fget=_get_password,
        fset=_set_password
    )
