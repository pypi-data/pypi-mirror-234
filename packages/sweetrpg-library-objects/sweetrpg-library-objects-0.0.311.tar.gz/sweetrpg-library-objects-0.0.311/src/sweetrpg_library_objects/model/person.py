# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

import logging
from sweetrpg_model_core.model.base import Model


class Person(Model):
    """A model object representing RPG contributors."""

    def __init__(self, *args, **kwargs):
        """Creates a new Person object.

        :key str name: The name of the person.
        """
        logging.debug("args: %s, kwargs: %s", args, kwargs)
        print(kwargs)  # TODO: remove

        super().__init__(*args, **kwargs)

        self.name = kwargs.get("name")
        self.properties = kwargs.get("properties")
        self.tags = kwargs.get("tags")
