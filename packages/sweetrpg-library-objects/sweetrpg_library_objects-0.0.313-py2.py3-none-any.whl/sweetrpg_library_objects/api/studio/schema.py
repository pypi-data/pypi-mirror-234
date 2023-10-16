# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields
from sweetrpg_library_objects.model.studio import Studio
from sweetrpg_api_core.schema.base import BaseAPISchema


class StudioAPISchema(BaseAPISchema):
    model_class = Studio

    class Meta:
        type_ = "studio"
        self_view = "studio_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "studio_list"

    name = fields.String(required=True)  # , load_only=True)
    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
    properties = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
