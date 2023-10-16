# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from marshmallow import fields
from sweetrpg_library_objects.model.embedded.property import Property
from sweetrpg_model_core.schema.base import BaseEmbeddedSchema


class AuthorPropertySchema(BaseEmbeddedSchema):
    model_class = Property

    name = fields.String(required=True)  # , load_only=True)
    value = fields.String(required=True)  # , load_only=True)
    kind = fields.String(allow_none=True)  # , load_only=True)
