# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from datetime import datetime
from mongoengine import Document, fields
from pymongo import ASCENDING
from sweetrpg_catalog_objects.db.embedded.tag.document import TagDocument
from sweetrpg_catalog_objects.db.embedded.property.document import PropertyDocument


class PublisherDocument(Document):
    """A mapping object to convert MongoDB data to a Publisher object."""

    meta = {
        "indexes": [
            {"name": "publisher_name", "fields": ["name"]},
        ],
        "db_alias": "default",
        "collection": "publishers",
        "strict": False,
    }

    source_id = fields.StringField()

    # basic properties
    name = fields.StringField(min_length=1, max_length=200, required=True)
    address = fields.StringField(min_length=1, max_length=400)
    website = fields.StringField(min_length=1, max_length=100)
    notes = fields.StringField(min_length=1, max_length=1000)
    tags = fields.ListField(fields.EmbeddedDocumentField(TagDocument))
    properties = fields.ListField(fields.EmbeddedDocumentField(PropertyDocument))

    # relations

    # audit properties
    created_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    created_by = fields.StringField(default="system", required=True)
    updated_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    updated_by = fields.StringField(default="system", required=True)
    deleted_at = fields.DateTimeField(null=True)
    deleted_by = fields.StringField(null=True)
