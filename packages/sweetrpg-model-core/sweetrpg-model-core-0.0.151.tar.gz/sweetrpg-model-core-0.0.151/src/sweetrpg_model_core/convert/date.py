# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Date conversion functions.
"""

from datetime import datetime, timezone
from bson.timestamp import Timestamp
import logging


def to_datetime(value, tz=None, attr=None, data=None, **kwargs):
    """Deserializes a database value to a Python datetime.
    This function can be used as a callback for the Marshmallow :class:`fields.Function`
    field type.

    :param any value: The source value to convert to a Python datetime object. This can
        be a MongoDB :class:`bson.timestamp.Timestamp`, an ISO-formatted date/time
        string, or a UTC unix timestamp value.
    :param str attr: The name of the attribute being deserialized.
    :param object data: The object associated.
    :param dict kwargs:
    :return datetime.datetime: Python datetime object
    """
    logging.debug("to_datetime: value (parameter): %s", value)

    if value is None:
        logging.debug("to_datetime: None")
        return None
    elif isinstance(value, Timestamp):
        logging.debug("to_datetime: Timestamp: %s", value)
        value = value.as_datetime().timestamp()
    elif isinstance(value, datetime):
        logging.debug("to_datetime: datetime: %s", value)
        return value
    elif isinstance(value, str):
        logging.debug("to_datetime: str: %s", value)
        value = datetime.fromisoformat(value)
        return value
    elif isinstance(value, dict):
        logging.debug("to_datetime: dict: %s", value)
        if isinstance(value["$date"], str):
            logging.debug("to_datetime: value[$date]: %s", value["$date"])
            try:
                value = datetime.fromisoformat(value["$date"])
            except ValueError:
                value = datetime.strptime(value["$date"], "%Y-%M-%dT%H:%M:%S.%fZ")
            return value
        value = value["$date"] / 1000

    logging.debug("value (converted?): %s", value)
    return datetime.fromtimestamp(float(value), tz)


def to_timestamp(value, attr=None, obj=None, **kwargs):
    """Serialize an object value to a MongoDB timestamp.
    This function can be used as a callback for the Marshmallow :class:`fields.Function`
    field type.

    :param any value: The source value to convert to a MongoDB :class:`bson.timestamp.Timestamp`. This
                      can be a `datetime` object, or a time/increment tuple.
    :param str attr: The name of the attribute being serialized.
    :param object obj: The object associated.
    :param dict kwargs:
    :return bson.timestamp.Timestamp: MongoDB Timestamp object
    """
    logging.debug("to_timestamp: value (parameter): %s", value)

    if value is None:
        logging.debug("to_timestamp: None")
        return None
    if isinstance(value, datetime):
        logging.debug("to_timestamp: datetime")
        return Timestamp(value, 0)

    logging.debug("value (converted?): %s", value)
    return Timestamp(int(value), 0)
