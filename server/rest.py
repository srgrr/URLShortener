import uvicorn
import logging
from cli import get_configuration
from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from backend_accessor import get_backend
from pydantic import BaseModel
from typing import Optional

app_configuration = get_configuration()

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


class CreateBody(BaseModel):
    long_url: str
    desired_vanity: Optional[str]


@app.post("/", tags=["shortener"])
async def create_url(body: CreateBody):
    """Get a new short URL for a given long URL
    :param body: Body is a JSON with two strings long_url and desired_vanity, the later can be left empty if there is
    no particular preference
    :return: 200 (OK), {"short_url": generated_short_url}, 409 if desired vanity is already taken, 500 if URL gen failed
    """
    long_url, desired_vanity = body.long_url, body.desired_vanity
    short_url = _get_short_url(desired_vanity)
    get_backend(app_configuration).insert_new_url(long_url, short_url)
    return {
        "short_url": short_url
    }


@app.get("/{shortened_url}", tags=["shortener"])
async def get_url(shortened_url):
    """Given a short url, get redirected to the URL mapped by it
    :param shortened_url: Short URL
    :return: 302: found (temporary redirect)
    """
    long_url = _get_long_url(shortened_url)

    if long_url:
        return JSONResponse(
            status_code=status.HTTP_302_FOUND,
            headers={"Location": long_url},
            content=None
        )

    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        f"URL {shortened_url} doesn't redirect anywhere"
    )


@app.exception_handler(Exception)
def oauth_error_handler(_: Request, ex: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": f"Something went wrong: {ex}"},
        headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
    )


def _get_new_url():
    return get_backend(app_configuration).get_new_url()


def _get_short_url(desired_vanity=None):
    if desired_vanity:
        if _get_long_url(desired_vanity):
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"URL {desired_vanity} is already taken"
            )
        return desired_vanity
    return _get_new_url()


def _get_long_url(short_url):
    return get_backend(app_configuration).get_long_url(short_url)


def _configure_logger():
    args = {
        "filename": app_configuration["server"]["logging_file"],
        "level": logging.DEBUG,
        "format": "%(asctime)s %(levelname)-8s %(message)s",
        "datefmt": "%Y-%m-%d %H:%M:%S"
    }
    logging.basicConfig(**args)


if __name__ == '__main__':
    _configure_logger()
    uvicorn.run("rest:app", host="0.0.0.0", port=int(app_configuration["server"]["port"]))