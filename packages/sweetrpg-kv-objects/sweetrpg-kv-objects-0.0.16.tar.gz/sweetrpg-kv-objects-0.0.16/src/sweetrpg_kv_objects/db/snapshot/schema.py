# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Schema for Snapshot data.
"""

from marshmallow import fields
from sweetrpg_kv_objects.model.snapshot import Snapshot
from sweetrpg_model_core.schema.base import BaseSchema


class SnapshotSchema(BaseSchema):
    model_class = Snapshot

    store_id = fields.String(required=True)  # , load_only=True)

    name = fields.String(required=True)  # , load_only=True)

    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
    # value_ids = fields.List(fields.String(required=True))  # , load_only=True)
