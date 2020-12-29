#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Generate schema and sqlalchemy table mappings."""

from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore

# from sqlalchemy.ext.associationproxy import association_proxy  # type: ignore

Base = declarative_base()
NL = chr(10)
TAB = chr(9)
NLT = NL + TAB


class Pokemon(Base):  # type: ignore
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True)
    species = Column(String, nullable=False)
    classification = Column(String, nullable=False)
    type1_id = Column(Integer, ForeignKey("types.id"), nullable=False)
    type1 = relationship("Type", foreign_keys=[type1_id])
    type2_id = Column(Integer, ForeignKey("types.id"))
    type2 = relationship("Type", foreign_keys=[type2_id])
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    gender_ratio = Column(Float)
    egg1_id = Column(Integer, ForeignKey("egg_groups.id"), nullable=False)
    egg1 = relationship("EggGroup", foreign_keys=[egg1_id])
    egg2_id = Column(Integer, ForeignKey("egg_groups.id"))
    egg2 = relationship("EggGroup", foreign_keys=[egg2_id])
    legendary = Column(Boolean, default=False)
    evos = relationship(
        "Evolution",
        back_populates="pre_evo",
        primaryjoin="Pokemon.id==Evolution.pre_evo_id",
    )
    pre_evo = relationship(
        "Evolution",
        back_populates="evo",
        primaryjoin="Pokemon.id==Evolution.evo_id",
        uselist=False,
    )
    entries = relationship("Entry", back_populates="pokemon")
    moves = relationship("Learns", back_populates="pokemon")
    locations = relationship("PokemonObtain", back_populates="pokemon")

    def __repr__(self) -> str:
        return (
            f"<Pokemon(id='{self.id}',"
            f" species='{self.species}',"
            f" classification='{self.classification}',"
            f" type1_id='{self.type1_id}', type1='{self.type1}',"
            f" type2_id='{self.type2_id}', type2='{self.type2}',"
            f" height='{self.height}',"
            f" weight='{self.weight}',"
            f" gender_ratio='{self.gender_ratio}',"
            f" egg1_id='{self.egg1_id}', egg1='{self.egg1}',"
            f" egg2_id='{self.egg2_id}', egg2='{self.egg2}',"
            f" legendary='{self.legendary}',"
            f" evos='{self.evos}',"
            f" pre_evo='{self.pre_evo}',"
            f" entries='{self.entries}'"
            f" moves='{self.moves}',"
            f" locations='{self.locations}')>"
        )

    def __str__(self) -> str:
        return f"""Pokemon:
        ID:             {self.id:03d}
        Species:        {self.species.capitalize()}
        Classification: {self.classification.capitalize()}
        Type 1:         {str(self.type1)}
        Type 2:         {str(self.type2)}

        Height:         {self.height}
        Weight:         {self.weight}
        Gender Ratio:   {self.gender_ratio:.2%} Male
        Egg Group 1:    {str(self.egg1)}
        Egg Group 2:    {str(self.egg2)}

        Evolutions:
        {
        (TAB) + (NLT).join(
            sorted(
                [f'{evo.evo_id:03d}: {evo.evo.species}' for evo in self.evos]
            )
        )
        }
        Pre-Evolution:
        {(TAB) + self.pre_evo.pre_evo_id:03d}: {self.pre_evo.pre_evo.species}

        Entries:
        {(TAB) + (NLT).join([entry.entry for entry in self.entries])}

        Moves:
        {
        (TAB) + (NLT).join(
            [
            f'Method: {mv[1]}' + NLT + f'Level: {mv[2]}' + NLT + f'Move: {mv[3]}' + NL for mv in sorted(
                sorted(
                    [(move.method_id, move.method.method, move.level, move.move.name) for move in self.moves],
                    key=lambda move: move[2]
                ),
                key=lambda move: move[0]
            )
            ]
        )
        }

        Locations:
        {
        (TAB) + (NLT).join(
            [
            f'Location: {loc[1]}' + NLT + f'Method: {loc[3]}' + NL for loc in sorted(
                sorted(
                    [
                        (loc.location_id, loc.location.name, loc.method_id, loc.method.method)
                            for loc in self.locations
                    ],
                    key=lambda loc: loc[2]
                ),
                key=lambda loc: loc[0]
            )
            ]
        )
        }
        """


