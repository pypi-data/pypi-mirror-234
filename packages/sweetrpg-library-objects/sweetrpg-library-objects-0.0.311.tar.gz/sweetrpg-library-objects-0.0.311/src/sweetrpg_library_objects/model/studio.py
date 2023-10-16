# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

import logging
from sweetrpg_model_core.model.base import Model


class Studio(Model):
    """A model object representing RPG studios."""

    def __init__(self, *args, **kwargs):
        """Creates a new Studio object.

        :key str name: The name of the studio.
        """
        logging.debug("args: %s, kwargs: %s", args, kwargs)

        super().__init__(*args, **kwargs)

        self.name = kwargs.get("name")
        self.tags = kwargs.get("tags")
        self.properties = kwargs.get("properties")
