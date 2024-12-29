from data.init import cur, IntegrityError
from model.creature import Creature
from typing import Tuple
from errors import Missing, Duplicate
from typing import Optional

CreatureRow = Tuple[str, str, str, str, str]


cur.execute(
    """CREATE TABLE IF NOT EXISTS creature(
                    name        TEXT    PRIMARY KEY,
                    description TEXT,
                    country     TEXT,
                    area        TEXT,
                    aka         TEXT
            )"""
)


def row_to_model(row: CreatureRow) -> Creature:
    name, description, country, area, aka = row
    return Creature(
        name=name,
        description=description,
        country=country,
        area=area,
        aka=aka,
    )


def model_to_dict(creature: Creature) -> dict[str, str]:
    return creature.model_dump()


def get_one(name: str) -> Creature:
    stmt: str = "SELECT * FROM creature WHERE name=:name;"
    params: dict[str, str] = {"name": name}
    cur.execute(stmt, params)
    row: CreatureRow = cur.fetchone()
    if row:
        return row_to_model(row)

    raise Missing(f"Creature `{name}` not found")


def get_all() -> list[Creature]:
    stmt: str = "SELECT * FROM creature"
    cur.execute(stmt)
    return [row_to_model(row) for row in cur]


def create(creature: Creature) -> Creature:
    stmt: str = (
        """
        INSERT INTO creature 
        VALUES(:name, :description, :country, :area, :aka)
        """
    )
    params: dict[str, str] = model_to_dict(creature)
    try:
        cur.execute(stmt, params)
    except IntegrityError:
        raise Duplicate(f"Creature `{creature.name}` already exist")
    return get_one(creature.name)


def modify(creature: Creature) -> Creature:
    return creature


def replace(creature: Creature) -> Creature:
    stmt = """UPDATE creature
                SET country=:country,
                    description=:description,
                    area=:area,
                    aka=:aka
                WHERE name=:name"""
    params = model_to_dict(creature)
    cur.execute(stmt, params)
    if not cur.rowcount == 1:
        raise Missing(f"Creature `{creature.name}` not found")
    return get_one(creature.name)


def delete(name: str):
    stmt: str = "DELETE FROM creature WHERE name=:name"
    params: dict[str, str] = {"name": name}
    cur.execute(stmt, params)
    if not cur.rowcount == 1:
        raise Missing(f"Creature `{name}` not found")
