# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship
from sweetrpg_api_core.schema.base import BaseAPISchema
from sweetrpg_kv_objects.model.key import Key


class KeyAPISchema(BaseAPISchema):
    model_class = Key

    class Meta:
        type_ = "key"
        self_view = "key_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "key_list"

    store_id = fields.String(required=True)  # , load_only=True)

    name = fields.String(required=True)  # , load_only=True)
    description = fields.String(required=True)  # , load_only=True)

    # value_ids = fields.List(fields.String(required=True))  # , load_only=True)
    type = fields.String(required=True)  # , load_only=True)
    encoding = fields.String(required=True)  # , load_only=True)
    expression = fields.String(required=False)  # , load_only=True)

    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
