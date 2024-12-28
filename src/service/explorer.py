from ..model.explorer import Explorer
from ..fake import explorer as data


def get_all() -> list[Explorer]:
    return data.get_all()


def get_one(name: str) -> Explorer | None:
    return data.get_one(name)


def create(explorer: Explorer) -> Explorer:
    return data.create(explorer)


def modify(name: str, explorer: Explorer) -> Explorer:
    return data.modify(explorer)


def replace(name: str, explorer: Explorer) -> Explorer:
    return data.replace(explorer)


def delete(name: str) -> None:
    return data.delete(name)
