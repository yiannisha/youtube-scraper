#!/usr/bin/env python3

''' A module to extract youtube data from a json file '''

import os
import sys
import json

import scrape

from typing import Dict

def jsonFileData(filepath: str) -> Dict[str, any]:
    '''
    Returns data from a json file.
    '''

    data = []

    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.loads(''.join(f.readlines()))

    return data

if __name__ == '__main__':

    # parse arguments
    try:
        CSV_FILE = sys.argv[1]
    except:
        raise IndexError('No output csv file passed.')
    try:
        filepath = sys.argv[2]
    except:
        raise FileNotFoundError('No json filepath passed.')

    # get data from file
    file_data = jsonFileData(filepath)

    # write data to csv file
    sys.stdout.write(f'Exporting data to {CSV_FILE}\n')
    with open(CSV_FILE, 'w', encoding='utf-8') as f:
        f.write('url,title,views,date,tags\n')

        for item in file_data:
            item = scrape.processRawData([item])
            if item:
                item = item[0]
                f.write(f"{item['url']},{item['title']},{item['views']},{item['date']},{'/'.join(item['tags'])}\n")
