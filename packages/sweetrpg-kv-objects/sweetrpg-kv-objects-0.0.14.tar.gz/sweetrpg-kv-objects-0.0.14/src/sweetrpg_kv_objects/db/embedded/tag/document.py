# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from datetime import datetime
from mongoengine import EmbeddedDocument, fields


class TagDocument(EmbeddedDocument):
    """A mapping object to convert MongoDB data to a Tag object."""

    # basic properties
    name = fields.StringField(min_length=1, max_length=50, required=True)
    value = fields.StringField(max_length=50)
