#!/bin/env python3

# Author: Jim Lee

import json
import urllib

import pandas as pd
import requests

from ..config import config


def GIFGIFMatrixSearch(emotionsingel,variable):
    API_KEY = config.scraper_api_key
    API_ENDPOINT_METRICS = config.scraper_api_endpoint_metrics
    API_ENDPOINT_RESULTS = config.scraper_api_endpoint_results
#     mode=random
    query = '?pID=gifgif&mode=all&key={key}'.format(key=API_KEY)
    url = urllib.parse.urljoin(API_ENDPOINT_METRICS, query)
    lmt = config.scraping_limit
    
    response = requests.get(url)
    response.raise_for_status()
    data = json.loads(response.text)
    
    df = pd.read_json(response.text)
    # print(df[df['metric'] == emotionsingel]['mID'].values[0])
    metric_id = df[df['metric'] == emotionsingel]['mID'].values[0]
    # print(metric_id)#&mID={mID}
    search_query = '?pID=gifgif&mID={mID}&metric_score={matrix_score}&limit={limit}&key={key}'.format(
        mID=metric_id, limit=lmt, matrix_score = variable, key=API_KEY
    )
    url = urllib.parse.urljoin(API_ENDPOINT_RESULTS, search_query)
    response = requests.get(url)
    response.raise_for_status()
    gifs_result = json.loads(response.content)
#     print(gifs_result['results'][0]['content_data']['embedLink'])
    display_url_list = []
    for i in range(len(gifs_result['results'])):
        url = gifs_result['results'][i]['content_data']['embedLink']#[0]['gif']['url'] #This is the url from json.
        # print (url)
        # urllib.request.urlretrieve(url, 'GIFGIFS'+str(i)+'.gif') #Downloads the gif file.
        display_url_list.append(url)
    return display_url_list
