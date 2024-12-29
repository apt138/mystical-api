from model.explorer import Explorer
from data import explorer as db


def get_all() -> list[Explorer]:
    return db.get_all()


def get_one(name: str) -> Explorer | None:
    return db.get_one(name)


def create(explorer: Explorer) -> Explorer:
    return db.create(explorer)


def modify(name: str, explorer: Explorer) -> Explorer:
    return db.modify(explorer)


def replace(name: str, explorer: Explorer) -> Explorer:
    return db.replace(explorer)


def delete(name: str) -> None:
    return db.delete(name)
