# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Schema for Value data.
"""

from marshmallow import fields
from sweetrpg_kv_objects.model.value import Value
from sweetrpg_model_core.schema.base import BaseSchema


class ValueSchema(BaseSchema):
    model_class = Value

    store_id = fields.String(required=True)  # , load_only=True)
    key_id = fields.String(required=True)  # , load_only=True)
    snapshot_id = fields.String(required=True)  # , load_only=True)

    value = fields.String(required=True)  # , load_only=True)

    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
