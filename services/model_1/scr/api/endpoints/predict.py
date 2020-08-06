#!/bin/env python3

# Python version: 3.8.3
# Author: Liam Ling
# Contact: liam_ling@sfu.ca
# File name: predict.py
# Description:
"""Endpoint /predict
"""

import logging

from fastapi import APIRouter, File

logger = logging.getLogger(__name__)

router = APIRouter

@router.post("/", tags=["predict"])
async def predict_emotion(file: bytes = File(...)):
