# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow import fields
from sweetrpg_catalog_objects.model.license import License
from sweetrpg_model_core.schema.base import BaseSchema


class LicenseSchema(BaseSchema):
    model_class = License

    title = fields.String(required=True)  # , load_only=True)
    short_title = fields.String(required=True)  # , load_only=True)
    version = fields.String()  # , load_only=True)
    deed = fields.String()  # , load_only=True)
    legal_code = fields.String()  # , load_only=True)
    url = fields.String()  # , load_only=True)
    status = fields.String(required=True)  # , load_only=True)
    availability = fields.String(required=True)  # , load_only=True)
    release_date = fields.Date()  # , load_only=True)
    revocation_date = fields.Date()  # , load_only=True)
    notes = fields.String()  # , load_only=True)
    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
    properties = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
    volume_ids = fields.List(fields.String(required=True))  # , load_only=True)
