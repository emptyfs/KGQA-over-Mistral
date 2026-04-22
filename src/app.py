import uvicorn
import uuid

from fastapi import FastAPI, Body, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import dotenv_values
from pathlib import Path
from contextlib import asynccontextmanager

from controller.mistral import Mistral

BASE_DIR = Path(__file__).parents[1] 
config = dotenv_values(BASE_DIR / ".env")
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

app.mount("/static", StaticFiles(directory=BASE_DIR / "src" / "static"))

@app.delete("/api/v1/graph")
async def clear_graph():
    try:
        app.state.mistral.clear_all_data()
        return {"status": "success", "message": "Граф и локальные данные успешно очищены."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/swagger_spec")
async def spec():
    return FileResponse(BASE_DIR / "src" / "specs" / "swagger_config.yaml")

@app.get("/swagger")
async def docs():
    return FileResponse(BASE_DIR / "src" / "templates" / "swagger.html")

@app.post("/api/v1/query/analyze")
async def query_analyze(query: str = Body(...)):
    try:
        response = app.state.mistral.query(query)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/documents/ingest")
async def docs_ingest(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    content = await file.read()
    task_id = str(uuid.uuid4())

    background_tasks.add_task(
        app.state.mistral.build_knowledge_graph,
        content,
        file.filename,
        task_id
    )

    return {
        "status": "processing",
        "task_id": task_id
    }


@app.get("/api/v1/documents/ingest/status/{task_id}")
async def ingest_status(task_id: str):
    progress = app.state.mistral.get_progress(task_id)
    if progress is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return progress


if __name__ == "__main__":

    host = "0.0.0.0"
    if PORT is None:
        print("Error: port not specified")
        raise SystemExit(1)
    print(f"The {TITLE} service has been launched")
    #uvicorn.run("app:app", host=host, port=PORT, reload=True)
    uvicorn.run("app:app", host=host, port=PORT)
