# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

import logging
from sweetrpg_model_core.model.base import Model


class Volume(Model):
    """A model object representing an RPG volume (digital or print)."""

    def __init__(self, *args, **kwargs):
        """Creates a new Volume object."""
        logging.debug("args: %s, kwargs: %s", args, kwargs)

        super().__init__(*args, **kwargs)

        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.properties = kwargs.get("properties")
        self.tags = kwargs.get("tags")
        self.system_ids = kwargs.get("system_ids")
        self.publisher_ids = kwargs.get("publisher_ids")
        self.studio_ids = kwargs.get("studio_ids")
        self.license_ids = kwargs.get("license_ids")
