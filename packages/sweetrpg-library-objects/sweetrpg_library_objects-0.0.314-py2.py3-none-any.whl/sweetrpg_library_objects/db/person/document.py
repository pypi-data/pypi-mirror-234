# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from datetime import datetime
from mongoengine import Document, fields
from sweetrpg_library_objects.db.embedded.property.document import PropertyDocument
from sweetrpg_library_objects.db.embedded.tag.document import TagDocument


class PersonDocument(Document):
    """A model object representing a person contributing to an RPG."""

    meta = {
        "indexes": [{"name": "person_name", "fields": ["name"]}],
        "db_alias": "default",
        "collection": "persons",
        "strict": False,
    }

    # basic properties
    name = fields.StringField(min_length=1, max_length=200, required=True)
    properties = fields.ListField(fields.EmbeddedDocumentField(PropertyDocument))
    tags = fields.ListField(fields.EmbeddedDocumentField(TagDocument))

    # relations

    # audit properties
    created_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    created_by = fields.StringField(default="system", required=True)
    updated_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    updated_by = fields.StringField(default="system", required=True)
    deleted_at = fields.DateTimeField(null=True)
    deleted_by = fields.StringField(null=True)
