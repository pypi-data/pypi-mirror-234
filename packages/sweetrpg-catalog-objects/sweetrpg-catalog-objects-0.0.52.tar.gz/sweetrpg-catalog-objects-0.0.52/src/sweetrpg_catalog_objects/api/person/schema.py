# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields
from marshmallow import post_load
from sweetrpg_catalog_objects.model.person import Person
from sweetrpg_catalog_objects.utils.user import add_user_info
from sweetrpg_api_core.schema.base import BaseAPISchema


class PersonAPISchema(BaseAPISchema):
    class Meta:
        type_ = "person"
        self_view = "person_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "person_list"

    @post_load
    def make_object(self, data, **kwargs):
        data = add_user_info(data)
        return Person(**data)

    id = fields.String()  # as_string=True, dump_only=True)
    name = fields.String(required=True)  # required=True) #, load_only=True)
    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
    properties = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
