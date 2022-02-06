#!/usr/bin/env python3

''' A module to get data for all of a youtube channel's videos '''

import os
import sys
import json
import requests
from bs4 import BeautifulSoup

from apify_client import ApifyClient

from typing import Dict, List, Union

def makeRequest (start_urls: Dict[str, str], token: str) -> List[any]:
    '''
    Makes a request to the YouTube Scraper API and returns data received.
    More info at: https://apify.com/bernardo/youtube-scraper

    :param start_urls: channel urls
    :param token: API token
    '''

    # Initialize the ApifyClient with your API token
    client = ApifyClient(token)

    # Prepare the actor input
    run_input = {
      "extendOutputFunction": "async ({ data, item, page, request, customData }) => {\n  return item; \n}",
      "extendScraperFunction": "async ({ page, request, requestQueue, customData, Apify, extendOutputFunction }) => {\n \n}",
      "handlePageTimeoutSecs": 3600,
      "proxyConfiguration": {
        "useApifyProxy": True
      },
      "startUrls": start_urls,
      "subtitlesLanguage": "en",
      "customData": {},
      "maxComments": 0
    }

    # Run the actor and wait for it to finish
    run = client.actor("bernardo/youtube-scraper").call(run_input=run_input)

    # Fetch actor results from the run's dataset (if there are any)
    return [item for item in client.dataset(run["defaultDatasetId"]).iterate_items()]

def processRawData (raw_data: List[Dict[str, any]]) -> List[Dict[str, Union[str, int]]]:
    '''
    Processes data from API resopnse to get only needed data.
    :param raw_data: data returned from the API request
    '''

    proc_data = []

    for item in raw_data:

        # check if it is a valid item
        try:
            item['url']
        except:
            continue

        proc_data.append(
                {
            'url' : item['url'],
            'title' : item['title'],
            'views' : item['viewCount'],
            'date' : item['date'],
            'tags' : get_tags(item['url']),
            }
        )

    return proc_data

def get_tags (url: str) -> List[str]:
    '''
    Gets the tags of the YouTube video at the URL passed.
    Scrapes the video page and gets tags from <meta> data.
    :param url: url of the video to get tags from
    '''

    tags = []

    # parse html and scrape tags
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    try:
        tags = soup.find('meta', {'name' : 'keywords'})['content'].split(',')
    except:
        print(f'Tags not found for {url}')

    return tags

if __name__ == '__main__':

    # parse arguments
    # channel url
    start_urls = [{'url' : url.strip()} for url in sys.stdin.readlines() if url.strip()]

    # output csv file
    try:
        CSV_FILE = sys.argv[1]
    except IndexError:
        raise IndexError ('No output csv file passed.')

    # get API token from creds.json file
    API_TOKEN = ''
    credentials_file = os.path.join(os.path.dirname(__file__), 'creds.json')

    if os.path.isfile(credentials_file):
        sys.stdout.write('Credentials file found.\n')
        with open(credentials_file, 'r', encoding='utf-8') as f:
            API_TOKEN = json.loads(''.join(f.readlines()))['API_TOKEN'];
    else:
        raise FileNotFoundError(f'Credentials file not found at: {credentials_file}')

    # make API request and get raw data
    sys.stdout.write(f'Making requests for: {[url for url in start_urls]}\n')
    data = processRawData(makeRequest(start_urls, API_TOKEN))

    # write data to a csv file
    sys.stdout.write(f'Exporting data to {CSV_FILE}\n')
    with open(CSV_FILE, 'w', encoding='utf-8') as f:
        f.write('url,title,views,date,tags\n')

        for item in data:
            f.write(f"{item['url']},{item['title']},{item['views']},{item['date']},{'/'.join(item['tags'])}\n")
