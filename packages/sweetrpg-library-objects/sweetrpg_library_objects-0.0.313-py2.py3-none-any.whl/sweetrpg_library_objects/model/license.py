# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

import logging
from sweetrpg_model_core.model.base import Model


class License(Model):
    """A model object representing an RPG license."""

    def __init__(self, *args, **kwargs):
        """Creates a new License object."""
        logging.debug("args: %s, kwargs: %s", args, kwargs)

        super().__init__(*args, **kwargs)

        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.body = kwargs.get("body")
        self.properties = kwargs.get("properties")
        self.tags = kwargs.get("tags")
        self.volume_ids = kwargs.get("volume_ids")
