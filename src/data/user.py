from model.user import User
from errors import Missing, Duplicate
from data.init import cur, IntegrityError
from typing import Tuple

cur.execute(
    """CREATE TABLE IF NOT EXISTS user(
                name TEXT PRIMARY KEY,
                hash_ TEXT
            );"""
)
cur.execute(
    """CREATE TABLE IF NOT EXISTS xuser(
                name TEXT PRIMARY KEY,
                hash_ TEXT
            );"""
)

UserRow = Tuple[str, str]


def row_to_model(row: UserRow) -> User:
    name, hash_ = row
    return User(name=name, hash_=hash_)


def model_to_dict(user: User) -> dict[str, str]:
    return user.model_dump()


def get_all() -> list[User]:
    stmt: str = "SELECT * FROM user;"
    cur.execute(stmt)
    return [row_to_model(row) for row in cur]


def get_one(name: str):
    stmt = """SELECT * FROM user WHERE name=:name"""
    params = {"name": name}
    cur.execute(stmt, params)
    row = cur.fetchone()
    if not row:
        raise Missing(f"User `{name}` not found")

    return row_to_model(row)


def create(user: User, table: str = "user") -> User:
    """Add <user> to user or xuser table"""
    stmt: str = f"INSERT INTO {table} VALUES (:name, :hash_);"
    params: dict[str, str] = model_to_dict(user)
    try:
        cur.execute(stmt, params)
    except IntegrityError:
        raise Duplicate(f"User `{user.name}` already exists")

    return get_one(user.name)


def replace(name: str, user: User) -> User:
    stmt: str = "UPDATE user SET name=:name, hash_=:hash_ WHERE name=:name_org;"
    params = {**model_to_dict(user), "name_org": name}
    cur.execute(stmt, params)
    if not cur.rowcount == 1:
        raise Missing(f"User `{name}` not found")

    return get_one(user.name)


def delete(name: str) -> None:
    stmt: str = "DELETE FROM user WHERE name=:name;"
    params: dict[str, str] = {"name": name}
    user = get_one(name)
    cur.execute(stmt, params)
    if not cur.rowcount == 1:
        raise Missing(f"User `{name}` not found")
    create(user=user, table="xuser")
