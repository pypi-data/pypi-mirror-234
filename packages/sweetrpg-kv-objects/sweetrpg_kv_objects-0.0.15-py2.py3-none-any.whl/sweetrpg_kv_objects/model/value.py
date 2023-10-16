# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

import logging
from sweetrpg_model_core.model.base import Model


class Value(Model):
    """A model object representing a key-value store value."""

    def __init__(self, *args, **kwargs):
        """Creates a new Value object."""
        logging.debug("args: %s, kwargs: %s", args, kwargs)

        super().__init__(*args, **kwargs)

        self.store_id = kwargs.get("store_id")
        self.key_id = kwargs.get("key_id")
        self.snapshot_id = kwargs.get("snapshot_id")

        self.value = kwargs.get("value")

        self.tags = kwargs.get("tags")
