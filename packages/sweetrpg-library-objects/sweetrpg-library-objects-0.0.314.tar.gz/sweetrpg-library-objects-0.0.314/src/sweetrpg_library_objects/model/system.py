# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

import logging
from sweetrpg_model_core.model.base import Model


class System(Model):
    """A model object representing an RPG game system."""

    def __init__(self, *args, **kwargs):
        """Creates a new System object.

        :key str name: The name of the system.
        """
        logging.debug("args: %s, kwargs: %s", args, kwargs)

        super().__init__(*args, **kwargs)

        self.game_system = kwargs.get("game_system")
        self.edition = kwargs.get("edition")
        self.tags = kwargs.get("tags")
