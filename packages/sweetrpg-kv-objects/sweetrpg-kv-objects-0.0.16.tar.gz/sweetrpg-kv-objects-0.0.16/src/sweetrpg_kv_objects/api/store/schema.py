# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship
from sweetrpg_api_core.schema.base import BaseAPISchema
from sweetrpg_kv_objects.model.store import Store


class StoreAPISchema(BaseAPISchema):
    model_class = Store

    class Meta:
        type_ = "store"
        self_view = "store_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "store_list"

    name = fields.String(required=True)  # , load_only=True)
    description = fields.String(required=True)  # , load_only=True)

    # key_ids = fields.List(fields.String(required=True))  # , load_only=True)
    # snapshot_ids = fields.List(fields.String(required=True))  # , load_only=True)
    current_snapshot_id = fields.String(required=True)  # , load_only=True)

    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
