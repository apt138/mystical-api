from data.init import cur, IntegrityError
from model.explorer import Explorer
from typing import Tuple, Optional
from errors import Missing, Duplicate

ExplorerRow = Tuple[str, str, str]

cur.execute(
    """CREATE TABLE IF NOT EXISTS explorer(
                    name        TEXT    PRIMARY KEY,
                    country     TEXT,
                    description TEXT          
            )"""
)


def row_to_model(row: ExplorerRow) -> Explorer:
    name, country, description = row
    return Explorer(
        name=name,
        country=country,
        description=description,
    )


def model_to_dict(explorer: Explorer) -> dict[str, str]:
    return explorer.model_dump()


def get_all() -> list[Explorer]:
    stmt: str = "SELECT * FROM explorer;"
    cur.execute(stmt)
    return [row_to_model(row) for row in cur]


def get_one(name: str) -> Optional[Explorer]:
    stmt: str = """SELECT * FROM explorer
                WHERE name=:name;"""
    params: dict[str, str] = {"name": name}
    cur.execute(stmt, params)
    row = cur.fetchone()
    if not row:
        raise Missing(f"Explorer `{name}` not found")
    return row_to_model(row)


def create(explorer: Explorer) -> Explorer:
    stmt: str = """INSERT INTO explorer
                    VALUES (:name, :country, :description);"""
    params: dict[str, str] = model_to_dict(explorer)
    try:
        cur.execute(stmt, params)
    except IntegrityError:
        raise Duplicate(f"Explorer `{explorer.name}` already exists")
    return get_one(explorer.name)


def replace(explorer: Explorer) -> Explorer:
    stmt: str = """UPDATE explorer
                    SET country=:country,
                        description=:description
                    WHERE name=:name;"""
    params: dict[str, str] = model_to_dict(explorer)
    cur.execute(stmt, params)
    if not cur.rowcount == 1:
        raise Missing(f"Explorer `{explorer.name}` not found")
    return get_one(explorer.name)


def modify(explorer: Explorer) -> Explorer:
    return explorer


def delete(name: str) -> None:
    stmt: str = "DELETE FROM explorer WHERE name=:name;"
    params: dict[str, str] = {"name": name}
    cur.execute(stmt, params)
    if not cur.rowcount == 1:
        raise Missing(f"Explorer `{name}` not found")
