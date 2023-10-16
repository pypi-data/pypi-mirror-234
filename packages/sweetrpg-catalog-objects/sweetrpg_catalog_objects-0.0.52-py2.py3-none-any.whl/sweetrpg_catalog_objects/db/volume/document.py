# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Volume document for MongoDB.
"""

from datetime import datetime
from mongoengine import Document, fields
from sweetrpg_catalog_objects.db.embedded.property.document import PropertyDocument
from sweetrpg_catalog_objects.db.embedded.tag.document import TagDocument


class VolumeDocument(Document):
    """
    A mapping object to convert MongoDB data to a Volume object.
    """

    meta = {
        "indexes": [
            {"name": "volume_title", "fields": ["title"]},
        ],
        "db_alias": "default",
        "collection": "volumes",
        "strict": False,
    }

    source_id = fields.StringField()

    # basic properties
    title = fields.StringField(required=True)
    description = fields.StringField(required=True)
    properties = fields.ListField(fields.EmbeddedDocumentField(PropertyDocument))
    tags = fields.ListField(fields.EmbeddedDocumentField(TagDocument))
    systems = fields.ListField(fields.ReferenceField("SystemDocument"))
    publishers = fields.ListField(fields.ReferenceField("PublisherDocument"))
    studios = fields.ListField(fields.ReferenceField("StudioDocument"))
    licenses = fields.ListField(fields.ReferenceField("LicenseDocument"))

    # audit properties
    created_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    created_by = fields.StringField(default="system", required=True)
    updated_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    updated_by = fields.StringField(default="system", required=True)
    deleted_at = fields.DateTimeField(null=True)
    deleted_by = fields.StringField(default="system", required=True)
