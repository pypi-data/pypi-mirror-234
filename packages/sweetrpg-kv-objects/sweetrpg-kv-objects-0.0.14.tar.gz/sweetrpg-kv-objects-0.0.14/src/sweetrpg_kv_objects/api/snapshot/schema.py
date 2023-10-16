# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship
from sweetrpg_api_core.schema.base import BaseAPISchema
from sweetrpg_kv_objects.model.snapshot import Snapshot


class SnapshotAPISchema(BaseAPISchema):
    model_class = Snapshot

    class Meta:
        type_ = "snapshot"
        self_view = "snapshot_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "snapshot_list"

    store_id = fields.String(required=True)  # , load_only=True)

    name = fields.String(required=True)  # , load_only=True)

    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
    # value_ids = fields.List(fields.String(required=True))  # , load_only=True)
