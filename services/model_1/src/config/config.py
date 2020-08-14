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

predict_result_temp_folder = Path(os.environ.get("PREDICT_RESULT_TEMP_FOLDER", "/tmp/result"))
openface_bin = Path(os.environ.get("OPENFACE_BIN", "/OpenFace/build/bin"))