import uvicorn
import aiohttp

from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from dotenv import dotenv_values
from pathlib import Path
from contextlib import asynccontextmanager

from services.proxy_service import proxy_fetch
from models.request_models import ProxyRequest

BASE_DIR = Path(__file__).parent 
config = dotenv_values(BASE_DIR / "settings.env")
PORT = int(config.get("PORT"))
TITLE = config.get("PACKAGE_NAME")
URL = config.get("URL")

async def startup(app: FastAPI):
    app.state.session = aiohttp.ClientSession()

async def shutdown(app: FastAPI):
    await app.state.session.close()

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




"""
@app.post("/takawaenga")
async def proxy(request_body: ProxyRequest = Body(...)):
    url = f"{URL}{request_body.endpoint}" if request_body.endpoint else URL
    method = request_body.method if request_body.method else "GET"

    try:
        response = await proxy_fetch(
            session=app.state.session,
            url=url,
            method=method.upper(),
            params=request_body.query,
            json=request_body.body
        )

        content_bytes = response["content"]
        status = response["status_code"]
        headers = response["headers"]

        return Response(content=content_bytes, status_code=status, headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
"""


if __name__ == "__main__":

    host = "0.0.0.0"
    if PORT is None:
        print("Error: port not specified")
        raise SystemExit(1)
    print(f"The {TITLE} service has been launched")
    uvicorn.run("app:app", host=host, port=PORT, reload=True)
    #uvicorn.run("app:app", host=host, port=PORT)
