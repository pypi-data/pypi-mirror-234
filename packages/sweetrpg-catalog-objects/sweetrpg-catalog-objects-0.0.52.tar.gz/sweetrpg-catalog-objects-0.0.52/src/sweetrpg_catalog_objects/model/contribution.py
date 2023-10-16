# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

import logging
from sweetrpg_model_core.model.base import Model


class Contribution(Model):
    """A model object representing contributions to an RPG volume contribution."""

    def __init__(self, *args, **kwargs):
        """Creates a new Contribution object.

        :key str person_id: The identifier of the contributor.
        :key list roles: A list of role values indicating the contributions.
        """
        logging.debug("args: %s, kwargs: %s", args, kwargs)
        print(kwargs)  # TODO: remove

        super().__init__(*args, **kwargs)

        self.person_id = kwargs.get("person_id")
        self.volume_id = kwargs.get("volume_id")
        self.roles = kwargs.get("roles")
