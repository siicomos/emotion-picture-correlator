#!/bin/env python3

# Python version: 3.8.3
# Author: Liam Ling
# Contact: liam_ling@sfu.ca
# File name: config.py
# Description:
"""This file specifies configuration settings for this package.
"""

import os
from pathlib import Path

# API log level
log_level = os.environ.get("LOG_LEVEL", "INFO")

# predict endpoints
predict_result_temp_folder = Path(os.environ.get("PREDICT_RESULT_TEMP_FOLDER", "/tmp/result"))
openface_bin = Path(os.environ.get("OPENFACE_BIN", "/OpenFace/build/bin"))
openface_model_1 = "model/main_clnf_multi_pie.txt"
models_folder = Path("src/models/")
model_1_pca = os.environ.get("MODEL_1_PCA", "")
model_1_clf = os.environ.get("MODEL_1_CLF", "")

# gif scraper
scraper_api_key = os.environ.get("SCRAPER_API_KEY", "")
scraper_api_endpoint_metrics='https://www.qnt.io/api/displaymetrics'
scraper_api_endpoint_results='https://www.qnt.io/api/results'