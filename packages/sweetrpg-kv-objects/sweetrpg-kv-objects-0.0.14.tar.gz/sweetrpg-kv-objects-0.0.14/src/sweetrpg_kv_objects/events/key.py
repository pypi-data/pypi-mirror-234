# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

import logging
from datetime import datetime
from sweetrpg_model_core.model.base import SimpleModel
from sweetrpg_model_core.convert.date import to_datetime


class KeyEvent(SimpleModel):
    """A model object representing an event on store's key."""

    def __init__(self, *args, **kwargs):
        """Creates a new Key object."""
        logging.debug("args: %s, kwargs: %s", args, kwargs)
        now = datetime.utcnow()  # .isoformat()

        super().__init__(*args, **kwargs)

        self.store = kwargs.get("store")  # the store where the event occurred
        self.event = kwargs.get("event")  # the event that occurred
        self.key = kwargs.get("key")  # the key whose value changed
        self.occurred_at = to_datetime(kwargs.get("occurred_at")) or now  # the date/time the event occurred
