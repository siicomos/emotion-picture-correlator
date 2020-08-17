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
from urllib.parse import urlparse

import numpy as np
import pandas as pd
from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse
from joblib import load

from ...config import config
from ...helpers import fileManager
from ...helpers.executor import Executor
from ...mappings import (scraper_mapping, svm_faces_aur_clf_mapping,
                         svm_gifgif_aur_clf100_mapping)
from ...scrapper.scrapper import GIFGIFMatrixSearch

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
        except Exception:
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

    if not fileManager.check_file(csv_file):
        logger.debug("Fail to extract featrues from the incoming file")
        raise HTTPException(
            status_code=406,
            detail="Fail to detect face, are you sure you took a picture of your face?"
        )
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

    # auc_data = openface_raw_data_filtered[['confidence', 'AU01_c', 'AU02_c', 
    #    'AU04_c', 'AU05_c', 'AU06_c', 'AU07_c', 'AU09_c', 'AU10_c', 
    #    'AU12_c', 'AU14_c', 'AU15_c', 'AU17_c', 'AU20_c', 'AU23_c', 
    #    'AU25_c', 'AU26_c', 'AU28_c', 'AU45_c']]
    # auc_data_X = auc_data.iloc[:,1:]

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
    logger.debug(f"Emotion keyword: {gifgif_emotion_keyword}")
    if gifgif_emotion_keyword:
        try:
            list_gifgif_url = GIFGIFMatrixSearch(emotionsingel=gifgif_emotion_keyword, variable=0.65)
        except Exception:
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

    # download the gifs
    list_download_result = []
    for url in list_gifgif_url:
        sub_path = urlparse(url).path
        full_path = fileManager.join_path(config.scraper_temp_folder, sub_path[1:]) # remove the first / in url path
        logger.debug(f"****full path***** : {config.scraper_temp_folder}")
        download_result = fileManager.download_file(url=url, save_path=full_path.parent, target_name=full_path.name)
        list_download_result.append(download_result)
    dict_download_result = dict(zip(list_gifgif_url, list_download_result))
    logger.debug(f"Download result:\n{dict_download_result}")

    # start collecting valid .gif
    count = 0
    response_content = {}

    for url, download_result in dict_download_result.items():
        # collect total 5 .gif
        if count == 5:
            break

        # run the OpenFace command
        path_to_temp_img = download_result.get("path")
        result_folder = fileManager.get_parent(path_to_temp_img)
        cmd = f"{config.openface_bin}/FaceLandmarkVidMulti -f {path_to_temp_img} -out_dir {result_folder} -mloc {config.openface_model_2}"
        if config.log_level == "DEBUG":
            verbose = False
        else:
            verbose = True
        returncode, stdout, stderr = Executor.run(cmd, verbose=verbose)
        if returncode != 0:
            logger.debug(f"Fail to execute OpenFace against the .gif file: {path_to_temp_img}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )
        
        # get the AUs (AU_r and AU_c) data
        csv_file = f"{result_folder.resolve()}/{fileManager.get_stem(path_to_temp_img)}.csv"
        if not fileManager.check_file(csv_file):
            logger.debug(f"Fail to extract featrues from the .gif file: {path_to_temp_img}")
        else:
            # valid .gif
            count += 1

            openface_raw_data = pd.read_csv(csv_file, sep=',\s+', delimiter=',', encoding="utf-8", skipinitialspace=True)
            
            ########################
            ## this is important! ##
            ########################
            ## if there are multiple frames in the .gif - ONLY the frames with higher than threshold confidence will be considered!
            if openface_raw_data.shape[0] > 1:
                openface_raw_data_filtered = openface_raw_data[openface_raw_data["confidence"] > config.openface_model_2_filter_threshold]
            else:
                openface_raw_data_filtered = openface_raw_data

            average_confidence = openface_raw_data_filtered["confidence"].mean()

            aur_data = openface_raw_data_filtered[['confidence', 'AU01_r', 'AU02_r', 
            'AU04_r', 'AU05_r', 'AU06_r', 'AU07_r', 'AU09_r', 'AU10_r', 
            'AU12_r', 'AU14_r', 'AU15_r', 'AU17_r', 'AU20_r', 'AU23_r', 
            'AU25_r', 'AU26_r', 'AU45_r']]
            aur_data_X = aur_data.iloc[:,1:]

            # auc_data = openface_raw_data_filtered[['confidence', 'AU01_c', 'AU02_c', 
            # 'AU04_c', 'AU05_c', 'AU06_c', 'AU07_c', 'AU09_c', 'AU10_c', 
            # 'AU12_c', 'AU14_c', 'AU15_c', 'AU17_c', 'AU20_c', 'AU23_c', 
            # 'AU25_c', 'AU26_c', 'AU28_c', 'AU45_c']]
            # auc_data_X = auc_data.iloc[:,1:]

            logger.debug(f"OpenFace confidence (threshold {config.openface_model_2_filter_threshold}): {average_confidence}")

            # load the model 1 PCA and clf
            model_2_pca = pk.load(open(fileManager.join_path(config.models_folder, config.model_2_pca),'rb'))
            model_2_clf = load(fileManager.join_path(config.models_folder, config.model_2_clf))

            # PCA transform and predict the emotion
            aur_data_X_pca = model_2_pca.transform(aur_data_X)
            model_2_clf_pred_result = model_2_clf.best_estimator_.predict(aur_data_X_pca)
            # model_2_clf_pred_prob = model_2_clf.best_estimator_.predict_proba(aur_data_X_pca)
            logger.debug(f"Prediction result: {model_2_clf_pred_result}")

            # calculate the score
            model_2_clf_target_emotion = gifgif_emotion_keyword
            # model_2_clf_target_indicator = list(svm_gifgif_aur_clf100_mapping.mapping.keys())[
            #     list(svm_gifgif_aur_clf100_mapping.mapping.values()).index(model_2_clf_target_emotion)
            # ]

            model_2_clf_confi_matrix = {}
            prediction_result_len = len(model_2_clf_pred_result)
            for indictator, emotion in svm_gifgif_aur_clf100_mapping.mapping.items():
                confidence = list(model_2_clf_pred_result).count(indictator)/prediction_result_len
                model_2_clf_confi_matrix.update({emotion: confidence})

            target_confidence = model_2_clf_confi_matrix.get(model_2_clf_target_emotion)
            logger.debug(f"Predicted emotion: {model_2_clf_target_emotion} confidence: {target_confidence}")
            logger.debug(f"Prediction confidence matrix:\n{model_2_clf_confi_matrix}")
            
            response_content.update({url: target_confidence})

        # remove the temp folder
        if fileManager.delete_path(result_folder):
            logger.debug(f"Temp folder for the model 2 result successfully removed: {result_folder}")
        else:
            logger.debug(f"Temp folder for the model 2 result remove failed: {result_folder}")
    
    response_content.update({"emotion":model_2_clf_target_emotion})

    return JSONResponse(
        status_code=200,
        content=response_content
    )
