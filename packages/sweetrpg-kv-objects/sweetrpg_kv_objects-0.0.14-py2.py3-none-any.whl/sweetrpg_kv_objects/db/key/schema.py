# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Schema for Key data.
"""

from marshmallow import fields
from sweetrpg_kv_objects.model.key import Key
from sweetrpg_model_core.schema.base import BaseSchema


class KeySchema(BaseSchema):
    model_class = Key

    store_id = fields.String(required=True)

    name = fields.String(required=True)  # , load_only=True)
    description = fields.String(required=True)  # , load_only=True)

    type = fields.String(required=True)  # , load_only=True)
    encoding = fields.String(required=True)  # , load_only=True)
    expression = fields.String(required=True)  # , load_only=True)

    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
    # value_ids = fields.List(fields.String(required=True))  # , load_only=True)
