from fastapi import APIRouter
from model.creature import Creature
from fake import creature as service

router = APIRouter(tags=["creature"], prefix="/creature")


@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Creature | None:
    return service.get_one(name)


@router.post("/")
def create(creature: Creature) -> Creature:
    return service.create(creature)


@router.patch("/{name}")
def modify(name: str, creature: Creature) -> Creature:
    return service.modify(creature)


@router.put("/{name}")
def replace(name: str, creature: Creature) -> Creature:
    return service.replace(creature)


@router.delete("/{name}")
def delete(name: str) -> None:
    return service.delete(name)
