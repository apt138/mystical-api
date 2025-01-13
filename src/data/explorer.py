from data.init import Session
from sqlalchemy.exc import IntegrityError
from model.explorer import Explorer
from typing import Tuple, Optional
from errors import Missing, Duplicate
from data.model import Explorer as DBExplorer

ExplorerRow = Tuple[str, str, str]


def row_to_model(row: ExplorerRow | DBExplorer) -> Explorer:
    if isinstance(row, DBExplorer):
        name = row.name
        country = row.country
        description = row.description
    else:
        name, country, description = row
    return Explorer(
        name=name,
        country=country,
        description=description,
    )


def model_to_dict(explorer: Explorer) -> dict[str, str]:
    return explorer.model_dump()


def get_all() -> list[Explorer]:
    # stmt: str = "SELECT * FROM explorer;"
    # cur.execute(stmt)
    with Session() as sess:
        rows = sess.query(DBExplorer).all()
        return [row_to_model(row) for row in rows]


def get_one(name: str) -> Optional[Explorer]:
    # stmt: str = """SELECT * FROM explorer
    #             WHERE name=:name;"""
    # params: dict[str, str] = {"name": name}
    # cur.execute(stmt, params)
    # row = cur.fetchone()
    with Session() as sess:
        row = sess.query(DBExplorer).filter(DBExplorer.name == name).first()
        if not row:
            raise Missing(f"Explorer `{name}` not found")
        return row_to_model(row)


def create(explorer: Explorer) -> Explorer:
    # stmt: str = """INSERT INTO explorer
    #                 VALUES (:name, :country, :description);"""
    # params: dict[str, str] = model_to_dict(explorer)
    # try:
    #     cur.execute(stmt, params)
    with Session() as sess:
        sess.add(DBExplorer(**explorer.model_dump()))
        try:
            sess.commit()
        except IntegrityError:
            raise Duplicate(f"Explorer `{explorer.name}` already exists")
        return get_one(explorer.name)


def replace(name: str, explorer: Explorer) -> Explorer:
    # stmt: str = """UPDATE explorer
    #                 SET country=:country,
    #                     description=:description
    #                 WHERE name=:name;"""
    # params: dict[str, str] = model_to_dict(explorer)
    # cur.execute(stmt, params)
    with Session() as sess:
        db = sess.query(DBExplorer).filter(DBExplorer.name == name).first()
        if not db:
            raise Missing(f"Explorer `{explorer.name}` not found")

        db.name = explorer.name
        db.country = explorer.country
        db.description = explorer.description
        try:
            sess.commit()
            sess.refresh(db)
        except IntegrityError:
            raise Duplicate(f"Explorer `{explorer.name}` already exists")
        return get_one(explorer.name)


def modify(explorer: Explorer) -> Explorer:
    return explorer


def delete(name: str) -> None:
    # stmt: str = "DELETE FROM explorer WHERE name=:name;"
    # params: dict[str, str] = {"name": name}
    # cur.execute(stmt, params)
    with Session() as sess:
        db = sess.query(DBExplorer).filter(DBExplorer.name == name).first()
        if not db:
            raise Missing(f"Explorer `{name}` not found")
        sess.delete(db)
        sess.commit()
