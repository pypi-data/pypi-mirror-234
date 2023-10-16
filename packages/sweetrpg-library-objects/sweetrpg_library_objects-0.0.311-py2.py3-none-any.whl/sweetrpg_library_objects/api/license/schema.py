# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship
from sweetrpg_api_core.schema.base import BaseAPISchema
from sweetrpg_library_objects.model.license import License


class LicenseAPISchema(BaseAPISchema):
    model_class = License

    class Meta:
        type_ = "license"
        self_view = "license_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "license_list"

    title = fields.String(required=True)  # , load_only=True)
    description = fields.String(required=True)  # , load_only=True)
    body = fields.String(required=True)  # , load_only=True)
    properties = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
    volume_ids = fields.List(fields.String(required=True))  # , load_only=True)
