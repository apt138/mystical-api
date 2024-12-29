from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from service import user as srvc
from model.user import User
from errors import INTERNAL_SERVER_ERROR_MSG, Missing, Duplicate, InvalidUser

router = APIRouter(tags=["user"], prefix="/user")

# This dependency makes a post to "/user/token"
# (from a form containing a username and password)
# and returns an access token.

oauth_dep = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token")
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = srvc.auth_user(form_data.username, form_data.password)
        token = srvc.create_access_token(user.name)
        return {"access_token": token, "token_type": "bearer"}

    except (InvalidUser, Missing) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.msg,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/token")
def get_access_token(token: str = Depends(oauth_dep)) -> dict:
    """Return the current access token"""
    return {"token": token}


@router.get("/")
def get_all() -> list[User]:
    return srvc.get_all()


@router.get("/{name}")
def get_one(name: str) -> User:
    try:
        return srvc.get_one(name)
    except Missing as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.msg)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(user: User) -> User:
    try:
        return srvc.create(user)
    except Duplicate as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg)


@router.put("/{name}")
def replace(name: str, user: User) -> User:
    try:
        return srvc.replace(name, user)
    except Missing as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.msg)


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete(name: str):
    try:
        return srvc.delete(name)
    except Missing as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.msg)
