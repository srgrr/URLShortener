import uvicorn
import logging
from fastapi import Depends, FastAPI, Form, Request, Response, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


app = FastAPI(
    title="Local URL Shortener",
    openapi_tags=[
      {"name": "shortener", "description": "Endpoints for the shortener service itself"}
    ],
    description=__doc__,
    docs_url="/",
)


@app.on_event("startup")
def startup():
    # initialise application state from config settings
    logging.info(f"Started URLShortener instance")


@app.on_event("shutdown")
def startup():
    # initialise application state from config settings
    logging.info(f"Stopped URLShortener instance")


@app.post("/", tags=["shortener"])
async def create_url(request: Request):
    body = await request.json()
    return {
      "message": f"Posted long URL {body['long_url']}"
    }


@app.get("/{shortened_url}", tags=["shortener"])
async def get_url(shortened_url):
    return {
      "message": f"Got redirect petition for {shortened_url}"
    }


if __name__ == '__main__':
    uvicorn.run("server.rest:app", host="0.0.0.0", port=9113)