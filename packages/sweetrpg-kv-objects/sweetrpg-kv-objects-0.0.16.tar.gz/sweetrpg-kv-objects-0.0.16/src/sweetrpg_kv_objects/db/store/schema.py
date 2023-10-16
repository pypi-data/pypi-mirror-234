# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Schema for Store data.
"""

from marshmallow import fields
from sweetrpg_kv_objects.model.store import Store
from sweetrpg_model_core.schema.base import BaseSchema


class StoreSchema(BaseSchema):
    model_class = Store

    name = fields.String(required=True)  # , load_only=True)
    description = fields.String(required=True)  # , load_only=True)

    # key_ids = fields.List(fields.String(required=True))  # , load_only=True)
    # snapshot_ids = fields.List(fields.String(required=True))  # , load_only=True)
    current_snapshot_id = fields.String(required=True)  # , load_only=True)

    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
