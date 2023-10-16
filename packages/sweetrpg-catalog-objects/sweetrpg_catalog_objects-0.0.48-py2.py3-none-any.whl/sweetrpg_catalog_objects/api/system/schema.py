# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields
from sweetrpg_catalog_objects.model.system import System
from sweetrpg_api_core.schema.base import BaseAPISchema


class SystemAPISchema(BaseAPISchema):
    model_class = System

    class Meta:
        type_ = "system"
        self_view = "system_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "system_list"

    game_system = fields.String(required=True)  # , load_only=True)
    name = fields.String(required=True)
    edition = fields.String(required=True)
    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
