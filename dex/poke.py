#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Carry pokemon information and related methods.

Todo:
    Finish data implementation
    Determine necessary methods to include

Notes:
    Should this maybe take a number and init from db?

"""

class Pokemon:
    """Pokemon object for data consolidation."""

    def __init__(self, number: int):
        """Initialize values for pokemon object.

        Args:
            number: Dex number of pokemon to create

        """
        self.number = number
        self.weight: float
        self.height: float
        self.entry: str
        self.load_data()

    def load_data(self) -> None:
        """Load pokemon data from database."""
        pass
