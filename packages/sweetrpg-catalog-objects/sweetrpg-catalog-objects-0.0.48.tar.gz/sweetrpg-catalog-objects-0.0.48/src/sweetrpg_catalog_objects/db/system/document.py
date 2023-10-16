# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from datetime import datetime
from mongoengine import Document, fields
from sweetrpg_catalog_objects.db.embedded.tag.document import TagDocument


class SystemDocument(Document):
    """A mapping object to convert MongoDB data to a System object."""

    meta = {
        "indexes": [
            # {"name": "game_system_edition", "fields": ["game_system", "edition"], "unique": True},
            {"name": "game_system", "fields": ["game_system"], "unique": True},
        ],
        "db_alias": "default",
        "collection": "systems",
        "strict": False,
    }

    source_id = fields.StringField()

    # basic properties
    game_system = fields.StringField(required=True)
    name = fields.StringField(required=True)
    edition = fields.StringField(required=True)
    tags = fields.ListField(fields.EmbeddedDocumentField(TagDocument))

    # relations

    # audit properties
    created_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    created_by = fields.StringField(default="system", required=True)
    updated_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    updated_by = fields.StringField(default="system", required=True)
    deleted_at = fields.DateTimeField(null=True)
    deleted_by = fields.StringField(default="system", required=True)
