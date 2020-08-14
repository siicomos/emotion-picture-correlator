#!/bin/env python3

# Python version: 3.8.3
# Author: Liam Ling
# Contact: liam_ling@sfu.ca
# File name: predict.py
# Description:
"""Endpoint /predict
"""

import logging

from fastapi import APIRouter, File, UploadFile, Request

from ...config import config
from ...helpers import fileManager
from ...helpers.executor import Executor

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", tags=["predict"])
async def predict_emotion(request: Request, uploadFile: UploadFile = File(...)):
    """Use prebuild model to predict the face emotion"""
    temp_img = uploadFile.filename
    content = await uploadFile.read()
    result_folder = fileManager.join_path(config.predict_result_temp_folder, f"{request.client.host}")
    path_to_temp_img = fileManager.join_path(result_folder, temp_img)
    with open(path_to_temp_img, "wb") as f:
        f.write(content)

    cmd = f"{config.openface_bin}/FaceLandmarkImg -f {path_to_temp_img} -out_dir {result_folder}"
    Executor.run(cmd, verbose=True)
