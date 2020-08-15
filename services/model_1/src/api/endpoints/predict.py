#!/bin/env python3

# Python version: 3.8.3
# Author: Liam Ling
# Contact: liam_ling@sfu.ca
# File name: predict.py
# Description:
"""Endpoint /predict
"""

import logging
from datetime import datetime

from fastapi import APIRouter, File, Request, UploadFile

from ...config import config
from ...helpers import fileManager
from ...helpers.executor import Executor

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", tags=["predict"])
async def predict_emotion(request: Request, uploadFile: UploadFile = File(...)):
    """Use prebuild model to predict the face emotion"""
    temp_img = uploadFile.filename # get user image name
    content = await uploadFile.read() # get image data
    time_now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f') # time now
    # make the temp folder
    result_folder = fileManager.join_path(config.predict_result_temp_folder, f"{time_now}-{request.client.host}")
    fileManager.try_make_path(result_folder)
    # write to temp img file
    path_to_temp_img = fileManager.join_path(result_folder, temp_img)
    with open(path_to_temp_img, "wb") as f:
        f.write(content)
    logger.debug(f"File created: {path_to_temp_img}")

    # run the OpenFace command
    cmd = f"{config.openface_bin}/FaceLandmarkImg -f {path_to_temp_img} -out_dir {result_folder}"
    Executor.run(cmd, verbose=True)

    # 