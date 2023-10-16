# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow import fields
from sweetrpg_catalog_objects.model.contribution import Contribution
from sweetrpg_model_core.schema.base import BaseSchema


class ContributionSchema(BaseSchema):
    model_class = Contribution

    person_id = fields.String(required=True)  # , load_only=True)
    volume_id = fields.String(required=True)
    roles = fields.List(fields.String(required=True))
