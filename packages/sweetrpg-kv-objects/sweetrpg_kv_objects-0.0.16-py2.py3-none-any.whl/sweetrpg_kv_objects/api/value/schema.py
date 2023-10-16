# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship
from sweetrpg_api_core.schema.base import BaseAPISchema
from sweetrpg_kv_objects.model.value import Value


class ValueAPISchema(BaseAPISchema):
    model_class = Value

    class Meta:
        type_ = "value"
        self_view = "value_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "value_list"

    store_id = fields.String(required=True)  # , load_only=True)
    key_id = fields.String(required=True)  # , load_only=True)
    snapshot_id = fields.String(required=True)  # , load_only=True)

    value = fields.String(required=True)  # , load_only=True)

    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
