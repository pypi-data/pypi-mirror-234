# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Base schema for model classes.
"""

from marshmallow import Schema, fields, EXCLUDE
from marshmallow import pre_load
from marshmallow import post_load
from datetime import datetime
import logging


class BaseSchema(Schema):
    """Base type for schema classes.
    Inherit from this type for database schema objects to gain ID and date conversion
    pre-load functionality, and to have ID and audit fields setup automatically.
    """

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def handle_id(self, in_data, **kwargs):
        """Converts _id into id"""
        in_data["id"] = in_data.get("_id") or in_data.get("id")
        return in_data

    @pre_load
    def handle_dates(self, in_data, **kwargs):
        """Converts date/time value to an ISO formatted string."""
        for k in ["created_at", "updated_at", "deleted_at"]:
            if isinstance(in_data.get(k), datetime):
                in_data[k] = in_data[k].isoformat()
        return in_data

    @post_load
    def make_object(self, data, **kwargs):
        """Create a model object from the provided data.

        :param data: A dictionary of data to populate the model object.
        :returns: An instance of the `model_class`.
        """
        logging.info("data: %s, kwargs: %s", data, kwargs)
        print(data, kwargs)  # TODO: remove
        return self.model_class(**data)

    id = fields.Str()  # as_string=True, dump_only=True)
    created_at = fields.DateTime(required=True)
    created_by = fields.String(required=True)
    updated_at = fields.DateTime(required=True)
    updated_by = fields.String(required=True)
    deleted_at = fields.DateTime(allow_none=True)
    deleted_by = fields.String(allow_none=True)


class BaseEmbeddedSchema(Schema):
    """Base schema for embedded objects."""

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs):
        """ """
        logging.info("data: %s", data)
        return self.model_class(**data)
