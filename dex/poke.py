#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Carry pokemon information and related methods.

Todo:
    Finish data implementation
    Determine necessary methods to include

Notes:
    Should this maybe take a number and init from db?

"""

from typing import Dict, Tuple, List
from PIL import Image  # type: ignore
import logging
import db.pokeschema as pokeschema


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

    def __init__(self, id: int, session):
        """Initialize values for pokemon object.

        Args:
            number: National dex number of pokemon to create

        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Pokemon({id})")
        self.id = id
        self.species: str
        self.classification: str
        self.height: float
        self.weight: float
        self.entries: List[str] = []
        self.sprites: List[Image.Image] = []
        self.footprint: Image.Image
        self.load_images()
        self.load_data(session)

    def __repr__(self) -> str:
        return f"Pokemon({self.id})"

    def load_images(self) -> None:
        """Load sprites and footprint from spritesheet."""
        sprite_sheet = Image.open(f"assets/sprites/{self.id:03d}.png")
        self.sprites.append(sprite_sheet.crop((0, 0, 56, 56)))
        self.sprites.append(sprite_sheet.crop((0, 56, 56, 112)))
        self.footprint = sprite_sheet.crop((0, 112, 16, 128))

    def load_data(self, session) -> None:
        """Load pokemon data from database."""
        # load from DB based on ID
        mon = session.query(pokeschema.Pokemon).filter_by(id=self.id).first()
        self.species = mon.species
        self.classification = mon.classification
        self.height = mon.height
        self.weight = mon.weight
        for entry in mon.entries:
            self.entries.append(entry.entry)
        # self.species = "Magikarp"
        # self.classification = "Fish"
        # self.height = 0.9
        # self.weight = 10.0
        # entry = (
        #     "For no reason, it jumps and splashes about, making it "
        #     "easy for predators like Pidgeotto to catch it mid-jump."
        # )
        # self.entries = {(2, 2): entry}
