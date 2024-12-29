from fastapi import APIRouter, HTTPException
from starlette import status
from model.creature import Creature
from service import creature as srvc
from errors import Missing, Duplicate, INTERNAL_SERVER_ERROR_MSG

router = APIRouter(tags=["creature"], prefix="/creature")


@router.get("/")
def get_all() -> list[Creature]:
    try:
        return srvc.get_all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=INTERNAL_SERVER_ERROR_MSG,
        )


@router.get("/{name}")
def get_one(name: str) -> Creature | None:
    try:
        return srvc.get_one(name)
    except Missing as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.msg)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=INTERNAL_SERVER_ERROR_MSG,
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(creature: Creature) -> Creature:
    try:
        return srvc.create(creature)
    except Duplicate as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=INTERNAL_SERVER_ERROR_MSG,
        )


# @router.patch("/{name}")
# def modify(name: str, creature: Creature) -> Creature:
#     return srvc.modify(creature)


@router.put("/{name}")
def replace(name: str, creature: Creature) -> Creature:
    try:
        return srvc.replace(name, creature)
    except Missing as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.msg)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=INTERNAL_SERVER_ERROR_MSG,
        )


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete(name: str) -> None:
    try:
        return srvc.delete(name)
    except Missing as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.msg)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=INTERNAL_SERVER_ERROR_MSG,
        )
