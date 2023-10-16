# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from datetime import datetime
from mongoengine import Document, fields
from pymongo import ASCENDING


class ContributionDocument(Document):
    """A model object representing an RPG contribution."""

    meta = {
        "indexes": [
            # {"name": "contribution_name", "fields": ["name"]},
            {"name": "person_volume_unique", "fields": ["person_id", "volume_id"], "unique": True}
        ],
        "db_alias": "default",
        "collection": "contributions",
        "strict": False,
    }

    # basic properties
    roles = fields.ListField(fields.StringField(required=True), required=True)

    # relations
    person_id = fields.StringField(min_length=1, max_length=30, required=True)
    volume_id = fields.StringField(min_length=1, max_length=30, required=True)

    # audit properties
    created_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    created_by = fields.StringField(default="system", required=True)
    updated_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    updated_by = fields.StringField(default="system", required=True)
    deleted_at = fields.DateTimeField(null=True)
    deleted_by = fields.StringField(null=True)