class Evolution(Base):  # type: ignore
    __tablename__ = "evolves"

    pre_evo_id = Column(Integer, ForeignKey("pokemon.id"), primary_key=True)
    pre_evo = relationship("Pokemon", foreign_keys=[pre_evo_id], back_populates="evos")
    evo_id = Column(Integer, ForeignKey("pokemon.id"), primary_key=True)
    evo = relationship("Pokemon", foreign_keys=[evo_id], back_populates="pre_evo")
    trigger_id = Column(Integer, ForeignKey("evolution_triggers.id"), nullable=False)
    trigger = relationship("EvoTrigger")
    level = Column(Integer)
    item_id = Column(Integer, ForeignKey("items.id"))
    item = relationship("Item")
    additional_reqs = Column(String)

    def __repr__(self) -> str:
        return (
            f"<Evolution(pre_evo_id='{self.pre_evo_id}', pre_evo='{self.pre_evo}',"
            f" evo_id='{self.evo_id}', evo='{self.evo}',"
            f" trigger_id='{self.trigger_id}', trigger='{self.trigger}',"
            f" level='{self.level}',"
            f" item_id='{self.item_id}', item='{self.item}',"
            f" additional_reqs='{self.additional_reqs}')>"
        )

    def __str__(self) -> str:
        return f"""Evolution:
        Pre Evolution ID:        {self.pre_evo_id:03d}
        Pre Evolution Species:   {self.pre_evo.species.capitalize()}

        Evolves Into

        Evolution ID:            {self.evo_id:03d}
        Evolution Species:       {self.evo.species.capitalize()}

        By

        Evolution Trigger:       {str(self.trigger)}
        Level Requirement:       {self.level}
        Item Requirement:        {self.item.name.capitalize()}

        Additional Requirements: {self.additional_reqs}
        """


class Learns(Base):  # type: ignore
    __tablename__ = "learns"

    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), primary_key=True)
    pokemon = relationship("Pokemon", back_populates="moves")
    move_id = Column(Integer, ForeignKey("moves.id"), primary_key=True)
    move = relationship("Move", back_populates="pokemon")
    method_id = Column(Integer, ForeignKey("learn_methods.id"), nullable=False)
    method = relationship("LearnMethod")
    level = Column(Integer)

    def __repr__(self) -> str:
        return (
            f"<Learns(pokemon_id='{self.pokemon_id}', pokemon='{self.pokemon}',"
            f" move_id='{self.move_id}', move='{self.move}',"
            f" method_id='{self.method_id}', method='{self.method}',"
            f" level='{self.level}')>"
        )

    def __str__(self) -> str:
        return f"""Move Learn:
        Pokemon ID:      {self.pokemon_id:03d}
        Pokemon Species: {self.pokemon.species.capitalize()}

        Learns:          {self.move.name.capitalize()}

        By Method:       {str(self.method)}
        Level:           {self.level}
        """


