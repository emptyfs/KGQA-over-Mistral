import uvicorn

from fastapi import FastAPI, Body, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from dotenv import dotenv_values
from pathlib import Path
from contextlib import asynccontextmanager

from controller.mistral import Mistral

BASE_DIR = Path(__file__).parent 
config = dotenv_values(BASE_DIR / "settings.env")
PORT = int(config.get("PORT"))
TITLE = config.get("PACKAGE_NAME")
URL = config.get("URL")

async def startup(app: FastAPI):
    app.state.mistral = Mistral(config)

async def shutdown(app: FastAPI):
    pass

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup(app)
    yield
    await shutdown(app)

app = FastAPI(
    title=f"{TITLE} API",
    debug=False, 
    docs_url=None, 
    redoc_url=None, 
    openapi_url=None,
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"))

@app.get("/swagger_spec")
async def spec():
    return FileResponse(BASE_DIR / "specs" / "swagger_config.yaml")

@app.get("/swagger")
async def docs():
    return FileResponse(BASE_DIR / "templates" / "swagger.html")

@app.post("/api/v1/documents/ingest")
async def docs_ingest(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    content = await file.read()

    background_tasks.add_task(
        app.state.mistral.build_knowledge_graph,
        content,
        file.filename
    )

    return {
        "status": "processing"
    }


if __name__ == "__main__":

    host = "0.0.0.0"
    if PORT is None:
        print("Error: port not specified")
        raise SystemExit(1)
    print(f"The {TITLE} service has been launched")
    uvicorn.run("app:app", host=host, port=PORT, reload=True)
    #uvicorn.run("app:app", host=host, port=PORT)
