from model.explorer import Explorer

_explorers: list[Explorer] = [
    Explorer(name="Claude Hande", country="FR", description="Scarce during full moons"),
    Explorer(name="Noah Weiser", country="DE", description="Myopic machete man"),
]


def get_all() -> list[Explorer]:
    return _explorers


def get_one(name: str) -> Explorer | None:
    for _explorer in _explorers:
        if name.lower() == _explorer.name.lower():
            return _explorer

    return None


# The following are nonfunctional for now,
# so they just act like they work, without modifying
# the actual fake _explorers list:
def create(explorer: Explorer) -> Explorer:
    """Add an explorer"""
    return explorer


def modify(explorer: Explorer) -> Explorer:
    """Partially modify the explorer"""
    return explorer


def replace(explorer: Explorer) -> Explorer:
    """Completely replace the explorer"""
    return explorer


def delete(name: str) -> None:
    """Delete an explorer; return None if it existed"""
    return None
