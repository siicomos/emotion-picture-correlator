#!/bin/env python3

# Python version: 3.8.3
# Author: Liam Ling
# Contact: liam_ling@sfu.ca
# File name: app.py
# Description:
"""Main application
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api import api_router
from .config.app_config import settings

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
    # openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)