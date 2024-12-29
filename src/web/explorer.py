from fastapi import APIRouter, HTTPException
from starlette import status
from model.explorer import Explorer
from service import explorer as srvc
from errors import Missing, Duplicate, INTERNAL_SERVER_ERROR_MSG

router = APIRouter(prefix="/explorer", tags=["explorer"])


@router.get("/")
def get_all() -> list[Explorer]:
    try:
        return srvc.get_all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=INTERNAL_SERVER_ERROR_MSG,
        )


@router.get("/{name}")
def get_one(name: str) -> Explorer | None:
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
def create(explorer: Explorer) -> Explorer:
    try:
        return srvc.create(explorer)
    except Duplicate as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=INTERNAL_SERVER_ERROR_MSG,
        )


# @router.patch("/{name}")
# def modify(name: str, explorer: Explorer) -> Explorer:
#     return srvc.modify(name, explorer)


@router.put("/{name}")
def replace(name: str, explorer: Explorer) -> Explorer:
    try:
        return srvc.replace(name, explorer)
    except Missing as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.msg)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=INTERNAL_SERVER_ERROR_MSG,
        )


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete(name: str):
    try:
        return srvc.delete(name)
    except Missing as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.msg)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=INTERNAL_SERVER_ERROR_MSG,
        )
