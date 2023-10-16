# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Base objects for model and embedded model.
"""

from reprlib import recursive_repr
import logging
from datetime import datetime
from sweetrpg_model_core.convert.date import to_datetime


class BaseModel(object):
    """A base model with common methods for model types.

    Do not subclass this; use `Model` or `EmbeddedModel` instead.
    """

    @recursive_repr()
    def __repr__(self):
        attrs = []
        for k, v in self.__dict__.items():
            if k.startswith("__") or k.startswith("to_"):
                continue
            # v = getattr(self, k)
            attrs.append("{k}={v}".format(k=k, v=v))
        return f'<{self.__class__.__name__}({", ".join(attrs)})>'

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the model object.

        Returns:
            dict: A Python dictionary.
        """
        d = {}
        for k, v in self.__dict__.items():
            logging.debug("k: %s, type: %s, v: %s", k, type(k), v)
            if k.startswith("__") or k.startswith("to_"):
                continue
            d[k] = v  # getattr(self, k)
        return d


class SimpleModel(BaseModel):
    """
    A simple model object which includes an 'id' property.
    """

    def __init__(self, *args, **kwargs):
        """Create a simple model object."""
        logging.debug("args: %s, kwargs: %s", args, kwargs)

        self.id = kwargs.get("_id") or kwargs.get("id")
        logging.debug("id: %s", self.id)


class Model(BaseModel):
    """A model object which includes an 'id' property as well as
    audit fields for created, updated, and deleted times.
    """

    def __init__(self, *args, **kwargs):
        """Create a base model object."""
        logging.debug("args: %s, kwargs: %s", args, kwargs)
        now = datetime.utcnow()  # .isoformat()

        self.id = kwargs.get("_id") or kwargs.get("id")
        logging.debug("id: %s", self.id)
        self.created_at = to_datetime(kwargs.get("created_at")) or now
        logging.debug("created_at: %s", self.created_at)
        self.created_by = kwargs["created_by"]
        logging.debug("created_by: %s", self.created_by)
        self.updated_at = to_datetime(kwargs.get("updated_at")) or now
        logging.debug("updated_at: %s", self.updated_at)
        self.updated_by = kwargs["updated_by"]
        logging.debug("updated_by: %s", self.updated_by)
        self.deleted_at = to_datetime(kwargs.get("deleted_at"))
        logging.debug("deleted_at: %s", self.deleted_at)
        self.deleted_by = kwargs.get("deleted_by")
        logging.debug("deleted_by: %s", self.deleted_by)


class EmbeddedModel(BaseModel):
    """An embedded model object, meant to be contained in another model object. It does not
    contain an identifier or audit fields.
    """

    def __init__(self, *args, **kwargs):
        """Create a base model object."""
        logging.debug("args: %s, kwargs: %s", args, kwargs)
