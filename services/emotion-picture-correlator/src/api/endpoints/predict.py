#!/bin/env python3

# Python version: 3.8.3
# Author: Liam Ling
# Contact: liam_ling@sfu.ca
# File name: predict.py
# Description:
"""Endpoint /predict
"""

import logging
import pickle as pk
from datetime import datetime

import numpy as np
import pandas as pd
from fastapi import APIRouter, File, Request, UploadFile, HTTPException
from joblib import load

from ...config import config
from ...helpers import fileManager
from ...helpers.executor import Executor
from ...scrapper.scrapper import GIFGIFMatrixSearch
from ...mappings import scraper_mapping, svm_faces_aur_clf_mapping

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
        try:
            f.write(content)
        except Exception as e:
            logger.debug("Fail to save the incoming file")
            raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    logger.debug(f"File created: {path_to_temp_img}")

    # run the OpenFace command
    cmd = f"{config.openface_bin}/FaceLandmarkImg -f {path_to_temp_img} -out_dir {result_folder} -mloc {config.openface_model_1}"
    if config.log_level == "DEBUG":
        verbose = False
    else:
        verbose = True
    returncode, stdout, stderr = Executor.run(cmd, verbose=verbose)
    if returncode != 0:
        logger.debug("Fail to execute OpenFace against the incoming file")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    # get the AUs (AU_r and AU_c) data
    csv_file = f"{result_folder.resolve()}/{fileManager.get_stem(temp_img)}.csv"
    openface_raw_data = pd.read_csv(csv_file, sep=',\s+', delimiter=',', encoding="utf-8", skipinitialspace=True)
    
    ########################
    ## this is important! ##
    ########################
    ## if there are multiple faces in the frame - ONLY the highest confidence one will be considered!
    if openface_raw_data.shape[0] > 1:
        openface_raw_data_filtered = openface_raw_data[openface_raw_data["confidence"] == openface_raw_data["confidence"].max()]
    else:
        openface_raw_data_filtered = openface_raw_data

    highest_confidence = openface_raw_data_filtered["confidence"].values

    aur_data = openface_raw_data_filtered[['confidence', 'AU01_r', 'AU02_r', 
       'AU04_r', 'AU05_r', 'AU06_r', 'AU07_r', 'AU09_r', 'AU10_r', 
       'AU12_r', 'AU14_r', 'AU15_r', 'AU17_r', 'AU20_r', 'AU23_r', 
       'AU25_r', 'AU26_r', 'AU45_r']]
    aur_data_X = aur_data.iloc[:,1:]

    auc_data = openface_raw_data_filtered[['confidence', 'AU01_c', 'AU02_c', 
       'AU04_c', 'AU05_c', 'AU06_c', 'AU07_c', 'AU09_c', 'AU10_c', 
       'AU12_c', 'AU14_c', 'AU15_c', 'AU17_c', 'AU20_c', 'AU23_c', 
       'AU25_c', 'AU26_c', 'AU28_c', 'AU45_c']]
    auc_data_X = auc_data.iloc[:,1:]

    logger.debug(f"OpenFace confidence (selected face): {highest_confidence}")

    # load the model 1 PCA and clf
    model_1_pca = pk.load(open(fileManager.join_path(config.models_folder, config.model_1_pca),'rb'))
    model_1_clf = load(fileManager.join_path(config.models_folder, config.model_1_clf))

    # PCA transform and predict the emotion
    aur_data_X_pca = model_1_pca.transform(aur_data_X)
    model_1_clf_pred_result = model_1_clf.best_estimator_.predict(aur_data_X_pca)[0]
    model_1_clf_pred_prob = model_1_clf.best_estimator_.predict_proba(aur_data_X_pca)[0][0]

    model_1_clf_classes = model_1_clf.best_estimator_.classes_[0]
    logger.debug(f"Predicted emotion: {model_1_clf_pred_result} confidence: {model_1_clf_pred_prob[np.where(model_1_clf_classes == model_1_clf_pred_result)]}")
    logger.debug(f"Prediction confidence matrix:\n{dict(zip(model_1_clf_classes, model_1_clf_pred_prob))}")

    # remove the temp folder
    if fileManager.delete_path(result_folder):
        logger.debug(f"Temp folder for the model 1 result successfully removed: {result_folder}")
    else:
        logger.debug(f"Temp folder for the model 1 result remove failed: {result_folder}")

    # tranlate the mapping from model 1 to gif scraper mapping
    model_1_clf_pred_result_indicator = list(svm_faces_aur_clf_mapping.mapping.keys())[
        list(svm_faces_aur_clf_mapping.mapping.values()).index(model_1_clf_pred_result)
    ]

    # gif scraper
    gifgif_emotion_keyword = scraper_mapping.mapping.get(model_1_clf_pred_result_indicator)
    if gifgif_emotion_keyword:
        try:
            list_gifgif_url = GIFGIFMatrixSearch(emotionsingel=gifgif_emotion_keyword, variable=0.65)
        except Exception as e:
            logger.debug("Fail to retrive url from GIFGIF")
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )
    else:
        logger.debug("Fail to map the model 1 emotion keyword to GIFGIF search keyword")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
        
    logger.debug(f"List of GIFGIF url:\n{list_gifgif_url}")

    # load the model 2 PCA and clf