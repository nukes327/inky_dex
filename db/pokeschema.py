#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Generate schema and sqlalchemy table mappings.

Todo:
    Sqlite doesn't support enums, need to write tables instead for these as well.

"""

from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey  # type: ignore
from sqlalchemy.orm import relationship, aliased  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore

# from sqlalchemy.ext.associationproxy import association_proxy  # type: ignore

Base = declarative_base()


class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True)
    species = Column(String, nullable=False)
    classification = Column(String, nullable=False)
    type1_id = Column(Integer, ForeignKey("types.id"), nullable=False)
    type1 = relationship("Type", foreign_keys=[type1_id])
    type2_id = Column(Integer, ForeignKey("types.id"))
    type2 = relationship("Type", foreign_keys=[type2_id])
    moves = relationship("Learns", back_populates="pokemon")
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
    locations = relationship("Obtain", back_populates="pokemon")
    entries = relationship("Entry", back_populates="pokemon")

    def __repr__(self):
        return f"""<Pokemon(id='{self.id}', species='{self.species}', classification='{self.classification}',
        type1_id='{self.type1_id}', type1='{self.type1}',
        type2_id='{self.type2_id}', type2='{self.type2}',
        moves='{self.moves}',
        height='{self.height}', weight='{self.weight}', gender_ratio='{self.gender_ratio}',
        egg1_id='{self.egg1_id}', egg1='{self.egg1}',
        egg2_id='{self.egg2_id}', egg2='{self.egg2}',
        legendary='{self.legendary}',
        evos='{self.evos}',
        pre_evo='{self.pre_evo}'
        locations='{self.locations}',
        entries='{self.entries}')>"""


class Evolution(Base):
    __tablename__ = "evolves"

    pre_evo_id = Column(Integer, ForeignKey("pokemon.id"), primary_key=True)
    evo_id = Column(Integer, ForeignKey("pokemon.id"), primary_key=True)
    pre_evo = relationship("Pokemon", foreign_keys=[pre_evo_id], back_populates="evos")
    evo = relationship("Pokemon", foreign_keys=[evo_id], back_populates="pre_evo")
    trigger_id = Column(Integer, ForeignKey("evolution_triggers.id"), nullable=False)
    trigger = relationship("EvoTrigger")
    level = Column(Integer)
    item_id = Column(Integer, ForeignKey("items.id"))
    item = relationship("Item")
    additional_reqs = Column(String)

    def __repr__(self):
        return f"""<Evolution(pre_evo_id='{self.pre_evo_id}', pre_evo='{self.pre_evo.species}',
        evo_id='{self.evo_id}', evo='{self.evo.species}',
        trigger_id='{self.trigger_id}', trigger='{self.trigger}',
        level='{self.level}', item_id='{self.item_id}', item='{self.item}',
        additional_reqs='{self.additional_reqs}')>"""


class Learns(Base):
    __tablename__ = "learns"

    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), primary_key=True)
    pokemon = relationship("Pokemon", back_populates="moves")
    move_id = Column(Integer, ForeignKey("moves.id"), primary_key=True)
    move = relationship("Move", back_populates="pokemon")
    method_id = Column(Integer, ForeignKey("learn_methods.id"), nullable=False)
    method = relationship("LearnMethod")
    level = Column(Integer)

    def __repr__(self):
        return f"""<Learns(pokemon_id='{self.pokemon_id}', pokemon='{self.pokemon.species}',
        move_id='{self.move_id}', move='{self.move.name}',
        method_id='{self.method_id}', method='{self.method}',
        level='{self.level}')>"""


class Move(Base):
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

    def __repr__(self):
        return f"""<Move(id='{self.id}', name='{self.name}',
        type_id='{self.type_id}', type='{self.type}',
        category_id='{self.category_id}', category='{self.category}',
        pp='{self.pp}', power='{self.power}', accuracy='{self.accuracy}',
        machine_id='{self.machine_id}', machine='{self.machine}',
        description='{self.description}',
        pokemon='{self.pokemon}')>"""


class Obtain(Base):
    __tablename__ = "obtained"

    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), primary_key=True)
    pokemon = relationship("Pokemon", back_populates="locations")
    location_id = Column(Integer, ForeignKey("locations.id"), primary_key=True)
    location = relationship("Location", back_populates="pokemon")
    method_id = Column(Integer, ForeignKey("obtain_methods.id"), nullable=False)
    method = relationship("ObtainMethod")

    def __repr__(self):
        return f"""<Obtain(pokemon_id='{self.pokemon_id}', pokemon='{self.pokemon.species}',
        location_id='{self.location_id}', location='{self.location.name}',
        method_id='{self.method_id}', method='{self.method}')>"""


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    pokemon = relationship("Obtain", back_populates="location")

    def __repr__(self):
        return f"""<Location(id='{self.id}', name='{self.name}',
        pokemon='{self.pokemon}')>"""


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"))
    pokemon = relationship("Pokemon", back_populates="entries")
    entry = Column(String)

    def __repr__(self):
        return f"""<Entry(id='{self.id}', pokemon_id='{self.pokemon_id}', pokemon='{self.pokemon.species}',
        entry='{self.entry}')>"""


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    purchase_price = Column(Integer)
    sale_price = Column(Integer)
    location_id = Column(Integer, ForeignKey("locations.id"))
    location = relationship("Location")

    def __repr__(self):
        return f"""<Item(id='{self.id}', name='{self.name}',
        description='{self.description}',
        purchase_price='{self.purchase_price}', sale_price='{self.sale_price}',
        location_id='{self.location_id}', location='{self.location.name}')>"""


class Type(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<Type(id='{self.id}', type='{self.type}')>"


class EggGroup(Base):
    __tablename__ = "egg_groups"

    id = Column(Integer, primary_key=True)
    group = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<EggGroup(id='{self.id}', group='{self.group}')>"


class DamageCategory(Base):
    __tablename__ = "damage_categories"

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<DamageCategory(id='{self.id}', category='{self.category}')>"


class ObtainMethod(Base):
    __tablename__ = "obtain_methods"

    id = Column(Integer, primary_key=True)
    method = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<ObtainMethod(id='{self.id}', method='{self.method}')>"


class EvoTrigger(Base):
    __tablename__ = "evolution_triggers"

    id = Column(Integer, primary_key=True)
    trigger = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<EvoMethod(id='{self.id}', trigger='{self.trigger}')>"


class LearnMethod(Base):
    __tablename__ = "learn_methods"

    id = Column(Integer, primary_key=True)
    method = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<LearnMethod(id='{self.id}', method='{self.method}')>"


if __name__ == "__main__":
    from sqlalchemy import create_engine

    engine = create_engine("sqlite:///poke.db", echo=True)
    Base.metadata.create_all(engine)
