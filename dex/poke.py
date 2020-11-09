#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Carry pokemon information and related methods.

Todo:
    Finish data implementation
    Determine necessary methods to include

Notes:
    Should this maybe take a number and init from db?

"""

from typing import Dict, Tuple


class Pokemon:
    """Pokemon object for data consolidation.

    Attributes:
        number (int): National dex id for pokemon
        species (str): Species (often seen as name) of pokemon
        classification (str): How the dex classifies species, i.e. mouse pokemon pikachu
        weight (float): Weight in kg
        height (float): Height in meters
        entries (dict of tuple/str pairs): All dex entries compiled for species
            Tuple is (gen, ver)

    """

    def __init__(self, number: int):
        """Initialize values for pokemon object.

        Args:
            number: National dex number of pokemon to create

        """
        self.number = number
        self.species: str
        self.classification: str
        self.weight: float
        self.height: float
        self.entries: Dict[Tuple[int, int], str]
        self.load_data()

    def load_data(self) -> None:
        """Load pokemon data from database."""
        pass
