# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Schema for Volume data.
"""

from marshmallow import fields
from sweetrpg_catalog_objects.model.volume import Volume
from sweetrpg_model_core.schema.base import BaseSchema


class VolumeSchema(BaseSchema):
    model_class = Volume

    title = fields.String(required=True)  # , load_only=True)
    description = fields.String(required=True)  # , load_only=True)
    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
    properties = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
    system_ids = fields.List(fields.String(required=True))  # , load_only=True)
    publisher_ids = fields.List(fields.String(required=True))
    studio_ids = fields.List(fields.String(required=True))
    license_ids = fields.List(fields.String(required=True))