class Move(Base):  # type: ignore
    __tablename__ = "moves"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey("types.id"), nullable=False)
    type = relationship("Type")
    category_id = Column(Integer, ForeignKey("damage_categories.id"), nullable=False)
    category = relationship("DamageCategory")
    pp = Column(Integer)
    power = Column(Integer)
    accuracy = Column(Float)
    machine_id = Column(Integer, ForeignKey("items.id"))
    machine = relationship("Item")
    description = Column(String)
    pokemon = relationship("Learns", back_populates="move")

    def __repr__(self) -> str:
        return (
            f"<Move(id='{self.id}', name='{self.name}',"
            f" type_id='{self.type_id}', type='{self.type}',"
            f" category_id='{self.category_id}', category='{self.category}',"
            f" pp='{self.pp}',"
            f" power='{self.power}',"
            f" accuracy='{self.accuracy}',"
            f" machine_id='{self.machine_id}', machine='{self.machine}',"
            f" description='{self.description}',"
            f" pokemon='{self.pokemon}')>"
        )

    def __str__(self) -> str:
        return f"""Move:
        Name:        {self.name.capitalize()}
        Type:        {str(self.type)}
        Category:    {str(self.category)}
        PP:          {self.pp}
        Power:       {self.power}
        Accuracy:    {self.accuracy}
        Machine:     {self.machine.name.upper()}
        Description: {self.description.capitalize()}

        Learned By:
        {
        (TAB) + (NLT).join(
            sorted(
                [f'{poke.pokemon_id:03d}: {poke.pokemon.species}' for poke in self.pokemon]
            )
        )
        }
        """


class PokemonObtain(Base):  # type: ignore
    __tablename__ = "pokemon_obtained"

    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), primary_key=True)
    pokemon = relationship("Pokemon", back_populates="locations")
    location_id = Column(Integer, ForeignKey("locations.id"), primary_key=True)
    location = relationship("Location", back_populates="pokemon")
    method_id = Column(Integer, ForeignKey("obtain_methods.id"), nullable=False)
    method = relationship("ObtainMethod")

    def __repr__(self) -> str:
        return (
            f"<PokemonObtain(pokemon_id='{self.pokemon_id}', pokemon='{self.pokemon}',"
            f" location_id='{self.location_id}', location='{self.location}',"
            f" method_id='{self.method_id}', method='{self.method}')>"
        )

    def __str__(self) -> str:
        return f"""Pokemon Obtain:
        Pokemon ID:      {self.pokemon_id:03d}
        Pokemon Species: {self.pokemon.species.capitalize()}

        Is Obtained At:  {self.location.name.capitalize()}
        Method:          {str(self.method)}
        """


class ItemObtain(Base):  # type: ignore
    __tablename__ = "item_obtained"

    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    item = relationship("Item", back_populates="locations")
    location_id = Column(Integer, ForeignKey("locations.id"), primary_key=True)
    location = relationship("Location", back_populates="items")
    method_id = Column(Integer, ForeignKey("obtain_methods.id"), nullable=False)
    method = relationship("ObtainMethod")

    def __repr__(self) -> str:
        return (
            f"<ItemObtain(item_id='{self.item_id}', item='{self.item}',"
            f" location_id='{self.location_id}', location='{self.location}',"
            f" method_id='{self.method_id}', method='{self.method}')>"
        )

    def __str__(self) -> str:
        return f"""Item Obtain:
        Item:           {self.item.name.capitalize()}

        Is Obtained At: {self.location.name.capitalize()}
        Method:         {str(self.method)}
        """


class Location(Base):  # type: ignore
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    pokemon = relationship("PokemonObtain", back_populates="location")
    items = relationship("ItemObtain", back_populates="location")

    def __repr__(self) -> str:
        return f"<Location(id='{self.id}', name='{self.name}', pokemon='{self.pokemon}', items='{self.items}')>"

    def __str__(self) -> str:
        return f"""Location:
        Name:            {self.name.capitalize()}

        Pokemon Listing:
        {
        (TAB) + (NLT).join(
            [
            f'Method: {poke[1]}' + NLT + f'{poke[2]:03d}: {poke[3]}' + NL for poke in sorted(
                sorted(
                    [(pk.method_id, pk.method.method, pk.pokemon_id, pk.pokemon.species) for pk in self.pokemon],
                    key=lambda pk: pk[2]
                ),
                key=lambda pk: pk[0]
            )
            ]
        )
        }


        Item Listing:
        {
        (TAB) + (NLT).join(
            [
            f'Method: {item[1]}' + NLT + f'Item: {item[3]}' + NL for item in sorted(
                sorted(
                    [(item.method_id, item.method.method, item.item_id, item.item.name) for item in self.items],
                    key=lambda it: it[2]
                ),
                key=lambda it: it[0]
            )
            ]
        )
        }
        """


