# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow import fields
from sweetrpg_catalog_objects.model.system import System
from sweetrpg_model_core.schema.base import BaseSchema


class SystemSchema(BaseSchema):
    model_class = System

    game_system = fields.String(required=True)  # , load_only=True)
    name = fields.String(required=True)  # , load_only=True)
    edition = fields.String(required=True)  # , load_only=True)
    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
