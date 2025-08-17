from fastapi import FastAPI

from fastapi_autoloader import AutoLoader

app = FastAPI()

controllers = AutoLoader("example/controllers")
controllers.load(app)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello"}
