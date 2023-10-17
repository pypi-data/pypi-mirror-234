"""collection of data models"""
from datetime import datetime, timezone
from uuid import uuid4

from peewee import DateTimeField, Model, TextField, UUIDField

DateTimeField.formats = [
    "%Y-%m-%d %H:%M:%S.%f%z",
    "%Y-%m-%d %H:%M:%S%z",
]


# pylint: disable=too-few-public-methods
class Setting(Model):
    """setting model"""
    id = UUIDField(primary_key=True, default=uuid4)
    key = TextField(index=True, null=True)
    value = TextField(null=True)

    class Meta:
        """defines meta information"""
        table_name = "settings"

class Timespan(Model):
    """timespan model"""
    id = UUIDField(primary_key=True, default=uuid4)
    start_time = DateTimeField(null=True)
    stop_time = DateTimeField(null=True)
    updated_at = DateTimeField(
        default=lambda: datetime.now(tz=timezone.utc), null=False
    )

    class Meta:
        """defines meta information"""
        table_name = "timespans"


class State(Model):
    """state model"""
    key = TextField(primary_key=True)
    value = TextField(null=True)

    class Meta:
        """defines meta information"""
        table_name = "state"
