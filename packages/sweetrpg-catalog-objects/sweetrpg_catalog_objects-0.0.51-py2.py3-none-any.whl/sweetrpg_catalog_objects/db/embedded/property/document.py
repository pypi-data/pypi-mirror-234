# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from mongoengine import EmbeddedDocument, fields


class PropertyDocument(EmbeddedDocument):
    """A mapping object for properties."""

    # basic properties
    name = fields.StringField(min_length=1, max_length=50, required=True)
    value = fields.StringField(min_length=2, max_length=200, required=True)
    kind = fields.StringField(min_length=1, max_length=20, required=True)
