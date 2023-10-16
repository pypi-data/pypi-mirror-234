# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields
from marshmallow import post_load
from sweetrpg_catalog_objects.model.contribution import Contribution
from sweetrpg_catalog_objects.utils.user import add_user_info
from sweetrpg_api_core.schema.base import BaseAPISchema


class ContributionAPISchema(BaseAPISchema):
    class Meta:
        type_ = "contribution"
        self_view = "contribution_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "contribution_list"

    @post_load
    def make_object(self, data, **kwargs):
        data = add_user_info(data)
        return Contribution(**data)

    id = fields.String()  # as_string=True, dump_only=True)
    person_id = fields.String(required=True)  # required=True) #, load_only=True)
    volume_id = fields.String(required=True)  # required=True) #, load_only=True)
    roles = fields.List(fields.String(required=True))  # required=True) #, load_only=True)
