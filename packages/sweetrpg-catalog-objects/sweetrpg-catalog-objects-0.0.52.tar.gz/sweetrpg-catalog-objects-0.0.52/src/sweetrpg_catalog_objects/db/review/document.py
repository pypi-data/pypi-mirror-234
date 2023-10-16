# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from datetime import datetime
from mongoengine import Document, fields
from sweetrpg_catalog_objects.db.embedded.tag.document import TagDocument


class ReviewDocument(Document):
    """A mapping object to convert MongoDB data to a Review object."""

    meta = {
        "indexes": [
            {"name": "review_title", "fields": ["title"]},
        ],
        "db_alias": "default",
        "collection": "reviews",
        "strict": False,
    }

    source_id = fields.StringField()

    # basic properties
    title = fields.StringField(required=True)
    body = fields.StringField(required=True)
    language = fields.StringField(required=True, default="en_US")
    tags = fields.ListField(fields.EmbeddedDocumentField(TagDocument))

    # relations
    volume_id = fields.StringField(required=True)

    # audit properties
    created_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    created_by = fields.StringField(default="system", required=True)
    updated_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    updated_by = fields.StringField(default="system", required=True)
    deleted_at = fields.DateTimeField(null=True)
    deleted_by = fields.StringField(default="system", required=True)