class Entry(Base):  # type: ignore
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"))
    pokemon = relationship("Pokemon", back_populates="entries")
    entry = Column(String)

    def __repr__(self) -> str:
        return (
            f"<Entry(id='{self.id}',"
            f" pokemon_id='{self.pokemon_id}', pokemon='{self.pokemon.species}',"
            f" entry='{self.entry}')>"
        )

    def __str__(self) -> str:
        return f"""Dex Entry:
        Pokemon ID:      {self.pokemon_id:03d}
        Pokemon Species: {self.pokemon.species.capitalize()}
        Entry:           {self.entry.capitalize()}
        """


class Item(Base):  # type: ignore
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    purchase_price = Column(Integer)
    sale_price = Column(Integer)
    description = Column(String)
    locations = relationship("ItemObtain", back_populates="item")

    def __repr__(self) -> str:
        return (
            f"<Item(id='{self.id}', name='{self.name}',"
            f" purchase_price='{self.purchase_price}',"
            f" sale_price='{self.sale_price}',"
            f" description='{self.description}',"
            f" locations='{self.locations}')>"
        )

    def __str__(self) -> str:
        return f"""Item:
        Name:           {self.name.capitalize()}
        Purchase Price: {self.purchase_price:n}
        Sale Price:     {self.sale_price:n}
        Description:    {self.description.capitalize()}

        Locations:
        {
        (TAB) + (NLT).join(
            [
            f'Location: {loc[1]}' + NLT + f'Method: {loc[3]}' + NL for loc in sorted(
                sorted(
                    [(loc.method_id, loc.method.method, loc.location_id, loc.location.name) for loc in self.locations],
                    key=lambda loc: loc[0]
                ),
                key=lambda loc: loc[2]
            )
            ]
        )
        }
        """


class Type(Base):  # type: ignore
    __tablename__ = "types"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<Type(id='{self.id}', type='{self.type}')>"

    def __str__(self) -> str:
        return self.type.capitalize()


class EggGroup(Base):  # type: ignore
    __tablename__ = "egg_groups"

    id = Column(Integer, primary_key=True)
    group = Column(String, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<EggGroup(id='{self.id}', group='{self.group}')>"

    def __str__(self) -> str:
        return self.group.capitalize()


class DamageCategory(Base):  # type: ignore
    __tablename__ = "damage_categories"

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<DamageCategory(id='{self.id}', category='{self.category}')>"

    def __str__(self) -> str:
        return self.category.capitalize()


class ObtainMethod(Base):  # type: ignore
    __tablename__ = "obtain_methods"

    id = Column(Integer, primary_key=True)
    method = Column(String, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<ObtainMethod(id='{self.id}', method='{self.method}')>"

    def __str__(self) -> str:
        return self.method.capitalize()


class EvoTrigger(Base):  # type: ignore
    __tablename__ = "evolution_triggers"

    id = Column(Integer, primary_key=True)
    trigger = Column(String, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<EvoMethod(id='{self.id}', trigger='{self.trigger}')>"

    def __str__(self) -> str:
        return self.trigger.capitalize()


class LearnMethod(Base):  # type: ignore
    __tablename__ = "learn_methods"

    id = Column(Integer, primary_key=True)
    method = Column(String, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<LearnMethod(id='{self.id}', method='{self.method}')>"

    def __str__(self) -> str:
        return self.method.capitalize()


if __name__ == "__main__":
    from sqlalchemy import create_engine

    engine = create_engine("sqlite:///poke.db", echo=True)
    Base.metadata.create_all(engine)
