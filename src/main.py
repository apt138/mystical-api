from fastapi import FastAPI
from web import explorer, creature, user

app = FastAPI()


@app.get("/")
def root():
    return {"message": "hello there!"}


@app.get("/echo/{testing}")
def echo(testing: str):
    return {"message": f"{testing}"}


app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)
