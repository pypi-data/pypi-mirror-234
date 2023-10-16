# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship
from sweetrpg_api_core.schema.base import BaseAPISchema
from sweetrpg_catalog_objects.model.license import License


class LicenseAPISchema(BaseAPISchema):
    model_class = License

    class Meta:
        type_ = "license"
        self_view = "license_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "license_list"

    title = fields.String(required=True)  # , load_only=True)
    short_title = fields.String(required=True)  # , load_only=True)
    version = fields.String(required=True)  # , load_only=True)
    deed = fields.String()  # , load_only=True)
    legal_code = fields.String()  # , load_only=True)
    url = fields.String()  # , load_only=True)
    status = fields.String(required=True)  # , load_only=True)
    availability = fields.String(required=True)  # , load_only=True)
    release_date = fields.Date()  # , load_only=True)
    revocation_date = fields.Date()  # , load_only=True)
    notes = fields.String()  # , load_only=True)
    properties = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
    volume_ids = fields.List(fields.String(required=True))  # , load_only=True)
