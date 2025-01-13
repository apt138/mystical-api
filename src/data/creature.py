from data.init import Session
from data.model import Creature as DBCreature
from model.creature import Creature
from typing import Tuple
from errors import Missing, Duplicate
from typing import Optional
from sqlalchemy.exc import IntegrityError


CreatureRow = Tuple[str, str, str, str, str]


def row_to_model(row: CreatureRow | DBCreature) -> Creature:
    if isinstance(row, DBCreature):
        name = row.name
        description = row.description
        country = row.country
        area = row.area
        aka = row.aka
    else:
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
    # stmt: str = "SELECT * FROM creature WHERE name=:name;"
    # params: dict[str, str] = {"name": name}
    # cur.execute(stmt, params)
    # row: CreatureRow = cur.fetchone()
    with Session() as sess:
        row = sess.query(DBCreature).filter(DBCreature.name == name).first()
        if row:
            return row_to_model(row)

        raise Missing(f"Creature `{name}` not found")


def get_all() -> list[Creature]:
    # stmt: str = "SELECT * FROM creature"
    # cur.execute(stmt)
    with Session() as sess:
        rows = sess.query(DBCreature).all()
        return [row_to_model(row) for row in rows]


def create(creature: Creature) -> Creature:
    # stmt: str = (
    #     """
    #     INSERT INTO creature
    #     VALUES(:name, :description, :country, :area, :aka)
    #     """
    # )
    # params: dict[str, str] = model_to_dict(creature)
    with Session() as sess:
        try:
            sess.add(DBCreature(**creature.model_dump()))
            sess.commit()
        # try:
        #     cur.execute(stmt, params)
        except IntegrityError:
            raise Duplicate(f"Creature `{creature.name}` already exist")
        return get_one(creature.name)


def modify(creature: Creature) -> Creature:
    return creature


def replace(name: str, creature: Creature) -> Creature:
    # stmt = """UPDATE creature
    #             SET country=:country,
    #                 description=:description,
    #                 area=:area,
    #                 aka=:aka
    #             WHERE name=:name"""
    # params = model_to_dict(creature)
    # cur.execute(stmt, params)
    with Session() as sess:
        db = sess.query(DBCreature).filter(DBCreature.name == name).first()
        if not db:
            raise Missing(f"Creature `{name}` not found")

        db.name = creature.name
        db.description = creature.description
        db.area = creature.area
        db.aka = creature.aka
        try:
            sess.commit()
            sess.refresh(db)
        except IntegrityError:
            raise Duplicate(f"Creature `{creature.name}` already exist")
        return get_one(creature.name)


def delete(name: str):
    # stmt: str = "DELETE FROM creature WHERE name=:name"
    # params: dict[str, str] = {"name": name}
    # cur.execute(stmt, params)
    with Session() as sess:
        db = sess.query(DBCreature).filter(DBCreature.name == name).first()
        if not db:
            raise Missing(f"Creature `{name}` not found")
        sess.delete(db)
        sess.commit()
