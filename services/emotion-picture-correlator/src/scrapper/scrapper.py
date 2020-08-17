def GIFGIFMatrixSearch(emotionsingel,varable):
    API_KEY = '54a309ac1c61be23aba0da3f'
    API_ENDPOINT_METRICS = 'https://www.qnt.io/api/displaymetrics'
    API_ENDPOINT_RESULTS = 'https://www.qnt.io/api/results'
#     mode=random
    query = '?pID=gifgif&mode=all&key={key}'.format(key=API_KEY)
    url = urllib.parse.urljoin(API_ENDPOINT_METRICS, query)
    lmt = 5
    
    response = requests.get(url)
    response.raise_for_status()
    data = json.loads(response.text)
    
    df = pd.read_json(response.text)
    print(df[df['metric'] == emotionsingel]['mID'].values[0])
    metric_id = df[df['metric'] == emotionsingel]['mID'].values[0]
    print(metric_id)#&mID={mID}
    search_query = '?pID=gifgif&mID={mID}&metric_score={matrix_score}&limit={limit}&key={key}'.format(
        mID=metric_id, limit=lmt, matrix_score = varable, key=API_KEY
    )
    url = urllib.parse.urljoin(API_ENDPOINT_RESULTS, search_query)
    response = requests.get(url)
    response.raise_for_status()
    gifs_result = json.loads(response.content)
#     print(gifs_result['results'][0]['content_data']['embedLink'])
    display_url_list = []
    for i in range(len(gifs_result['results'])):
        url = gifs_result['results'][i]['content_data']['embedLink']#[0]['gif']['url'] #This is the url from json.
        print (url)
        urllib.request.urlretrieve(url, 'GIFGIFS'+str(i)+'.gif') #Downloads the gif file.
        display_url_list.append(url)
    return display_url_list