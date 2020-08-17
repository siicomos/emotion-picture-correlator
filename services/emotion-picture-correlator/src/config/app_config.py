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
    API_TITLE = "Emotiona-Picture-Correlator API"
    API_DESCRIPTION = """Detect and process human face with emotion and process the emotion to find the relevant GIFs"""
    API_VERSION = "1.0"
    
    # CORS settings - allow all currently
    BACKEND_CORS_ORIGINS = ["*"]

settings = Settings()
