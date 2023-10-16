# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from datetime import datetime
from mongoengine import Document, fields
from sweetrpg_catalog_objects.db.embedded.property.document import PropertyDocument
from sweetrpg_catalog_objects.db.embedded.tag.document import TagDocument


class LicenseDocument(Document):
    """A mapping object to convert MongoDB data to a License object."""

    meta = {
        "indexes": [
            {"name": "license_title", "fields": ["title"]},
        ],
        "db_alias": "default",
        "collection": "licenses",
        "strict": False,
    }

    source_id = fields.StringField()

    # basic properties
    title = fields.StringField(required=True)
    short_title = fields.StringField(required=True)
    version = fields.StringField()
    deed = fields.StringField()
    legal_code = fields.StringField()
    url = fields.StringField()
    status = fields.StringField(required=True)
    availability = fields.StringField(required=True)
    release_date = fields.DateField()
    revocation_date = fields.DateField()
    notes = fields.StringField()
    properties = fields.ListField(fields.EmbeddedDocumentField(PropertyDocument))
    tags = fields.ListField(fields.EmbeddedDocumentField(TagDocument))
    volumes = fields.ListField(fields.ReferenceField("VolumeDocument"))

    # audit properties
    created_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    created_by = fields.StringField(default="system", required=True)
    updated_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    updated_by = fields.StringField(default="system", required=True)
    deleted_at = fields.DateTimeField(null=True)
    deleted_by = fields.StringField(default="system", required=True)
