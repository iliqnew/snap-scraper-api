from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from . import models
from .database import engine
from .routers.screenshots import router as screenshots_router


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.mount("/data", StaticFiles(directory="data"), name="data")
app.include_router(screenshots_router)


@app.get("/isalive")
async def isalive():
    return {"status": "ok"}
