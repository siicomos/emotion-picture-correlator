#!/bin/env python3

# Python version: 3.8.3
# Author: Liam Ling
# Contact: liam_ling@sfu.ca
# File name: app.py
# Description:
"""Main application
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import api_router
from .config import config
from .config.app_config import settings
from .logger.logger import Logger

Logger(level=config.log_level)

logger = logging.getLogger(__name__)

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

if config.model_1_pca == "" or config.model_1_clf == "":
    logger.error("Model 1 PCA or CLF missing")
    raise RuntimeError("Fail to start application")
if config.model_2_pca == "" or config.model_2_clf == "":
    logger.error("Model 2 PCA or CLF missing")
    raise RuntimeError("Fail to start application")