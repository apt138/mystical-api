from model.user import User
from errors import Missing, Duplicate

fakes = [
    User(name="kwijobo", hash="abc"),
    User(name="ermagerd", hash="xyz"),
]


def find(name: str) -> User:
    for user in fakes:
        if user.name == name:
            return user

    raise Missing(f"User `{name}` not found")


def get_all() -> list[User]:
    return fakes


def get_one(name: str) -> User:
    return find(name)


def create(user: User) -> User:
    if find(user.name):
        raise Duplicate(f"User `{user.name}` already exists ")
    fakes.append(user)
    return user


def replace(name: str, new_user: User) -> User:
    user = find(name)
    if not user:
        raise Missing(f"User `{name}` not found")

    user.name = new_user.name
    user.hash_ = new_user.hash_

    return get_one(user.name)


def delete(name: str) -> None:
    if not find(name):
        raise Missing(f"User `{name}` not found")
