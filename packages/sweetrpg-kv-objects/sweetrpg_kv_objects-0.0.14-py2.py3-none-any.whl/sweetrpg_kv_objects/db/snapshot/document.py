# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Snapshot document for MongoDB.
"""

from datetime import datetime
from mongoengine import Document, fields
from sweetrpg_kv_objects.db.embedded.property.document import PropertyDocument
from sweetrpg_kv_objects.db.embedded.tag.document import TagDocument


class SnapshotDocument(Document):
    """
    A mapping object to convert MongoDB data to a Snapshot object.
    """

    meta = {
        "indexes": [
            {"name": "snapshot_name", "fields": ["name"]},
        ],
        "db_alias": "default",
        "collection": "snapshots",
        "strict": False,
    }

    # references
    store_id = fields.ReferenceField("StoreDocument")

    # basic properties
    name = fields.StringField(required=True)
    tags = fields.ListField(fields.EmbeddedDocumentField(TagDocument))
    # values = fields.ListField(fields.ReferenceField("ValueDocument"))

    # audit properties
    created_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    created_by = fields.StringField(default="system", required=True)
    updated_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    updated_by = fields.StringField(default="system", required=True)
    deleted_at = fields.DateTimeField(null=True)
    deleted_by = fields.StringField(null=True)
