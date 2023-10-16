# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship
from sweetrpg_api_core.schema.base import BaseAPISchema
from sweetrpg_library_objects.model.volume import Volume


class VolumeAPISchema(BaseAPISchema):
    model_class = Volume

    class Meta:
        type_ = "volume"
        self_view = "volume_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "volume_list"

    title = fields.String(required=True)  # , load_only=True)
    description = fields.String(required=True)  # , load_only=True)
    slug = fields.String(required=True)  # , load_only=True)
    properties = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
    system_ids = fields.List(fields.String(required=True))  # , load_only=True)
    publisher_ids = fields.List(fields.String(required=True))  # , load_only=True)
    studio_ids = fields.List(fields.String(required=True))  # , load_only=True)
    license_ids = fields.List(fields.String(required=True))  # , load_only=True)
