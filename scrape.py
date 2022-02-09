#!/usr/bin/env python3

''' A module to get data for all of a youtube channel's videos '''

import os
import sys
import json
import requests
from bs4 import BeautifulSoup

from apify_client import ApifyClient

from typing import Dict, List, Union

def makeRequest (start_urls: List[Dict[str, str]], max_results: int, token: str) -> List[str]:
    '''
    Makes a request to the YouTube Scraper API and returns an iterator of
    the data received.
    More info at: https://apify.com/bernardo/youtube-scraper

    :param start_urls: channel urls
    :param max_results: max results to return, if zero then returns all videos
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

    if max_results:
        run_input['maxResults'] = max_results

    # Run the actor and wait for it to finish
    run = client.actor("bernardo/youtube-scraper").call(run_input=run_input)

    # Fetch actor results from the run's dataset (if there are any)
    return client.dataset(run["defaultDatasetId"]).iterate_items()

def processRawData (raw_data: List[Dict[str, str]]) -> List[Dict[str, Union[str, List[str], None]]]:
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
            'title' : item['title'].replace(',', ''),
            'views' : item['viewCount'],
            'date' : item['date'][:10],
            'tags' : get_tags(item['url']),
            }
        )

    return proc_data

def get_tags (url: str) -> Union[List[str], None]:
    '''
    Gets the tags of the YouTube video at the URL passed.
    Scrapes the video page and gets tags from <meta> data.
    :param url: url of the video to get tags from
    '''

    tags = []

    # parse html and scrape tags
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    try:
        tags = [tag.strip() for tag in soup.find('meta', {'name' : 'keywords'})['content'].split(',') if tag.strip()]
    except:
        print(f'Tags not found for {url}')
        tags.append('None')

    return tags

def read_credentials () -> str:
    '''
    Returns the API_TOKEN found in the local creds.json file
    '''

    # get API token from creds.json file
    API_TOKEN = ''
    credentials_file = os.path.join(os.path.dirname(__file__), 'creds.json')

    if os.path.isfile(credentials_file):
        sys.stdout.write('Credentials file found.\n')
        with open(credentials_file, 'r', encoding='utf-8') as f:
            API_TOKEN = json.loads(''.join(f.readlines()))['API_TOKEN'];
    else:
        raise FileNotFoundError(f'Credentials file not found at: {credentials_file}')

    return API_TOKEN

def exportCSV (data_iterator, CSV_FILE: str) -> None:
    '''
    Export data to csv.

    :param data_iter: an iterator of the data to be exported to the csv file
    :param csvFilepath: filepath to csv to export data to.
    '''

    sys.stdout.write(f'Exporting data to {CSV_FILE}\n')
    with open(CSV_FILE, 'w', encoding='utf-8') as f:
        f.write('url,title,views,date,tags\n')

        for item in data_iterator:
            item = processRawData([item])
            if item:
                item = item[0]
                f.write(f"{item['url']},{item['title']},{item['views']},{item['date']},{'/'.join(item['tags'])}\n")


if __name__ == '__main__':

    # parse arguments
    # channel url
    start_urls = [{'url' : url.strip()} for url in sys.stdin.readlines() if url.strip()]

    # output csv file
    if sys.argv[1]:
        # run.sh still passes '' when no argument is passed so we check for empty string
        CSV_FILE = sys.argv[1]
    else:
        raise ValueError('No output csv file specified.\n')

    # max results to return
    if sys.argv[2]:
        # run.sh still passes '' when no argument is passed so we check for empty string
        try:
            MAX_RESULTS = int(sys.argv[2])
            sys.stdout.write(f'Max results set to: {MAX_RESULTS}.\n')
        except ValueError:
            sys.stderr.write(f'Max results must be an integer but got: {sys.argv[2]}.\n')
    else:
        # if no number for max results is passed then sys.argv[2] == ''
        sys.stdout.write('Number for max results not found. Will request all channel videos.\n')
        MAX_RESULTS = 0

    # get API token from local cred.json file
    API_TOKEN = read_credentials()

    # make API request and get raw data
    sys.stdout.write(f'Making requests for: {[url for url in start_urls]}\n')
    data_iterator = makeRequest(start_urls, MAX_RESULTS, token=API_TOKEN)

    # write data to a csv file
    exportCSV(data_iterator, CSV_FILE)
