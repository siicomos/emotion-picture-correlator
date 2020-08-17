#!/bin/env python3

# Python version: 3.8.3
# Author: Liam Ling
# Contact: liam_ling@sfu.ca
# File name: app.py
# Description:
"""Configuration settings using a Pydantic BaseSettings object
"""

from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Configurable application settings"""

    DEBUG = False

    # API metadata
    API_TITLE = "Model-1 API"
    API_DESCRIPTION = """Detect and process human face with emotion and report the emotion"""
    API_VERSION = "1.0"
    # Prefix for URL endpoints (not used currently)
    # API_V1_STR = '/api/v1'

    # CORS settings - allow all currently
    BACKEND_CORS_ORIGINS = ["http://localhost:3000"]

settings = Settings()
