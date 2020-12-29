#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Add default rows to fixed tables in database."""

import pokeschema


def add_types(session) -> None:
    session.add_all(
        [
            pokeschema.Type(type="normal"),
            pokeschema.Type(type="fighting"),
            pokeschema.Type(type="flying"),
            pokeschema.Type(type="poison"),
            pokeschema.Type(type="ground"),
            pokeschema.Type(type="rock"),
            pokeschema.Type(type="bug"),
            pokeschema.Type(type="ghost"),
            pokeschema.Type(type="steel"),
            pokeschema.Type(type="fire"),
            pokeschema.Type(type="water"),
            pokeschema.Type(type="grass"),
            pokeschema.Type(type="electric"),
            pokeschema.Type(type="psychic"),
            pokeschema.Type(type="ice"),
            pokeschema.Type(type="dragon"),
            pokeschema.Type(type="dark"),
            pokeschema.Type(type="???"),
        ]
    )


def add_egg_groups(session) -> None:
    session.add_all(
        [
            pokeschema.EggGroup(group="monster"),
            pokeschema.EggGroup(group="water 1"),
            pokeschema.EggGroup(group="bug"),
            pokeschema.EggGroup(group="flying"),
            pokeschema.EggGroup(group="field"),
            pokeschema.EggGroup(group="fairy"),
            pokeschema.EggGroup(group="grass"),
            pokeschema.EggGroup(group="human-like"),
            pokeschema.EggGroup(group="water 3"),
            pokeschema.EggGroup(group="mineral"),
            pokeschema.EggGroup(group="amorphous"),
            pokeschema.EggGroup(group="water 2"),
            pokeschema.EggGroup(group="ditto"),
            pokeschema.EggGroup(group="dragon"),
            pokeschema.EggGroup(group="undiscovered"),
        ]
    )


def add_damage_categories(session) -> None:
    session.add_all(
        [
            pokeschema.DamageCategory(category="physical"),
            pokeschema.DamageCategory(category="special"),
            pokeschema.DamageCategory(category="status"),
        ]
    )


def add_obtain_methods(session) -> None:
    session.add_all(
        [
            pokeschema.ObtainMethod(method="catch"),
            pokeschema.ObtainMethod(method="fish"),
            pokeschema.ObtainMethod(method="trade"),
            pokeschema.ObtainMethod(method="purchase"),
            pokeschema.ObtainMethod(method="gift"),
            pokeschema.ObtainMethod(method="hatch"),
            pokeschema.ObtainMethod(method="evolve"),
            pokeschema.ObtainMethod(method="find"),
        ]
    )


def add_evo_triggers(session) -> None:
    session.add_all(
        [
            pokeschema.EvoTrigger(trigger="level"),
            pokeschema.EvoTrigger(trigger="item"),
            pokeschema.EvoTrigger(trigger="trade"),
        ]
    )


def add_learn_methods(session) -> None:
    session.add_all(
        [
            pokeschema.LearnMethod(method="level"),
            pokeschema.LearnMethod(method="machine"),
            pokeschema.LearnMethod(method="egg"),
            pokeschema.LearnMethod(method="tutor"),
        ]
    )


if __name__ == "__main__":
    from sqlalchemy import create_engine  # type: ignore
    from sqlalchemy.orm import sessionmaker  # type: ignore

    engine = create_engine("sqlite:///poke.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        add_types(session)
        add_egg_groups(session)
        add_damage_categories(session)
        add_obtain_methods(session)
        add_evo_triggers(session)
        add_learn_methods(session)

        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
