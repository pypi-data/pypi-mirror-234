# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Document conversion functions.
"""

import logging
import json
from .date import to_datetime
from sweetrpg_model_core.model.base import BaseModel
from typing import Optional


def convert_document_property_value(value):
    """Convert a property value from "document" format to a "normal" value, e.g., a MongoDB object ID
    (a dict with key '$oid') would be converted to just the ID value.

    :param any value: The value to convert
    :returns any: The converted value
    """
    if isinstance(value, list):
        new_values = []
        for v in value:
            new_values.append(convert_document_property_value(v))
        return new_values
    if isinstance(value, dict):
        if value.get("$oid"):
            return value.get("$oid")
        elif value.get("$date"):
            return to_datetime(value)

    return value


def to_model(doc, model_class) -> Optional[BaseModel]:
    """Convert a database document to a model instance.

    :param Document doc: The input document to convert. This instance must have a to_json() function
        that returns a dictionary of the document data.
    :param class model_class: The type of model class to convert to. This class must accept kwargs
        in its initializer.
    :returns: An instance of the model class, initialized with the document data.
    """
    logging.debug("doc: %s, model_class: %s", doc, model_class)
    if not hasattr(doc, "to_json"):
        return None
    data = doc.to_json()
    logging.debug("data: %s", data)
    if isinstance(data, str):
        logging.debug("converting data from str to dict")
        data = json.loads(data)
    logging.debug("data: %s", data)
    for k, v in data.items():
        data[k] = convert_document_property_value(v)
    logging.debug("converted data: %s", data)
    model = model_class(**data)
    logging.debug("model: %s", model)

    return model
