# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow import fields
from sweetrpg_library_objects.model.license import License
from sweetrpg_model_core.schema.base import BaseSchema


class LicenseSchema(BaseSchema):
    model_class = License

    title = fields.String(required=True)  # , load_only=True)
    description = fields.String(required=True)  # , load_only=True)
    body = fields.String(required=True)  # , load_only=True)
    tags = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
    properties = fields.List(fields.Dict(keys=fields.String(required=True), values=fields.String()))
    volume_ids = fields.List(fields.String(required=True))  # , load_only=True)
