#!/bin/env python3

# Python version: 3.8.3
# Author: Liam Ling
# Contact: liam_ling@sfu.ca
# File name: router.py
# Description:
"""API Router
"""

from fastapi import APIRouter

from .endpoints import predict

api_router = APIRouter()
api_router.include_router(predict.router, prefix="/predict", tags=["predict"])