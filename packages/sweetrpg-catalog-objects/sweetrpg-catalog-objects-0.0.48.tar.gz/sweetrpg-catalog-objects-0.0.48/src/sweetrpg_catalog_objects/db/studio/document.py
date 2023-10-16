# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from datetime import datetime
from mongoengine import Document, fields
from sweetrpg_catalog_objects.db.embedded.tag.document import TagDocument
from sweetrpg_catalog_objects.db.embedded.property.document import PropertyDocument


class StudioDocument(Document):
    """A mapping object to convert MongoDB data to a Studio object."""

    meta = {
        "indexes": [
            {"name": "studio_name", "fields": ["name"]},
        ],
        "db_alias": "default",
        "collection": "studios",
        "strict": False,
    }

    source_id = fields.StringField()

    # basic properties
    name = fields.StringField(min_length=1, max_length=200, required=True)
    website = fields.StringField()
    notes = fields.StringField()
    tags = fields.ListField(fields.EmbeddedDocumentField(TagDocument))
    properties = fields.ListField(fields.EmbeddedDocumentField(PropertyDocument))

    # relations

    # audit properties
    created_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    created_by = fields.StringField(default="system", required=True)
    updated_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    updated_by = fields.StringField(default="system", required=True)
    deleted_at = fields.DateTimeField(null=True)
    deleted_by = fields.StringField(default="system", required=True)
