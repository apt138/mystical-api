from model.creature import Creature
from data import creature as db


def get_all() -> list[Creature]:
    return db.get_all()


def get_one(name: str) -> Creature | None:
    return db.get_one(name)


def create(creature: Creature) -> Creature:
    return db.create(creature)


def modify(name: str, creature: Creature) -> Creature:
    return db.modify(creature)


def replace(name: str, creature: Creature) -> Creature:
    return db.replace(creature)


def delete(name: str) -> None:
    return db.delete(name)
