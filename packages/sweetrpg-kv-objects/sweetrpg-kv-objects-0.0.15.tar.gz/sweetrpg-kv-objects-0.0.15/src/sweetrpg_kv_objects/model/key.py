# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

import logging
from sweetrpg_model_core.model.base import Model


class Key(Model):
    """A model object representing a key-value store key."""

    def __init__(self, *args, **kwargs):
        """Creates a new Key object."""
        logging.debug("args: %s, kwargs: %s", args, kwargs)

        super().__init__(*args, **kwargs)

        self.store_id = kwargs.get("store_id")

        self.name = kwargs.get("name")
        self.description = kwargs.get("description")

        self.type = kwargs.get("type")
        self.encoding = kwargs.get("encoding")
        self.expression = kwargs.get("expression")

        self.tags = kwargs.get("tags")
        # self.value_ids = kwargs.get("value_ids")
