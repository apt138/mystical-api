from model.creature import Creature
from fake import creature as data


def get_all() -> list[Creature]:
    return data.get_all()


def get_one(name: str) -> Creature | None:
    return data.get_one(name)


def create(creature: Creature) -> Creature:
    return data.create(creature)


def modify(name: str, creature: Creature) -> Creature:
    return data.modify(creature)


def replace(name: str, creature: Creature) -> Creature:
    return data.replace(creature)


def delete(name: str) -> None:
    return data.delete(name)
