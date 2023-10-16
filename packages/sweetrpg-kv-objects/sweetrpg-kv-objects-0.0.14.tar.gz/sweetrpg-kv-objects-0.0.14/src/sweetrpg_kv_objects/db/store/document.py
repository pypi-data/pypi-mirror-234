# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Store document for MongoDB.
"""

from datetime import datetime
from mongoengine import Document, fields
from sweetrpg_kv_objects.db.embedded.property.document import PropertyDocument
from sweetrpg_kv_objects.db.embedded.tag.document import TagDocument


class StoreDocument(Document):
    """
    A mapping object to convert MongoDB data to a Store object.
    """

    meta = {
        "indexes": [
            {"name": "store_name", "fields": ["name"]},
        ],
        "db_alias": "default",
        "collection": "stores",
        "strict": False,
    }

    # basic properties
    name = fields.StringField(required=True)
    description = fields.StringField(required=True)
    current_snapshot = fields.ReferenceField("SnapshotDocument")

    # other properties
    tags = fields.ListField(fields.EmbeddedDocumentField(TagDocument))
    # keys = fields.ListField(fields.ReferenceField("KeyDocument"))
    # snapshots = fields.ListField(fields.ReferenceField("SnapshotDocument"))

    # audit properties
    created_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    created_by = fields.StringField(default="system", required=True)
    updated_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    updated_by = fields.StringField(default="system", required=True)
    deleted_at = fields.DateTimeField(null=True)
    deleted_by = fields.StringField(null=True)
